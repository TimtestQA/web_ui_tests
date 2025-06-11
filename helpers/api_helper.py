import os
import requests
from dotenv import load_dotenv

load_dotenv()

class APIHelper:

    ENDPOINT = "http://qa-playground-social.com/api/v2.0"

    def __init__(self):
        self.headers = {}
        self.params = {
            "api_key_token": os.getenv("API_KEY_TOKEN"),
        }

    def get_user_by_guid(self, guid):
        url = f"{self.ENDPOINT}/user_details"
        self.params["guid"] = guid
        response = requests.get(url, headers=self.headers, params=self.params)
        return response.json()

    def delete_user_by_guid(self, guid):
        url = f"{self.ENDPOINT}/delete/user"
        self.params["guid"] = guid
        response = requests.post(url, headers=self.headers, params=self.params)
        return response.json()