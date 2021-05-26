import json
import datetime
import requests
from secrets import spotify_user_id, spotify_token

class CreateAnnualPlaylist:
    def __init__ (self):
        self.user_id = spotify_user_id
        self.token = spotify_token

    def createPlaylist(self):
        now = datetime.datetime.now()
        request_body = json.dumps({
            "name": now.year,
            "description": "The music mood of " + str(now.year),
            "public": False
        })
        query = f"https://api.spotify.com/v1/users/{self.user_id}/playlists"
        response = requests.post(
            query, 
            data=request_body, 
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.token}'
            }
        )

        response_json = response.json()
        try:
            return response_json['id']
        except KeyError:
            print("Please generate a new Auth Token from here: https://developer.spotify.com/console/post-playlists/")

    def getSavedTracks(self):
        query = "https://api.spotify.com/v1/me/tracks?limit=50"
        response = requests.get(
            query,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.token}'
            }
        )
        response_json = response.json()
        return response_json['items']



    def addSavedTracks(self):
        playlistID = self.createPlaylist()
        items = self.getSavedTracks()
        request_body = json.dumps({
            "uris": self.extractTrackID(items, 'uri'),
        })
        query = f'https://api.spotify.com/v1/playlists/{playlistID}/tracks'
        response = requests.post(
            query,
            data=request_body,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.token}'
            }
        )
        response_json = response.json()

    def extractTrackID(self, items, key):
        ids = []
        #print(items[0][])
        for s in items:
            ids.append(s.get('track').get(key))
        return ids

    def removeSavedTracks(self, items):
        request_body = json.dumps({
            "ids": self.extractTrackID(items, 'id'),
        })
        query = 'https://api.spotify.com/v1/me/tracks'
        response = requests.delete(
            query,
            data=request_body, #is it better to send this as a query parameter? 
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.token}'
            }
        )
        print(response.status_code)
        response_json = response.json()
        

if __name__ == '__main__':
    annualPlaylist = CreateAnnualPlaylist()
    annualPlaylist.addSavedTracks()
