from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from spotify.util import get_user_tokens
from django.templatetags.static import static
import matplotlib.pyplot as plt
import io
import base64
import urllib.parse
import requests




# Create your views here.
def login(request):
    return render(request, 'login.html')

def recently_played(request, limit = 20):
    access_token = get_user_tokens(request.session.session_key).access_token
    profile_picture_url = get_user_profile_picture_url(request)

    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'limit': limit}

    # Get recently played tracks
    recently_played_response = requests.get('https://api.spotify.com/v1/me/player/recently-played', headers=headers, params=params)
    recently_played_tracks = recently_played_response.json() if recently_played_response.status_code == 200 else None

    # Get currently playing track
    currently_playing_response = requests.get('https://api.spotify.com/v1/me/player/currently-playing', headers=headers, params=params)
    currently_playing_track = currently_playing_response.json() if currently_playing_response.status_code == 200 else None

    context = {
        'recently_played_tracks': recently_played_tracks,
        'currently_playing_track': currently_playing_track,
        'profile_picture_url': profile_picture_url
    }

    return render(request, 'recently_played.html', context)

def top_tracks(request, limit=50):
    access_token = get_user_tokens(request.session.session_key).access_token

    time_range = request.GET.get('time_range', 'short_term')
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'limit': limit, 'time_range': time_range}
    response = requests.get('https://api.spotify.com/v1/me/top/tracks', headers=headers, params=params)
    
    if response.status_code == 200:
        top_artists = response.json()
        return render(request, 'top_tracks.html', {'top_tracks': top_artists, 'time_range': time_range, 'profile_picture_url': get_user_profile_picture_url(request)})
    else:
        return render(request, 'top_tracks.html', {'error': 'Failed to retrieve top artists'})

def top_artists(request, limit=50):
    access_token = get_user_tokens(request.session.session_key).access_token
    profile_picture_url = get_user_profile_picture_url(request)

    time_range = request.GET.get('time_range', 'short_term')
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'limit': limit, 'time_range': time_range}
    response = requests.get('https://api.spotify.com/v1/me/top/artists', headers=headers, params=params)
    
    if response.status_code == 200:
        top_artists = response.json()
        return render(request, 'top_artists.html', {'top_artists': top_artists, 'time_range': time_range, 'profile_picture_url': get_user_profile_picture_url(request)})
    else:
        return render(request, 'top_artists.html', {'error': 'Failed to retrieve top artists'})
    
def top_genres(request):
    access_token = get_user_tokens(request.session.session_key).access_token
    profile_picture_url = get_user_profile_picture_url(request)

    timerange = request.GET.get('time_range', 'short_term')
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'time_range': timerange}
    response = requests.get('https://api.spotify.com/v1/me/top/artists', headers=headers, params=params)
    
    if response.status_code == 200:
        top_artists = response.json()
        genre_count = {}
        
        for artist in top_artists['items']:
            for genre in artist['genres']:
                if genre in genre_count:
                    genre_count[genre] += 1
                else:
                    genre_count[genre] = 1
        
        # Sort genres by count and take the top 10
        sorted_genres = sorted(genre_count.items(), key=lambda item: item[1], reverse=True)[:10]
        
        if len(sorted_genres) == 0:
            return render(request, 'top_genres.html', {'error': 'No genres found'})
        genres, counts = zip(*sorted_genres)
        
        fig, ax = plt.subplots()
        fig.set_facecolor('#F5F5F5')
        ax.set_facecolor('#F5F5F5')
        ax.pie(counts, labels=genres, autopct='%1.1f%%', startangle=90,)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())
        uri = 'data:image/png;base64,' + urllib.parse.quote(string)
        
        print(sorted_genres)
        return render(request, 'top_genres.html', {'pie_chart': uri, 'time_range': timerange, 'top_genres': sorted_genres, 'profile_picture_url': get_user_profile_picture_url(request)})
    else:
         return render(request, 'top_genres.html', {'error': 'Failed to retrieve top genres'})

def get_user_profile_picture_url(request):
    access_token = get_user_tokens(request.session.session_key).access_token  # Ensure access token retrieval is correct
    if not access_token:
        return None

    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get('https://api.spotify.com/v1/me', headers=headers)

    if response.status_code == 200:
        user_data = response.json()
        return user_data['images'][0]['url'] if user_data['images'] else static('images/default.png')
    else:
        print(f"Failed to retrieve user profile: {response.status_code} - {response.text}")
        return None


def test(request):
    return HttpResponse('Test page')