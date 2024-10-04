from typing import List
from ninja.errors import HttpError
from django.shortcuts import get_object_or_404
from ninja import Router
from django.http import Http404
from django.core.exceptions import ValidationError

from core.models import Note, Group, Tag, CustomUser as User
from snippets.services.note_services import create_note, update_note, delete_note, serialize_note, list_notes_serialized, delete_user
from snippets.dtos.note_schema import NoteIn, NoteOut, NoteUpdate
from core.signals import logger
from core.auth import AuthBearer



router = Router(tags=['notes'],auth=AuthBearer())


@router.get('/', response=List[NoteOut])
def list_notes(request):
    return list_notes_serialized()

@router.get('/{note_id}', response=NoteOut)
def get_note_by_id(request, note_id: int):
    note = get_object_or_404(Note, id=note_id)
    return serialize_note(note)

@router.post('/', response={201:NoteOut, 401: dict, 400: dict})
def create_note_endpoint(request, payload: NoteIn):
    print(f"create_note_endpoint called. Request auth: {request.auth}")
    logger.debug(f"Received payload: {payload}")
    logger.debug(f"Request auth: {request.auth}")
    # logger.debug(f"Request user: {getattr(request, 'user', None)}")
    user = request.auth
    if user is None:
        logger.warning("Unauthenticated user tried to create a note")
        print("User is None, returning 401")
        return 401, {'error': 'User must be authenticated'}

    # if not request.user.is_authenticated:
    #     return {'error': 'User must be authenticated'}, 401
    group = get_object_or_404(Group, id=payload.group) if payload.group else None
    tags = Tag.objects.filter(id__in=payload.tags) if payload.tags else []
    # tags = payload.tags if payload.tags else []

    try:
        note = create_note(
            user=user,
            title=payload.title,
            content=payload.content,
            expiration_date=payload.expiration_date,
            group=group,
            tags=tags
        )
        logger.info(f"Note created: {note}")
        return 201, serialize_note(note)
    except ValidationError as e:
        return 400, {'error': str(e)}

@router.put('/{note_id}', response=NoteOut)
def update_note_endpoint(request, note_id: int, payload: NoteUpdate):
    note = get_object_or_404(Note, id=note_id)

    # if note.user != request.user:
    #     raise HttpError(403, 'You can only edit your own notes.')

    group = get_object_or_404(Group, id=payload.group) if payload.group else note.group
    tags = Tag.objects.filter(id__in=payload.tags) if payload.tags else note.tags.all()

    updated_note = update_note(
        note,
        title=payload.title,
        content=payload.content,
        expiration_date=payload.expiration_date,
        group=group,
        tags=tags
    )
    return serialize_note(updated_note)


@router.patch('/{note_id}', response=NoteOut)
def patch_note_endpoint(request, note_id: int, payload: NoteUpdate):
    note = get_object_or_404(Note, id=note_id)

    # if note.user != request.user:
    #     raise HttpError(403, 'You can only edit your own notes.')

    group = get_object_or_404(Group, id=payload.group) if payload.group else note.group
    tags = Tag.objects.filter(id__in=payload.tags) if payload.tags else note.tags.all()

    updated_note = update_note(
        note,
        title=payload.title,
        content=payload.content,
        expiration_date=payload.expiration_date,
        group=group,
        tags=tags
    )
    return serialize_note(updated_note)


@router.delete('/{note_id}')
def delete_note_endpoint(request, note_id: int):
    note = get_object_or_404(Note, id=note_id)

    # if note.user != request.user:
    #     raise HttpError(403, 'You can only delete your own notes.')

    delete_note(note)
    return {'success': True}