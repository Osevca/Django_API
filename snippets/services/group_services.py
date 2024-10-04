from typing import List
from django.core.exceptions import ValidationError
from django.db import transaction

from core.models import Group
from core.signals import logger



def create_group(name: str, tags: list[int] = None) -> Group:
    if not name.strip():
        raise ValidationError("Group name cannot be empty.")
    if Group.objects.filter(name=name).exists():
        raise ValidationError(f"Group with name '{name}'already exists.")
    group = Group.objects.create(name=name)
    if tags:
        group.tags.set(tags)
    return group

def update_group(group: Group, name: str = str, tags: list[int] = None) -> Group:
    if not name.strip():
        raise ValidationError("Group name cannot be empty.")
    if name and Group.objects.filter(name=name).exclude(id=group.id).exists():
        raise ValidationError(f"Group with name '{name}' already exists.")

    group.name = name if name else group.name
    if tags is not None:
        group.tags.set(tags)
    group.save()
    return group

@transaction.atomic
def delete_group(group: Group) -> None:
    logger.info(f"starting deletion of group: '{group.id}' - '{group.name}'")
    notes_to_check = list(group.notes.all())
    users_to_check = list(group.users.all())
    tags_to_check = list(group.tags.all())

    group.notes.clear()
    group.users.clear()
    group.tags.clear()

    group.delete()
    logger.info(f"Group '{group.id}' deleted")

    for note in notes_to_check:
        if note.group is None and note.tags.count() == 0:
            note.delete()
            logger.info(f"Orphaned note '{note.id}' deleted")

    for tag in tags_to_check:
        if tag.notes.count() == 0 and tag.users.count() == 0 and tag.groups.count() == 0:
            tag.delete()
            logger.info(f"Orphaned tag '{tag.id}' deleted")
    logger.info("Group deletion process completed")

def serialize_group(group: Group) -> dict:
    return {
        'id': group.id,
        'name': group.name,
        'tags': [tag.id for tag in group.tags.all()],
    }

def list_groups_serialized() -> List[dict]:
    groups = Group.objects.all()
    return [serialize_group(group) for group in groups]
