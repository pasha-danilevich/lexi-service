from django.apps import AppConfig
import threading
from .ping import ping_server

class DevAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.api.v1.dev'

    def ready(self):
        # Запускаем поток для пинга сервера только один раз
        if not hasattr(self, 'ping_thread'):
            self.ping_thread = threading.Thread(target=ping_server)
            self.ping_thread.daemon = True
            self.ping_thread.start()
        else:
            print('Второй поток')