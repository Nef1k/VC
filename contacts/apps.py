from django.apps import AppConfig


class ContactsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'contacts'

    def ready(self):
        from contacts import signals  # no qa
