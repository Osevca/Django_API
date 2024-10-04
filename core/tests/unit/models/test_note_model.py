import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from unittest.mock import patch

from core.models import CustomUser as User, Tag, Group, Note
from snippets.tasks import delete_expired_notes

@pytest.mark.django_db
class TestNoteModel:
    @pytest.fixture(autouse=True)
    def setup(self, db):
        self.user, _ = User.objects.get_or_create(
            username='testuser',
            defaults={'password': 'testpass'}
        )
        self.group = Group.objects.create(name='Test Group')
        self.tag = Tag.objects.create(name='Test Tag')

    def test_create_note(self):
        note = Note.objects.create(
            title='Test Note',
            content='This is a test note',
            user=self.user,
            group=self.group
        )
        note.tags.add(self.tag)
        assert note.title == 'Test Note'
        assert note.content == 'This is a test note'
        assert note.user == self.user
        assert note.group == self.group
        assert self.tag in note.tags.all()

    def test_note_str(self):
        note = Note.objects.create(title='Test Note', content='Content', user=self.user)
        assert str(note) == 'Test Note'

    def test_note_expiration(self):
        future_date = timezone.now() + timedelta(days=1)
        note = Note.objects.create(
            title='Future Expiration',
            content='This note will expire soon',
            user=self.user,
            expiration_date=future_date
        )

        assert Note.objects.filter(id=note.id).exists()

        with patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = future_date + timedelta(days=1)
            delete_expired_notes.apply()
            assert not Note.objects.filter(id=note.id).exists()

    def test_note_ordering(self):
        note1 = Note.objects.create(title='Note 1', content='Content 1', user=self.user)
        note2 = Note.objects.create(title='Note 2', content='Content 2', user=self.user)
        notes = Note.objects.all()
        assert notes[0] == note2
        assert notes[1] == note1

    def test_note_without_group(self):
        note = Note.objects.create(
            title='Note without group',
            content='This note has no group',
            user=self.user
        )
        assert note.group is None

    def test_note_with_multiple_tags(self):
        tag1 = Tag.objects.create(name='Tag 1')
        tag2 = Tag.objects.create(name='Tag 2')
        note = Note.objects.create(
            title='Multi-tag Note',
            content='This note has multiple tags',
            user=self.user
        )
        note.tags.add(tag1, tag2)
        assert note.tags.count() == 2
        assert tag1 in note.tags.all()
        assert tag2 in note.tags.all()

    def test_note_expiration_date_timezone_aware(self):
        naive_date = timezone.now().replace(tzinfo=None) + timedelta(days=7)
        note = Note.objects.create(
            title='Timezone Note',
            content='This note tests timezone awareness',
            user=self.user,
            expiration_date=naive_date
        )
        assert timezone.is_aware(note.expiration_date)

    def test_note_days_until_expiration_edge_cases(self):
        note_no_expiration = Note.objects.create(
            title='No Expiration',
            content='This note has no expiration date',
            user=self.user
        )
        assert note_no_expiration.days_until_expiration is None

        past_date = timezone.now() - timedelta(days=1)
        with pytest.raises(ValidationError):
            Note.objects.create(
                title='Past Expiration',
                content='This note has expired',
                user=self.user,
                expiration_date=past_date
            )

        future_date = timezone.now() + timedelta(days=1)
        note = Note.objects.create(
            title='Future Expiration',
            content='This note will expire soon',
            user=self.user,
            expiration_date=future_date
        )
        assert note.days_until_expiration is not None