from typing import List
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils import timezone

from core.signals import logger
from core.models import Note,Group, CustomUser as User

def create_note(user: User, title: str, content: str, expiration_date=None, group=None, tags: List[int] = None) -> Note:
    logger.info(f"create_note called with: user={user}, title={title}, content={content}")
    if group is not None and isinstance(group, int):
        group = get_object_or_404(Group, id=group)

    note = Note.objects.create(
        user=user,
        title=title,
        content=content,
        expiration_date=expiration_date,
        group=group,
    )
    if tags:
        note.tags.set(tags)

    return note

def update_note(note: Note, title=None, content=None, expiration_date=None, group=None, tags=None) -> Note:
    if title and Note.objects.filter(title=title, user=note.user).exclude(id=note.id).exists():
        raise ValidationError(f"Note with title '{title}' already exists for this user.")

    if title:
        note.title = title
    if content:
        note.content = content
    if expiration_date:
        note.expiration_date = expiration_date
    if group:
        note.group = group
    if tags:
        note.tags.set(tags)

    note.save()
    return note


# @transaction.atomic
def delete_note(note):
    logger.info(f"Starting deleting note: '{note.id}' - '{note.title}'")
    logger.info(f"Initial state: Group: '{note.group}', Tags: '{list(note.tags.all())}', User: '{note.user}'")
    group_to_check = note.group
    group_id = group_to_check.id if group_to_check else None
    tags_to_check = list(note.tags.all())
    user = note.user
    note.tags.clear()
    logger.info(f"Note '{note.id}' deleted")
    note.delete()

    if group_id:
        group = Group.objects.filter(id=group_id).first()
        if group:
            logger.info(f"Group '{group.id}' check: notes='{group.notes.count()}', users='{group.users.count()}'")
            if group.notes.count() == 0 and group.users.count() == 0:
                group.delete()
                logger.info(f"Group '{group_id}' deleted")
            else:
                logger.info(f"Group '{group_id}' retained: has '{group.notes.count()}'notes and '{group.users.count()}' users")

    for tag in tags_to_check:
        logger.info(f"Tag {tag.id} check: notes={tag.notes.count()}, users={tag.users.count()}")
        if tag.notes.count() == 0 and tag.users.count() == 0:
            tag.delete()
            logger.info(f"Tag {tag.id} deleted")
        else:
            logger.info(f"Tag {tag.id} retained: has {tag.notes.count()} notes and {tag.users.count()} users")

    user.updated_at = timezone.now()
    user.save()
    logger.info(f"User {user.id} updated_at updated")
    logger.info("Note deletion process completed")


def serialize_note(note: Note) -> dict:
    return {
        'id': note.id,
        'title': note.title,
        'content': note.content,
        'user_id': note.user.id,
        'group': note.group.id if note.group else None,
        'tags': [tag.id for tag in note.tags.all()],
        "created_at": note.created_at.isoformat(),
        "updated_at": note.updated_at.isoformat(),
        "expiration_date": note.expiration_date.isoformat() if note.expiration_date else None
    }

def list_notes_serialized(user_id: int = None) -> List[dict]:
    if user_id:
        notes = Note.objects.filter(user_id=user_id).order_by('-created_at')
    else:
        notes = Note.objects.all().order_by('-created_at')
    return [serialize_note(note) for note in notes]


@transaction.atomic
def delete_user(user: User) -> None:
    Note.objects.filter(user=user).delete()
    user.tags.clear()
    user.groups.clear()
    user.delete()