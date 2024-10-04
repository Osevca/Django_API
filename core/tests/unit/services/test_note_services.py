import pytest
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError

from snippets.services.note_services import create_note, update_note, delete_note, serialize_note, list_notes_serialized
from core.models import Note, Group, Tag, CustomUser as User

@pytest.mark.django_db
class TestNoteService:
    @pytest.fixture(autouse=True)
    def setup(self, db):
        self.user, _ = User.objects.get_or_create(username='testuser', defaults={'password': 'password'})
        self.group = Group.objects.create(name='Test Group')
        self.tag1 = Tag.objects.create(name='Test Tag 1')
        self.tag2 = Tag.objects.create(name='Test Tag 2')

    def test_create_note_success(self):
        expiration_date = timezone.now() + timedelta(days=7)
        note = create_note(
            user=self.user,
            title='Test Note',
            content='This is a test note.',
            expiration_date=expiration_date,
            group=self.group,
            tags=[self.tag1.id, self.tag2.id]
        )
        assert note.title == 'Test Note'
        assert note.content == 'This is a test note.'
        assert note.user == self.user
        assert note.group == self.group
        assert note.expiration_date == expiration_date
        assert self.tag1 in note.tags.all()
        assert self.tag2 in note.tags.all()

    def test_update_note_success(self):
        note = create_note(
            user=self.user,
            title='Original Title',
            content='Original content.',
            group=self.group,
            tags=[self.tag1.id]
        )
        new_expiration_date = timezone.now() + timedelta(days=14)
        updated_note = update_note(
            note,
            title='Updated Title',
            content='Updated content.',
            expiration_date=new_expiration_date,
            tags=[self.tag2.id]
        )
        assert updated_note.title == 'Updated Title'
        assert updated_note.content == 'Updated content.'
        assert updated_note.expiration_date == new_expiration_date
        assert self.tag2 in updated_note.tags.all()
        assert self.tag1 not in updated_note.tags.all()

    def test_delete_note_success(self):
        note = create_note(
            user=self.user,
            title='Test Note',
            content='This is a test note.',
            group=self.group,
            tags=[self.tag1.id]
        )
        delete_note(note)
        assert not Note.objects.filter(id=note.id).exists()

    def test_update_note_duplicate_title(self):
        create_note(user=self.user, title='Existing Note', content='Content')
        note = create_note(user=self.user, title='Original Note', content='Content')

        with pytest.raises(ValidationError):
            update_note(note, title='Existing Note')

    def test_serialize_note(self):
        expiration_date = timezone.now() + timedelta(days=7)
        note = create_note(
            user=self.user,
            title='Test Note',
            content='This is a test note.',
            expiration_date=expiration_date,
            group=self.group,
            tags=[self.tag1.id, self.tag2.id]
        )
        serialized = serialize_note(note)

        assert serialized['title'] == 'Test Note'
        assert serialized['content'] == 'This is a test note.'
        assert serialized['user_id'] == self.user.id
        assert serialized['group'] == self.group.id
        assert self.tag1.id in serialized['tags']
        assert self.tag2.id in serialized['tags']
        assert serialized['expiration_date'] == expiration_date.isoformat()

    def test_list_notes_serialized(self):
        note1 = create_note(user=self.user, title='Note 1', content='Content 1')
        note2 = create_note(user=self.user, title='Note 2', content='Content 2')

        serialized_notes = list_notes_serialized(self.user.id)

        assert len(serialized_notes) == 2

        titles = [note['title'] for note in serialized_notes]
        assert 'Note 1' in titles
        assert 'Note 2' in titles

        assert serialized_notes[0]['id'] == note2.id
        assert serialized_notes[1]['id'] == note1.id

    def test_create_note_without_group_and_tags(self):
        note = create_note(
            user=self.user,
            title='Simple Note',
            content='This is a simple note without group and tags.'
        )
        assert note.group is None
        assert note.tags.count() == 0

    def test_update_note_partial(self):
        note = create_note(
            user=self.user,
            title='Original Title',
            content='Original content.'
        )
        updated_note = update_note(
            note,
            content='Updated content.',
        )
        assert updated_note.title == 'Original Title'
        assert updated_note.content == 'Updated content.'

    def test_list_notes_serialized_empty(self):
        serialized_notes = list_notes_serialized(self.user.id)
        assert len(serialized_notes) == 0

    def test_delete_note_with_group_and_tags(self):
        user, _ = User.objects.get_or_create(username='testuser2', defaults={'password': 'password'})
        group = Group.objects.create(name='Test Group for deletion')
        tag1 = Tag.objects.create(name='Test Tag 1 for deletion')
        tag2 = Tag.objects.create(name='Test Tag 2 for deletion')

        note = create_note(
            user=user,
            title='Test Note for deletion',
            content='This is a test note for deletion.',
            group=group,
            tags=[tag1.id, tag2.id]
        )
        group.users.add(user)
        tag1.users.add(user)
        tag2.users.add(user)

        note_id = note.id
        group_id = group.id
        tag1_id = tag1.id
        tag2_id = tag2.id

        delete_note(note)

        assert not Note.objects.filter(id=note_id).exists()
        assert Group.objects.filter(id=group_id).exists()
        assert Tag.objects.filter(id=tag1_id).exists()
        assert Tag.objects.filter(id=tag2_id).exists()
        assert User.objects.filter(id=self.user.id).exists()

        group.delete()
        tag1.delete()
        tag2.delete()
        user.delete()