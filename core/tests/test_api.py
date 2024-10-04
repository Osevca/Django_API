# from django.test import TestCase
# from ninja.testing import TestClient
# from core.models import Note, Group, Tag
# from django.contrib.auth import get_user_model
# from snippets.api import api


# User = get_user_model()

# class NoteAPITest(TestCase):
#     def setUp(self):
#         self.client = TestClient(api)
#         self.user = User.objects.create_user(username='testuser', password='password')
#         self.group = Group.objects.create(name='Test Group')
#         self.tag = Tag.objects.create(name='Test Tag')
#         self.note = Note.objects.create(
#             user=self.user,
#             title='Test Note',
#             content='This is a test note.',
#             group=self.group
#         )
#         self.note.tags.add(self.tag)

#     def test_list_notes(self):
#         response = self.client.get('/api/notes')
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(response.json()), 1)
#         self.assertEqual(response.json()[0]['title'], 'Test Note')

#     def test_create_note(self):
#         data = {
#             'title': 'New Note',
#             'content': 'New content',
#             'group': self.group.id,
#             'tags': [self.tag.id],
#             'expiration_date': '2024-09-20T05:11:09.432Z'
#         }
#         response = self.client.post('/api/notes', json=data)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(Note.objects.count(), 2)
#         self.assertEqual(Note.objects.latest('id').title, 'New Note')

#     def test_update_note(self):
#         data = {
#             'title': 'Updated Note',
#             'content': 'Updated content',
#             'group': self.group.id,
#             'tags': [self.tag.id],
#             'expiration_date': '2024-09-20T05:11:09.432Z'
#         }
#         response = self.client.put(f'/api/notes/{self.note.id}', json=data)
#         self.assertEqual(response.status_code, 200)
#         self.note.refresh_from_db()
#         self.assertEqual(self.note.title, 'Updated Note')

#     def test_delete_note(self):
#         response = self.client.delete(f'/api/notes/{self.note.id}')
#         self.assertEqual(response.status_code, 200)
#         self.assertFalse(Note.objects.filter(id=self.note.id).exists())
