# import pytest
# from django.utils import timezone
# from core.models import Note, Group, Tag

# @pytest.mark.django_db
# class TestNoteApi:

#     def test_create_note(self, client, user):
#         payload = {
#             "title": "Test Note",
#             "content": "This is a test note",
#             "expiration_date": (timezone.now() + timezone.timedelta(days=1)).isoformat(),
#             "user": user.id
#         }
#         response = client.post('/api/notes/', json=payload)

#         assert response.status_code == 200
#         assert response.json()['title'] == 'Test Note'

#     def test_get_note(self, client, user):
#         note = Note.objects.create(title='Existing Note', content='Content', user=user)
#         response = client.get(f'/api/notes/{note.id}')

#         assert response.status_code == 200
#         assert response.json()['title'] == 'Existing Note'

#     def test_update_note(self, client, user):
#         note = Note.objects.create(title='Old Title', content='Old Content', user=user)
#         payload = {
#             "title": "Updated Title",
#         }
#         response = client.patch(f'/api/notes/{note.id}', json=payload)

#         assert response.status_code == 200
#         assert response.json()['title'] == 'Updated Title'

#     def test_delete_note(self, client, user):
#         note = Note.objects.create(title='To Delete', content='Content', user=user)
#         response = client.delete(f'/api/notes/{note.id}')

#         assert response.status_code == 200
#         assert not Note.objects.filter(id=note.id).exists()