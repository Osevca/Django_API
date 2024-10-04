from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from core.models import CustomUser as User, Tag, Group, Note
import pytest


@pytest.mark.django_db
class CustomUserMOdelTest(TestCase):
    def test_create_user(self):
        user, created = User.objects.get_or_create(username='newuser', defaults={'password': '12345'})
        assert User.objects.count() == 2
        assert user.username == 'newuser'

    def test_user_str(self):
        user = User.objects.get(username='testuser')
        assert str(user) == 'testuser'


