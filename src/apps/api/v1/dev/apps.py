from django.apps import AppConfig
import threading
from .ping import ping_server

class DevAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.api.v1.dev'

    def ready(self):

        # Запускаем поток для пинга сервера
        ping_thread = threading.Thread(target=ping_server)
        ping_thread.daemon = True  # Позволяет завершить поток при завершении основного приложения
        ping_thread.start()