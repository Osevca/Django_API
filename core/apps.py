from django.apps import AppConfig
# from core.signals import *

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        import core.signals
        core.signals.delete_related_objects,
        core.signals.note_created,
        core.signals.log_note_changes,
        core.signals.note_created,
        core.signals.update_user_updated_at,
        core.signals.handle_orphaned_notes
