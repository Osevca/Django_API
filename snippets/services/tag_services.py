from django.core.exceptions import ValidationError

from core.models import Tag

def create_tag(name: str) -> Tag:
    if Tag.objects.filter(name=name).exists():
        raise ValidationError(f"Tag with name '{name}' already exists.")
    return Tag.objects.create(name=name)

def update_tag(tag: Tag, name= str) -> Tag:
    # if name and Tag.objects.filter(name=name).exclude(id=tag.id).exists():
    #     raise ValidationError(f"Tag with name '{name}' already exists.")
    # tag.name = name if name else tag.name

    if not name.strip():
        raise ValidationError("Tag name cannot be empty.")

    if Tag.objects.filter(name=name).exclude(id=tag.id).exists():
        raise ValidationError(f"Tag with name '{name}' already exists.")

    tag.name = name
    tag.save()
    return tag

def delete_tag(tag: Tag) -> None:
    tag.delete()