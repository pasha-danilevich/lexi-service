import requests
import time
from config.settings import SERVER_DOMAIN

import requests
import time
import threading

# Флаг для отслеживания состояния
is_pinging = False

def ping_server():
    global is_pinging
    while True:
        if not is_pinging:
            is_pinging = True  # Устанавливаем флаг, чтобы предотвратить повторный запуск
            try:
                response = requests.get(f'http://{SERVER_DOMAIN}/api/dev/ping/')
                print(f'Ping response status code: {response.status_code}')
            except Exception as e:
                print(f'Error pinging server: {e}')
            finally:
                is_pinging = False  # Сбрасываем флаг после завершения запроса

        time.sleep(400)  # Ждем 400 секунд перед следующим запросом