from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings 
from dashboard.models import song_data
from spotiapp.spotify_utils import get_spotify_client, get_spotify_oauth
from spotipy.oauth2 import SpotifyOAuth
import spotipy

# Create your views here.
def home(request):
    return render(request, 'first.html')

# Spotify login and callback
def get_spotify_oauth():
    return SpotifyOAuth(
        client_id=settings.SPOTIFY_CLIENT_ID,
        client_secret=settings.SPOTIFY_CLIENT_SECRET,
        redirect_uri=settings.SPOTIFY_REDIRECT_URI,
        scope="user-top-read user-library-read"
    )

def spotify_login(request):
    auth_url = get_spotify_client()
    if isinstance(auth_url, str):
        return redirect(auth_url)
    return HttpResponse("Spotify client is ready")

def spotify_callback(request):
    sp_oauth = get_spotify_oauth()
    code = request.GET.get('code')
    token_info = sp_oauth.get_access_token(code)
    sp = spotipy.Spotify(auth=token_info['access_token'])
    results = sp.current_user_saved_tracks()
    return JsonResponse(results)

# Test
def test_spotify_api(request):
    sp_oauth = get_spotify_oauth()
    code = request.GET.get('code')
    token_info = sp_oauth.get_access_token(code)
    sp = spotipy.Spotify(auth=token_info['access_token'])
    # Example API call to get the current user's profile
    top_artists = sp.current_user_saved_albums()
    
    return JsonResponse(top_artists)