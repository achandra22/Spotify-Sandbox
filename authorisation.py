import requests
import datetime
import base64
from secrets import client_id, client_secret

class SpotifyAuthorisation:
    def __init__(self):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.token_expires = datetime.datetime.now()
        self.did_expire = True


    def authorise(self):
        query = 'https://accounts.spotify.com/api/token'
        request_body = {
            "grant_type": "client_credentials"
        }
        client_creds = f"{self.client_id}:{self.client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        response = requests.post(
            query,
            data=request_body,
            headers={"Authorization": f"Basic {client_creds_b64.decode()}"}
        )
        # print(response.status_code)
        # print(response.json())

        if response.status_code in range(200, 299): #check whether request was valid
            token_response_data = response.json()
            now = datetime.datetime.now()
            self.access_token = token_response_data['access_token']
            self.expires_in = token_response_data['expires_in'] # seconds
            expires = now + datetime.timedelta(seconds=self.expires_in)
            self.did_expire = expires < now

    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires <= now:
            self.authorise()
            return self.get_access_token()
        elif token == None:
            self.perform_auth()
            return self.get_access_token() 
        return token

if __name__ == '__main__':
    sa = SpotifyAuthorisation()
    sa.authorise()


# Make sure to fill in your spotify client_secret information
# spotify_token = "BQC2rXOFN1nhwfWEmf9PTN_gKYzdDNSeIBmq1quLnCUWk3WpxC3HSiNjaV2FsmTCRPq1nM062jE8aEXE44RXNtXAVeJFw2xcibA1cLdobG674zg9DOYqjx5_qw26EpjKPt--8-74UYkxWApb95vTpjs8k-3GDnWzlzvmqfn32zsSEczaGPVamIpmIen0E4mzMmHHPdAHeklIJr0Xz-8sLZWH2SJyvorAOSzgEhNV6bhg0oI9dj3_6jFqIhf3mnylT6H9FRmg6ygecoVT"
# spotify_user_id = "dotti22"

#TO-DO need to fix token 

# Necessary Scopes
# - playlist-modify-public
# - playlist-modify-private
# - user-library-read

#Can generate OAuth Token from here: https://developer.spotify.com/console/post-playlists/