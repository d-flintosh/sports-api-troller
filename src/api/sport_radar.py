import json
import re
import time

import requests
from google.cloud import secretmanager_v1
from google.cloud.secretmanager_v1 import AccessSecretVersionRequest

BASE_URL = 'http://api.sportradar.us/'


class SportRadarApi:
    def __init__(self):
        client = secretmanager_v1.SecretManagerServiceClient()
        secret_request = AccessSecretVersionRequest({
            'name': 'projects/557888643787/secrets/sport-radar/versions/latest'
        })
        secret = client.access_secret_version(request=secret_request)

        self.api_keys = json.loads(secret.payload.data.decode('UTF-8'))

    def make_request(self, url: str) -> dict:
        url_parts = re.findall('(\w+)://([\w\-\.]+)/(\w+).(\w+)', url)
        league = url_parts[0][2]
        api_key = self.api_keys.get(league)
        full_url = url + f'?api_key={api_key}'
        time.sleep(1)
        response = requests.get(full_url)
        return json.loads(response.content)
