from django.test import TestCase
from django.conf import settings

class SettingsTest(TestCase):
    def test_settings_configured(self):
        self.assertTrue(settings.configured)
        self.assertEqual(settings.NINJA_PAGINATION_CLASS, 'ninja.pagination.PageNumberPagination')