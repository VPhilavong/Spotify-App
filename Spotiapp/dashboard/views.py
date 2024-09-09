from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from spotify.util import get_user_tokens
import requests




# Create your views here.
def login(request):
    return render(request, 'login.html')

def recently_played(request):
    return render(request, 'recently_played.html')

def top_tracks(request, limit=50):
    access_token = get_user_tokens(request.session.session_key).access_token
    
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'limit': limit}
    response = requests.get('https://api.spotify.com/v1/me/top/tracks', headers=headers, params=params)
    time_range = request.GET.get('time_range', 'medium_term')
    
    if response.status_code == 200:
        top_artists = response.json()
        return render(request, 'top_tracks.html', {'top_tracks': top_artists, 'time_range': time_range})
    else:
        return render(request, 'top_tracks.html', {'error': 'Failed to retrieve top artists'})

def top_artists(request, limit=50):
    access_token = get_user_tokens(request.session.session_key).access_token
    
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'limit': limit}
    response = requests.get('https://api.spotify.com/v1/me/top/artists', headers=headers, params=params)
    time_range = request.GET.get('time_range', 'medium_term')
    
    if response.status_code == 200:
        top_artists = response.json()
        return render(request, 'top_artists.html', {'top_artists': top_artists, 'time_range': time_range})
    else:
        return render(request, 'top_artists.html', {'error': 'Failed to retrieve top artists'})
    
def top_genres(request):
    return render(request, 'top_genres.html')

def test(request):
    return HttpResponse('Test page')