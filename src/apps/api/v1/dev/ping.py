import requests
import time
from config.settings import SERVER_DOMAIN

def ping_server():
    while True:
        
        response = requests.get(f'http://{SERVER_DOMAIN}/api/dev/ping/')
        print(f'Ping response status code: {response.status_code}')
        
        time.sleep(20)  # 1 минута
      