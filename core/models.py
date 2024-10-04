from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.conf import settings


class CustomUser(AbstractUser):
    bio = models.TextField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="tags")

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    tags = models.ManyToManyField(Tag, related_name="tag_groups")
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="user_groups")

    def __str__(self):
        return self.name


class Note(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expiration_date = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_notes")
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, related_name="notes")
    tags = models.ManyToManyField(Tag, related_name="notes")

    class Meta:
        ordering = ['-created_at']

    def clean(self):
        if self.expiration_date:
            if self.expiration_date.tzinfo is None:
                self.expiration_date = timezone.make_aware(self.expiration_date)

            if self.expiration_date <= timezone.now():
                raise ValidationError('Expiration date must be in the future.(models.py)')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def is_expired(self):
        return self.expiration_date and self.expiration_date < timezone.now()

    @property
    def days_until_expiration(self):
        if self.expiration_date:
            delta = self.expiration_date - timezone.now()
            return max(delta.days, 0)
        return None