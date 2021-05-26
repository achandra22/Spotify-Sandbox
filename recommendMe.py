import json
import datetime, time
import requests
from secrets import spotify_user_id, spotify_token

class PlaylistRecommender:
    def __init__(self):
        self.user_id = spotify_user_id
        self.token = spotify_token
    
    def searchItems(self, query, type):
        query = f'https://api.spotify.com/v1/search?q={query}&type={type}&limit=1'
        response = requests.get(
            query, 
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.token}'
            }
        )
        print(response.status_code)
        responseJSON = response.json()
        return responseJSON[type+'s']['items'][0].get('id')

    def getRecommendations(self, artists, tracks, length, danceability, popularity):
        seed_artists = ','.join(artists)
        seed_tracks = ','.join(tracks)
        seed_genres = 'Pop'
        print(seed_tracks)
        print(seed_artists)
        print(length, danceability, popularity)
        query = f'https://api.spotify.com/v1/recommendations?seed_artists={seed_artists}&seed_tracks={seed_tracks}&seed_genres={seed_genres}&limit={length}&target_danceability={danceability}&target_popularity={popularity}'
        response = requests.get(
            query, 
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.token}'
            }
        )
        print(response.status_code)
        #print(response.json())
        response_json = response.json()
        return response_json['tracks']


    def createPlaylist(self):
        now = datetime.datetime.now()
        request_body = json.dumps({
            "name": str(now.date()),
            "description": "The music mood of " + str(now.date()),
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
    def addToPlaylist(self, seed_artists, seed_tracks, length, danceability, popularity):
        playlistID = self.createPlaylist()
        tracks = self.getRecommendations(seed_artists, seed_tracks, length, danceability, popularity)
        request_body = json.dumps({
            "uris": self.extractURI(tracks),
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
        print(response.status_code)
        response_json = response.json()

    def extractURI(self, tracks):
        uris = []
        #print(items[0][])
        for s in tracks:
            #print(s)
            uris.append(s.get('uri'))
        return uris



if __name__ == '__main__':
    
    pr = PlaylistRecommender()
    print("Can't decide what to play? Let's make a playlist based on some music that you've been loving")
    print("Please enter up to four artists and tracks as inspiration.")
    seed_artists = [] #artists used to seed the recommendations
    seed_tracks = [] #tracks used to seed the recommendations
    for i in range(4):
        choice = input("Is this an Artist (a), Track (t) or are you Finished (f)?\n")
        if choice == 'f':
            break
        elif choice == 'a':
            value = input("Great! What is the name of this artist? ")
            type = 'artist' if choice == 'a' else 'track'
            id = pr.searchItems(value, 'artist')
            seed_artists.append(id)
            i += 1
        elif choice == 't':
            value = input("Great! What is the name of this track? ")
            id = pr.searchItems(value, 'track')
            seed_tracks.append(id)
            i += 1
        else:
            print("Please type either 'a'(rtist), 't'(rack) or 'f'(inish) to make a decision")
            time.sleep(2)
    
    #Getting recommendation parameters 
    length = int(input("How long would you like the playlist to be (in minutues)? "))
    danceability = input("Are the vibes more chill (0) or party (1) (Enter a number between 0 and 1)? ")
    popularity = input("Finally, are you after some quirky tunes (0) or bangers that everyone knows (100) (Enter a number between 0 and 100)? ")
    pr.addToPlaylist(seed_artists, seed_tracks, length//3, danceability, popularity)