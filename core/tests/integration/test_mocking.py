import pytest
from unittest.mock import patch

from core.models import Note, CustomUser
from core.auth import AuthBearer
from core.signals import logger
from django.utils import timezone

@pytest.mark.django_db
class TestNoteAPIWithMocking:

    @patch.object(AuthBearer, 'authenticate')
    @patch('snippets.apis.notes_api.create_note')
    def test_create_note_with_mocked_service(self, mock_create_note, mock_authenticate, authenticated_client, user):
        logger.info("Starting test_create_note_with_mocked_service")
        logger.info(f"mock_create_note: {mock_create_note}")

        mock_authenticate.return_value = user
        logger.info(f"Mock authentication set up for user: {user}")

        mock_note = Note(
            id=1,
            title="Mocked Note",
            content="Mocked Content",
            user=user,
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )
        mock_create_note.return_value = mock_note
        logger.info(f"mock_create_note.return_value = {mock_create_note.return_value}")

        logger.info("Mock note and endpoint response set up")

        payload = {
            "title": "Test Note",
            "content": "This is a test note",
        }
        headers = authenticated_client.get_headers()
        logger.info(f"Sending request with payload: {payload} and headers: {headers}")

        response = authenticated_client.post("/notes/", json=payload, headers=headers)

        logger.info(f'status code: {response.status_code}')
        logger.info(f'content: {response.content}')
        assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}"
        logger.debug(f'create_note was not called {mock_create_note.called}******************************')
        assert mock_create_note.called, "create_note was not called"
        called_args, called_kwargs = mock_create_note.call_args
        logger.info(f"Called args: {called_args}, Called kwargs: {called_kwargs}")

        assert "title" in called_kwargs
        assert called_kwargs["title"] == "Test Note"
        assert called_kwargs["user"] == user


    def test_create_note_unauthenticated(self, client):
        payload = {
            "title": "Test Note",
            "content": "This is a test note",
        }
        response = client.post("/notes/", json=payload)

        assert response.status_code == 401
