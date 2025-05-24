import time
import requests

class SpotifyTokenManager:
    def __init__(self, client_id, client_secret, refresh_token):
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.access_token = None
        self.token_expires_at = 0

    def get_access_token(self):
        current_time = time.time()
        if self.access_token is None or current_time >= self.token_expires_at:
            self.refresh_access_token()
        return self.access_token

    def refresh_access_token(self):
        url = "https://accounts.spotify.com/api/token"
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            token_info = response.json()
            self.access_token = token_info['access_token']
            expires_in = token_info.get('expires_in', 3600)
            self.token_expires_at = time.time() + expires_in - 60  # Refresh 1 min before expiry
        else:
            raise Exception(f"Failed to refresh token: {response.status_code} {response.text}")

# Usage example:
token_manager = SpotifyTokenManager(client_id='7240f6b32424485991cda36824b43683',
                                    client_secret='cd6fb4f3e2e44d82b99114f41762ef90',
                                    refresh_token='AQDLlMP8c9t9Jha-5MJEb561UaXx1lBajP4nxsnbiyFbskj1osvodiHmVKgx4DzXN466pnoAWkXTwFszROhgrnolMFJTbZnv6iwpAbU5qaS52y80v3Fb5Ez_xnFsM1VjRgU')
access_token = token_manager.get_access_token()

