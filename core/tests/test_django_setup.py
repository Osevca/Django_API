def test_django_setup():
    from django.conf import settings
    assert settings.configured, "Django settings are not configured"