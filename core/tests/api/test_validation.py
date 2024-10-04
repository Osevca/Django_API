import pytest
from unittest.mock import patch
from core.models import Note
from django.utils import timezone
from datetime import timedelta

@pytest.mark.django_db
class TestNoteAPIValidations:

    def test_create_note_with_invalid_expiration_date(self, authenticated_client, user):
        invalid_expiration_date = timezone.now() - timedelta(days=1)
        payload = {
            "title": "Invalid Note",
            "content": "This note has invalid expiration date",
            "expiration_date": invalid_expiration_date.isoformat(),
            # "user": user.id

        }
        response = authenticated_client.post("/notes/", json=payload, headers=authenticated_client.get_headers())
        print(f"Response JSON: {response.json()}")

        assert response.status_code == 400, f"Expected status code 400 gott {response.status_code}"
        assert "error" in response.json(), f"Expected 'error' in response is: {response.json()}"
        assert "Expiration date must be in the future" in response.json()["error"], f"Unexpected error message: {response.json()}"

    def test_update_nonexistent_note(self, authenticated_client):
        response = authenticated_client.patch("/notes/99999", json={"title": "Updated Title"}, headers=authenticated_client.get_headers())
        assert response.status_code == 404, f"Expected status code 404, got {response.status_code}"

