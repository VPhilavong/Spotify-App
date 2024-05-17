from auth import get_token, get_auth_header
import json
import os
from requests import post, get


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

def get_song_recommendations(limit=10, seed_tracks='', market="US", seed_genres="rap", target_danceability=0.1):
    url = "https://api.spotify.com/v1/recommendations"
    headers = get_auth_header(token)
    params = {
        "seed_tracks": ",".join(seed_tracks),
        "limit": limit,
        "market": market,
        "seed_generes": seed_genres,
        "target_danceability": target_danceability
    }
    result = get(url, headers=headers, params=params)
    json_result = json.loads()
    return json_result

token = get_token()
artist_result = search_for_artist(token, "Playboi Carti")

if artist_result:
    print(artist_result["name"])
    artist_id = artist_result["id"]
    songs = get_songs_by_artist(token, artist_id)
    
    for idx, song in enumerate(songs):
        print(f"{idx + 1}. {song['name']}")

 # Get song recommendations based on the artist's top tracks
    seed_tracks = [song["id"] for song in songs]
    recommendations = get_song_recommendations(limit=10, seed_tracks='', market="US", seed_genres="rap", target_danceability=0.1)
    print("\nRecommendations:")
    for idx, song in enumerate(recommendations):
        artists = ", ".join([artist["name"] for artist in song["artists"]])
        print(f"{idx + 1}. {song['name']} by {artists}")
