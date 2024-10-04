import pytest
from django.utils import timezone
from core.models import Note, Group, Tag, CustomUser as User
import time

@pytest.mark.django_db
class TestSignals:
    @pytest.fixture(autouse=True)
    def setup(self, db):
        self.user, _ = User.objects.get_or_create(username='testuser', defaults={'password': '12345'})
        self.other_user, _ = User.objects.get_or_create(username='otheruser', defaults={'password': '12345'})
        self.note = Note.objects.create(user=self.user, title='Test Note', content='This is a test note.')
        self.group = Group.objects.create(name='Test Group')
        self.tag = Tag.objects.create(name='Test Tag')

        self.group.users.add(self.user)
        self.group.users.add(self.other_user)
        self.tag.users.add(self.user)
        self.tag.users.add(self.other_user)

    def test_user_delete_signal(self):
        user_id = self.user.id
        note_id = self.note.id
        group_id = self.group.id
        tag_id = self.tag.id

        self.user.delete()

        assert not Note.objects.filter(id=note_id).exists()
        assert Group.objects.filter(id=group_id).exists()
        assert Tag.objects.filter(id=tag_id).exists()
        assert not self.group.users.filter(id=user_id).exists()
        assert not self.tag.users.filter(id=user_id).exists()

    def test_note_delete_signal(self):
        note_id = self.note.id
        self.note.delete()

        assert not Note.objects.filter(id=note_id).exists()
        assert User.objects.filter(id=self.user.id).exists()

    def test_group_delete_signal(self):
        group_id = self.group.id

        self.group.delete()

        assert not Group.objects.filter(id=group_id).exists()
        assert User.objects.filter(id=self.user.id).exists()
        assert User.objects.filter(id=self.other_user.id).exists()

    def test_tag_delete_signal(self):
        tag_id = self.tag.id

        self.tag.delete()

        assert not Tag.objects.filter(id=tag_id).exists()
        assert User.objects.filter(id=self.user.id).exists()
        assert User.objects.filter(id=self.other_user.id).exists()

    def test_cascade_delete_user_with_multiple_notes_and_groups(self):
        user, _ = User.objects.get_or_create(username='multiuser', defaults={'password': '12345'})
        note1 = Note.objects.create(user=user, title='Note 1', content='Content 1')
        note2 = Note.objects.create(user=user, title='Note 2', content='Content 2')
        group1 = Group.objects.create(name='Group 1')
        group2 = Group.objects.create(name='Group 2')
        user.groups.add(group1.id, group2.id)

        user_id = user.id
        note1_id = note1.id
        note2_id = note2.id
        group1_id = group1.id
        group2_id = group2.id

        user.delete()

        assert not User.objects.filter(id=user_id).exists()
        assert not Note.objects.filter(id=note1_id).exists()
        assert not Note.objects.filter(id=note2_id).exists()
        assert Group.objects.filter(id=group1_id).exists()
        assert Group.objects.filter(id=group2_id).exists()
        assert not group1.users.filter(id=user_id).exists()
        assert not group2.users.filter(id=user_id).exists()

    def test_orphaned_group_and_tag_deletion(self):
        user, _ = User.objects.get_or_create(username='orphanuser', defaults={'password': '12345'})
        group = Group.objects.create(name='Orphan Group')
        tag = Tag.objects.create(name='Orphan Tag')

        group.users.add(user)
        tag.users.add(user)

        Note.objects.create(user=user, title='Orphan Note', content='Content', group=group)
        user.tags.add(tag)

        user_id = user.id
        group_id = group.id
        tag_id = tag.id

        user.delete()

        assert not User.objects.filter(id=user_id).exists()
        assert not Group.objects.filter(id=group_id).exists()
        assert not Tag.objects.filter(id=tag_id).exists()

    def test_note_update_signal(self):
        note = Note.objects.create(user=self.user, title='Original Title', content='Original content')
        original_updated_at = note.updated_at

        time.sleep(0.1)

        note.title = 'Updated Title'
        note.save()

        updated_note = Note.objects.get(id=note.id)
        assert updated_note.updated_at > original_updated_at