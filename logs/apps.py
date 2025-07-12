
from django.apps import AppConfig

class LogsConfig(AppConfig):
    name = 'logs'

    def ready(self):
        import logs.signals  # ativa os signals no startup

class LogsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'logs'
