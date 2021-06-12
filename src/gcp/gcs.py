import json

from google.cloud.storage import Client


class Gcs:
    def __init__(self):
        self.client = Client(project='sports-data-service')
        self.bucket = self.client.get_bucket('college-by-player')

    def read_as_dict(self, url: str) -> dict:
        blob = self.bucket.get_blob(url)
        contents = blob.download_as_string()
        return json.loads(contents)

    def write(self, url: str, contents: dict):
        blob = self.bucket.blob(url)
        blob.upload_from_string(json.dumps(contents))

