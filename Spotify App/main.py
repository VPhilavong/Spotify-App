from auth import get_token, get_auth_header
import json
import os
from requests import get
import requests 


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

#borrowed from github
def get_metadata(token, query, search_type="track"):
    response = search_for_artist(token, artist_name)
    all = []
    for i in range(len(response['tracks']['items'])):
        track_name = response['tracks']['items'][i]['name']
        track_id = response['tracks']['items'][i]['id']
        artist_name = response['tracks']['items'][i]['artists'][0]['name']
        artist_id = response['tracks']['items'][i]['artists'][0]['id']
        album_name = response['tracks']['items'][i]['album']['name']
        images = response['tracks']['items'][i]['album']['images'][0]['url']

        raw = [track_name, track_id, artist_name, artist_id, images]

    
    
    return all

def get_song_recommendations(token, seed_tracks, limit=10, market="US", seed_genres="rap", target_danceability=0.1):
    url = "https://api.spotify.com/v1/recommendations"
    headers = get_auth_header(token)
    params = {
        "seed_tracks": ",".join(seed_tracks),
        "limit": limit,
        "market": market,
        "seed_genres": seed_genres,
        "target_danceability": target_danceability
    }

    # Debug prints to see what is being sent to the API
    print("\nError handling to see what the error is.")
    print(f"URL: {url}")
    print(f"Headers: {headers}")
    print(f"Params: {params}")

    response = requests.get(url, headers=headers, params=params)
    json_response = response.json()

    # Debug print to see the raw response from the API
    print(f"Response JSON: {json_response}")

    if response.status_code == 200:
        print("Recommended songs:")
        recommended_songs = []
        for idx, track in enumerate(json_response['tracks']):
            track_name = track['name']
            artist_name = track['artists'][0]['name']
            track_link = track['external_urls']['spotify']
            print(f"{idx + 1}. \"{track_name}\" by {artist_name}")
            recommended_songs.append([track_name, artist_name, track_link])
        return recommended_songs
    else:
        print(f"Failed to retrieve recommendations: {json_response}")
        return []

token = get_token()
artist_result = search_for_artist(token, "Playboi Carti")

if artist_result:
    print(artist_result["name"])
    artist_id = artist_result["id"]
    songs = get_songs_by_artist(token, artist_id)
    
    print(f"{artist_result['name']}")
    for idx, song in enumerate(songs):
        print(f"{idx + 1}. {song['name']}")

    # Get song recommendations based on the artist's top tracks
    seed_tracks = [song["id"] for song in songs]
    print(f"Seed Tracks: {seed_tracks}")

    recommendations = get_song_recommendations(token, seed_tracks, limit=5, market="US", seed_genres="rap", target_danceability=0.1)
    
    if recommendations:
        print("\nRecommended songs:")
        for idx, song in enumerate(recommendations):
            track_name = song[0]
            artist_name = song[1]
            link = song[2]
            print(f"{idx + 1}. \"{track_name}\" by {artist_name}")
            print(f"Link: {link}")