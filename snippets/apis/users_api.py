from typing import List
from ninja.errors import HttpError
from django.shortcuts import get_object_or_404
from ninja import Router

from core.models import CustomUser as User
from snippets.services.user_services import update_user, delete_user
from snippets.services.note_services import list_notes_serialized
from snippets.dtos.user_schema import UserIn, UserOut, UserUpdate
from snippets.dtos.note_schema import NoteOut

router = Router(tags=['users'])

@router.get('/', response=List[UserOut])
def list_users(request):
    if not request.user.is_staff:
        raise HttpError(403, 'Only admins can access this endpoint.')
    return User.objects.all()

@router.get('/{user_id}/notes', response=List[NoteOut])
def get_user_notes(request, user_id: int):
    user = get_object_or_404(User, id=user_id)
    return list_notes_serialized(user_id=user_id)

@router.post('/', response=UserOut)
def create_user_endpoint(request, payload: UserIn):
    if not request.user.is_staff:
        raise HttpError(403, 'Only admins can access this endpoint.')
    user = User.objects.create_user(**payload.dict())
    return user

@router.put('/{user_id}', response=UserOut)
def update_user_endpoint(request, user_id: int, payload: UserUpdate):
    if not request.user.is_staff:
        raise HttpError(403, 'Only admins can access this endpoint.')
    user = get_object_or_404(User, id=user_id)
    updated_user = update_user(user, **payload.dict(exclude_unset=True))
    return updated_user

@router.delete('/{user_id}')
def delete_user_endpoint(request, user_id: int):
    if not request.user.is_staff:
        raise HttpError(403, 'Only admins can access this endpoint.')
    user = get_object_or_404(User, id=user_id)
    delete_user(user)
    return {'success': True}