from django.shortcuts import get_object_or_404
from ninja import NinjaAPI
from ninja.errors import HttpError
from typing import List
from ninja.security import HttpBearer
from django.contrib.auth import authenticate
from django.conf import settings
from jose import jwt

from core.auth import create_token
from core.signals import logger
from snippets.dtos.login_schema import LoginSchema

from snippets.apis.users_api import router as users_router
from snippets.apis.notes_api import router as notes_router
from snippets.apis.groups_api import router as groups_router
from snippets.apis.tags_api import router as tags_router

from core.auth import auth


api = NinjaAPI(urls_namespace='myapi')

############################################################################
api.add_router('/users', users_router)
api.add_router('/notes', notes_router)
api.add_router('/groups', groups_router)
api.add_router('/tags', tags_router)
logger.debug(f"API routes after adding routers: {api.urls}")
############################################################################

@api.post('/login')
def login(request, payload: LoginSchema):
    user = authenticate(username=payload.username, password=payload.password)
    if user is None:
        return {'success': False, 'error': 'Invalid credentials'}
    token = create_token(user)
    return {'success': True, 'token': token}

@api.get('/protected', auth=auth)
def protected_route(request):
    print(f"Authenticated user: {request.auth}")
    return {'message': f'Hello, {request.auth.username}!'}


NinjaAPI._registry.clear()