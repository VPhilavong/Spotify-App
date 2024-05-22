from auth import get_token, get_auth_header
import json
import os
from requests import get
import requests 

class SpotifyAPI:
    def __init__(self, token):
        self._authorization_token = token

    def _place_get_api_request(self, url):
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._authorization_token}"
            }
        )
        return response

    def _place_post_api_request(self, url, data):
        response = requests.post(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._authorization_token}"
            }
        )
        return response

def search(token, query, search_type="artist"):
    access_token = get_auth_header(token)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"

    }
    url = "https://api.spotify.com/v1/search"
    params = {
        "query": query,
        "type": search_type.lower(),
        "limit": 5

    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code in range(200, 299):
        return response.json()
    else: 
        print(f"Response Error: {response.status_code}")
        return response.json()


def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=5"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    
    if len(json_result) == 0:
        print("This dude dont exist")
        return None
    
    return json_result[0]
  

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

def get_meta(self, query, search_type="track"):  # meta data of a track
    resp = self.search(query, search_type)
    all = []
    for i in range(len(resp['tracks']['items'])):
        track_name = resp['tracks']['items'][i]['name']
        track_id = resp['tracks']['items'][i]['id']
        artist_name = resp['tracks']['items'][i]['artists'][0]['name']
        artist_id = resp['tracks']['items'][i]['artists'][0]['id']
        album_name = resp['tracks']['items'][i]['album']['name']
        images = resp['tracks']['items'][i]['album']['images'][0]['url']

        raw = [track_name, track_id, artist_name, artist_id, images]
        all.append(raw)

    return all


def get_song_recommendations(token, seed_artists='', seed_tracks='', limit=20, market="US", seed_genres="rap", target_danceability=0.1):
    access_token = get_auth_header(token)
    endpoint_url = "https://api.spotify.com/v1/recommendations"
    query_params = {
        "limit": limit,
        "market": market,
        "seed_genres": seed_genres,
        "target_danceability": target_danceability,
        "seed_artists": seed_artists,
        "seed_tracks": seed_tracks
    }

    response = requests.get(endpoint_url, headers={
        "Content-type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }, params=query_params)


    # Making the API request

    if response.status_code in range(200, 299):
        json_response = response.json()
        return json_response
    else:
        print(f"API Error: {response.status_code}")
        print(response.content)
        return None

#test shit
token = get_token()
artist_result = search_for_artist(token, "Daniel Caesar")



if artist_result:
    artist_id = artist_result["id"]
    songs = get_songs_by_artist(token, artist_id)
    
    print(f"{artist_result['name']}")
    for idx, song in enumerate(songs):
        print(f"{idx + 1}. {song['name']}")

    # Get song recommendations based on the artist's top tracks
    seed_artists = [artist_id]

    seed_tracks = [song["id"] for song in songs]
    print(f"Seed Track for the artist top 10 and some albums: {seed_tracks}")
    
recommendations = get_song_recommendations(token, seed_artists, seed_tracks, limit=10, market="US", seed_genres="rap", target_danceability=1.0)


if recommendations:
    print(f"Recommended tracks for {artist_result['name']}:")
    for idx, song in enumerate(recommendations["tracks"]):
        print(f"{idx + 1}. {song['name']}")
