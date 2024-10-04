from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
import logging
from django.utils import timezone
from django.db.models import Count


from core.models import Note, Group, Tag, CustomUser as User


logger = logging.getLogger(__name__)

@receiver(post_save, sender=Note)
def note_created(sender, instance, created, **kwargs):
    if created:
        logger.info(f'Note titled "{instance.title}" was created.')


@receiver(pre_delete, sender=User)
def delete_related_objects(sender, instance, **kwargs):
    logger.info(f'Deleting all objects related to user: {instance.username}')

    Note.objects.filter(user=instance).delete()

    groups = instance.user_groups.all()
    tags = instance.tags.all()

    for group in groups:
        group.users.remove(instance)
        if group.users.count() == 0:
            group.delete()

    for tag in tags:
        tag.users.remove(instance)
        if tag.users.count() == 0:
            tag.delete()

    logger.info(f"Related objects for user {instance.username} have been handled.")


@receiver(pre_delete, sender=Group)
def handle_orphaned_notes(sender, instance, **kwargs):
    logger.info(f"Deleting orphaned notes for group: {instance.name}")

    orphaned_notes = instance.notes.all()
    for note in orphaned_notes:
        logger.info(f"Deleting orphaned note: {note.title}")
        note.delete()
    logger.info(f'Handled {orphaned_notes.count()} orphaned notes after group deletion.')



@receiver(post_save, sender=Note)
def update_user_updated_at(sender, instance, **kwargs):
    instance.user.updated_at = timezone.now()
    instance.user.save()


@receiver(post_save, sender=Note)
def log_note_changes(sender, instance, created, **kwargs):
    if created:
        logger.info(f"New note created: '{instance.title}' by user '{instance.user.username}'")
    else:
        logger.info(f"Note updated: '{instance.title}' by user '{instance.user.username}'")
