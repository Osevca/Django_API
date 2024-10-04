from celery import shared_task
from django.utils import timezone
from core.models import Note
from django.db.models import Q
from core.signals import logger


@shared_task
def delete_expired_notes():
    deleted_count, _ = Note.objects.filter(Q(expiration_date__lte=timezone.now()) & Q(expiration_date__isnull=False)).delete()
    logger.info(f"Deleted '{deleted_count}' expired notes.")