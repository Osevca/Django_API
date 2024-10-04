from typing import List
from django.shortcuts import get_object_or_404
from ninja import Router

from core.models import Tag
from snippets.services.tag_services import create_tag, update_tag, delete_tag
from snippets.dtos.tag_schema import TagIn, TagOut, TagUpdate


router = Router(tags=['tags'])

@router.get('/', response=List[TagOut])
def list_tags(request):
    return Tag.objects.all()

@router.get('/{tag_id}', response=TagOut)
def get_tag_by_id(request, tag_id: int):
    tag = get_object_or_404(Tag, id=tag_id)
    return tag

@router.post('/', response=TagOut)
def create_tag_endpoint(request, payload: TagIn):
    tag = create_tag(name=payload.name)
    return tag

@router.put('/{tag_id}', response=TagOut)
def update_tag_endpoint(request, tag_id: int, payload: TagUpdate):
    tag = get_object_or_404(Tag, id=tag_id)
    updated_tag = update_tag(tag, name=payload.name)
    return updated_tag

@router.patch('/{tag_id}', response=TagOut)
def patch_tag_endpoint(request, tag_id: int, payload: TagUpdate):
    tag = get_object_or_404(Tag, id=tag_id)
    updated_tag = update_tag(tag, name=payload.name)
    return updated_tag

@router.delete('/{tag_id}')
def delete_tag_endpoint(request, tag_id: int):
    tag = get_object_or_404(Tag, id=tag_id)
    delete_tag(tag)
    return {'success': True}