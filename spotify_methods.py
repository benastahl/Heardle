import requests
import base64
import time
import os

from dotenv import load_dotenv, find_dotenv

if not os.getenv("PUBLIC_ACTIVATED"):
    assert load_dotenv(find_dotenv()), "Failed to load environment."

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URI")
client_authorization_header = {
    "origin": "https://developer.spotify.com",
    "referer": "https://developer.spotify.com/",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": f"Basic {base64.b64encode(f'{client_id}:{client_secret}'.encode('utf8')).decode('utf8')}"
}

class SpotifyUser:
    def __init__(self, refresh_token=None, access_token=None, auth_code=None):
        self.s = requests.session()

        self.refresh_token = refresh_token
        self.access_token = access_token
        if auth_code:
            self.generate_tokens(auth_code)
        if not self.access_token:
            self.refresh_authorization_token()
        self.api_auth_headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

    def generate_tokens(self, auth_code):
        print("Generating tokens...")
        getTokensDATA = {
            "URL": "https://accounts.spotify.com/api/token",
            "PARAMS": {
                "code": auth_code,
                "grant_type": "authorization_code",
                "redirect_uri": redirect_uri
            }
        }
        print(getTokensDATA)
        getTokensPOST = self.s.post(
            getTokensDATA["URL"],
            params=getTokensDATA["PARAMS"],
            headers=client_authorization_header
        )
        print(client_authorization_header)
        if getTokensPOST.status_code not in [201, 200]:
            print(f"Generation not successful. ({getTokensPOST.status_code})")
            exit(1)
        self.refresh_token = getTokensPOST.json()['refresh_token']
        self.access_token = getTokensPOST.json()['access_token']

    def refresh_authorization_token(self):
        print("Refreshing auth token...")
        getAuthorizationTokenDATA = {
            "URL": "https://accounts.spotify.com/api/token",
            "PARAMS": {
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token,
            }
        }
        getAuthorizationTokenPOST = self.s.post(
            getAuthorizationTokenDATA["URL"],
            params=getAuthorizationTokenDATA["PARAMS"],
            headers=client_authorization_header
        )
        if getAuthorizationTokenPOST.status_code not in [201, 200]:
            print(getAuthorizationTokenPOST.text)
            print(f"Refresh not successful. ({getAuthorizationTokenPOST.status_code})")
            exit(1)
        self.access_token = getAuthorizationTokenPOST.json()['access_token']
        self.api_auth_headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

    def toggle_playback(self, track_id):
        self.refresh_authorization_token()
        devices = self.collect("/me/player/devices").json()['devices']
        device_id = devices[0]['id']
        print(devices)
        while True:
            print("Toggling playback...")
            playback_payload = {
                "uris": [f"spotify:track:{track_id}"],
                "position_ms": 0
            }

            REQ = self.s.put(
                url=f"https://api.spotify.com/v1/me/player/play",
                json=playback_payload,
                headers=self.api_auth_headers
            )
            print(REQ.json())
            if REQ.status_code == 401:
                self.refresh_authorization_token()
                time.sleep(3)
                continue
            break

    def collect(self, path, **params):
        while True:
            print(f"Requesting: '{path}'...")
            REQ = self.s.get(
                url=f"https://api.spotify.com/v1{path}",
                params=params,
                headers=self.api_auth_headers
            )
            if REQ.status_code == 401:
                self.refresh_authorization_token()
                time.sleep(3)
                continue

            return REQ

