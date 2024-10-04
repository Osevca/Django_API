import os
import django
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "snippets.settings")
django.setup()

import pytest
from ninja.testing import TestClient
from snippets.api import api
from core.models import CustomUser as User
from core.auth import create_token
import uuid
from core.signals import logger

@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        User.objects.get_or_create(username='testuser', defaults={'password': '12345'})

@pytest.fixture
def user(db):
    unique_username = f'testuser_{uuid.uuid4().hex[:8]}'
    user, _ = User.objects.get_or_create(username=unique_username, defaults={'password': 'testpass'})
    return user

@pytest.fixture
def client(scope="function"):
    return TestClient(api)


@pytest.fixture
def authenticated_client(client, user):
    token = create_token(user)
    print(f"Generated Token: {token}")

    def get_headers():
        return {"Authorization": f"Bearer {token}"}

    client.get_headers = get_headers
    return client

@pytest.fixture(autouse=True, scope="function")
def clear_ninja_registry():
    from ninja import NinjaAPI
    NinjaAPI._registry.clear()
    yield
    NinjaAPI._registry.clear()