import requests
import datetime
import base64
from secrets import client_id, client_secret

class SpotifyAuthorisation:
    def __init__(self):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.token_expiry = datetime.datetime.now()
        self.did_expire = True

    def authorise(self):
        query = 'https://accounts.spotify.com/api/token'
        request_body = {
            "grant_type": "client_credentials"
        }

        '''
        Header Parameter (from Spotify API docs)
        Base 64 encoded string that contains the client ID and client secret key. 
        The field must have the format: Authorization: Basic <base64 encoded client_id:client_secret>
        '''
        client_creds = f"{self.client_id}:{self.client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        response = requests.post(
            query,
            data=request_body,
            headers={"Authorization": f"Basic {client_creds_b64.decode()}"}
        )

        #check whether request was valid
        if response.status_code in range(200, 299): 
            token_response_data = response.json()
            now = datetime.datetime.now()
            self.access_token = token_response_data['access_token']
            expires_in = token_response_data['expires_in'] # seconds
            expiry = now + datetime.timedelta(seconds=expires_in)
            self.token_expiry = expiry
            self.did_expire = expiry < now
            return True #successfully performed authorisation

        return False #authorisation was unsuccessful

    def get_access_token(self):
        token = self.access_token
        now = datetime.datetime.now()
        if self.token_expiry < now:
            self.authorise()
            return self.get_access_token()
        elif token == None:
            self.authorise()
            return self.get_access_token() 
        return token

if __name__ == '__main__':
    sa = SpotifyAuthorisation()
    token = sa.get_access_token()
    print(token)
