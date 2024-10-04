import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from core.models import CustomUser as User, Tag, Group, Note

@pytest.mark.django_db
class TestCustomUserModel:

    def test_create_user(self):
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={'password': 'testpass'}
        )
        assert user.username == 'testuser'
        if created:
            assert user.check_password('testpass')
        else:
            print("User 'testuser' already existed, skipping password check.")

    def test_user_str(self):
        user, _ = User.objects.get_or_create(username='testuser')
        assert str(user) == 'testuser'