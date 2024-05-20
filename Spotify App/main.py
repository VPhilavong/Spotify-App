from auth import get_token, get_auth_header
import json
import os
from requests import get
import requests 

def search(query, search_type="artist"):
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




def get_song_recommendations(token, seed_artist, seed_tracks, limit=20, market="US", seed_genres="rap", target_danceability=0.1):
    headers = get_auth_header(token)
    url = "https://api.spotify.com/v1/recommendations"

    query = f'{url}limit={limit}&market={market}&seed_genres={seed_genres}&target_danceability={target_danceability}'
    query += f'&seed_tracks={",".join(seed_tracks)}'
    query += f'&seed_artist={",".join(seed_artist)}'

    params = {
        "seed_tracks": ",".join(seed_tracks),
        "seed_artist": ",".join(seed_artist),
        "limit": limit,
        "market": market,
        "seed_genres": seed_genres,
        "target_danceability": target_danceability
    }
    


    # Debug prints to see what is being sent to the API
    print("\nError handling to see what the ennnnnnrror is.")
    print(f"URL: {url}")
    print(f"Headers: {headers}")
    print(f"Params: {params}")

    response = requests.get(url, headers=headers, params=params)
    json_response = response.json()

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
        print(f"\nFailed to retrieve recommendations: {json_response}")
        return []

token = get_token()
artist_result = search_for_artist(token, "Drake ")

if artist_result:
    print(artist_result["name"])
    artist_id = artist_result["id"]
    songs = get_songs_by_artist(token, artist_id)
    
    print(f"{artist_result['name']}")
    for idx, song in enumerate(songs):
        print(f"{idx + 1}. {song['name']}")

    # Get song recommendations based on the artist's top tracks

    seed_tracks = [song["id"] for song in songs]
    print(f"Seeeeeeeed Tracks: {seed_tracks}")
    
    seed_artist = [artist_id]

    recommendations = get_song_recommendations(token, seed_artist, seed_tracks, limit=5, market="US", seed_genres="rap", target_danceability=0.1)
    
