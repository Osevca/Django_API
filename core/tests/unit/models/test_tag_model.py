import pytest
from core.models import Tag

@pytest.mark.django_db
class TestTagModel:
    def test_create_tag(self):
        tag = Tag.objects.create(name='Test Tag')
        assert tag.name == 'Test Tag'

    def test_tag_str(self):
        tag = Tag.objects.create(name='Test Tag')
        assert str(tag) == 'Test Tag'