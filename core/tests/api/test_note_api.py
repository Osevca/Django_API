import pytest
from django.utils import timezone
from ninja.testing import TestClient

from core.models import Note
from core.auth import create_token


@pytest.mark.django_db
class TestNoteApi:

    def test_create_note(self, authenticated_client, user):
        payload = {
            "title": "Test Note",
            "content": "This is a test note",
            "expiration_date": (timezone.now() + timezone.timedelta(days=1)).isoformat(),
        }
        headers = authenticated_client.get_headers()
        response = authenticated_client.post('/notes/', json=payload, headers=headers)

        assert response.status_code == 201
        assert response.json()['title'] == 'Test Note'

    def test_get_note(self, authenticated_client, user):
        note = Note.objects.create(title='Existing Note', content='Content', user=user)
        headers = authenticated_client.get_headers()
        response = authenticated_client.get(f'/notes/{note.id}', headers=headers)

        assert response.status_code == 200
        assert response.json()['title'] == 'Existing Note'

    def test_update_note(self, authenticated_client, user):
        note = Note.objects.create(title='Old Title', content='Old Content', user=user)
        payload = {
            "title": "Updated Title",
        }
        headers = authenticated_client.get_headers()
        response = authenticated_client.patch(f'/notes/{note.id}', json=payload, headers=headers)

        assert response.status_code == 200
        assert response.json()['title'] == 'Updated Title'

    def test_delete_note(self, authenticated_client, user):
        note = Note.objects.create(title='To Delete', content='Content', user=user)
        headers = authenticated_client.get_headers()
        response = authenticated_client.delete(f'/notes/{note.id}', headers=headers)

        assert response.status_code == 200
        assert not Note.objects.filter(id=note.id).exists()

    def test_list_notes(self, authenticated_client, user):
        Note.objects.create(title='Note 1', content='Content 1', user=user)
        Note.objects.create(title='Note 2', content='Content 2', user=user)

        headers = authenticated_client.get_headers()
        response = authenticated_client.get('/notes/', headers=headers)

        assert response.status_code == 200
        assert len(response.json()) == 2