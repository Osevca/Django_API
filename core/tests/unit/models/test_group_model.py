import pytest
from core.models import CustomUser as User, Tag, Group

@pytest.mark.django_db
class TestGroupModel:
    def test_create_group(self):
        group = Group.objects.create(name='Test Group')
        assert group.name == 'Test Group'

    def test_group_str(self):
        group = Group.objects.create(name='Test Group')
        assert str(group) == 'Test Group'

    def test_group_with_users_and_tags(self):
        user1, _ = User.objects.get_or_create(username='user1', defaults={'password': 'password1'})
        user2, _ = User.objects.get_or_create(username='user2', defaults={'password': 'password2'})
        tag1 = Tag.objects.create(name='GroupTag1')
        tag2 = Tag.objects.create(name='GroupTag2')

        group = Group.objects.create(name='Complex Group')
        group.users.add(user1, user2)
        group.tags.add(tag1, tag2)

        assert group.users.count() == 2
        assert group.tags.count() == 2
        assert user1 in group.users.all()
        assert user2 in group.users.all()
        assert tag1 in group.tags.all()
        assert tag2 in group.tags.all()