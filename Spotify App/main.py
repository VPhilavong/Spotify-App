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
token = get_token()
artist_result = search_for_artist(token, "Queen")
if artist_result:
    print(artist_result["name"])
artist_id = artist_result["id"]
songs = get_songs_by_artist(token, artist_id)
print(songs)


for idx, song in enumerate(songs):
    print(f"{idx + 1}. {song['name']}")