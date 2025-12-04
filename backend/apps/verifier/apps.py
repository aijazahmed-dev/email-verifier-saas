from django.apps import AppConfig


class VerifierConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'verifier'

    def ready(self):
        import verifier.signals
