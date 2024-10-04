from typing import List
# from ninja.errors import HttpError
from django.shortcuts import get_object_or_404
from ninja import Router

from core.models import Group
from snippets.services.group_services import create_group, update_group, delete_group, serialize_group, list_groups_serialized
from snippets.dtos.group_schema import GroupIn, GroupOut, GroupUpdate

router = Router(tags=['groups'])


@router.get('/', response=List[GroupOut])
def list_groups(request):
    return list_groups_serialized()

@router.get('/{group_id}', response=GroupOut)
def get_group_by_id(request, group_id: int):
    group = get_object_or_404(Group, id=group_id)
    return serialize_group(group)

@router.post('/', response=GroupOut)
def create_group_endpoint(request, payload: GroupIn):
    group = create_group(name=payload.name, tags=payload.tags)
    return serialize_group(group)

@router.put('/{group_id}', response=GroupOut)
def update_group_endpoint(request, group_id: int, payload: GroupUpdate):
    group = get_object_or_404(Group, id=group_id)
    updated_group = update_group(group, **payload.dict(exclude_unset=True))
    return serialize_group(updated_group)

@router.patch('/{group_id}', response=GroupOut)
def patch_group_endpoint(request, group_id: int, payload: GroupUpdate):
    group = get_object_or_404(Group, id=group_id)
    updated_group = update_group(group, **payload.dict(exclude_unset=True))
    return serialize_group(updated_group)

@router.delete('/{group_id}')
def delete_group_endpoint(request, group_id: int):
    group = get_object_or_404(Group, id=group_id)
    delete_group(group)
    return {'success': True}

