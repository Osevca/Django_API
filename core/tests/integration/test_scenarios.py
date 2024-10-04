import pytest
from unittest.mock import patch
from core.models import Note, Group, Tag



@pytest.mark.django_db
class TestComplexScenarios:

    def test_create_note_with_group_and_tags(self, authenticated_client , user):
        group = Group.objects.create(name="Test Group")
        tag1 = Tag.objects.create(name="Tag1")
        tag2 = Tag.objects.create(name="Tag2")

        payload = {
            "title": "Complex Note",
            "content": "This note has a group and tags",
            "group": group.id,
            "tags": [tag1.id, tag2.id]
        }
        response = authenticated_client.post("/notes/", json=payload, headers=authenticated_client.get_headers())
        assert response.status_code == 201
        assert response.json()["group"] == group.id
        assert set(response.json()["tags"]) == {tag1.id, tag2.id}