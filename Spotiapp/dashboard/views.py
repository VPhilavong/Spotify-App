from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings 
from dashboard.models import song_data
from spotiapp.spotify_utils import get_spotify_client, get_spotify_oauth
from spotipy.oauth2 import SpotifyOAuth
from django.contrib.auth import logout as auth_logout
from collections import Counter
import matplotlib.pyplot as plt
import io
import base64
import spotipy


# Create your views here.
def dashboard(request):
    return render(request, 'dashboard.html')

def login(request):
    return render(request, 'login.html')

# Spotify login and callback
def get_spotify_oauth():
    return SpotifyOAuth(
        client_id=settings.SPOTIFY_CLIENT_ID,
        client_secret=settings.SPOTIFY_CLIENT_SECRET,
        redirect_uri=settings.SPOTIFY_REDIRECT_URI,
        scope="user-top-read user-library-read"
    )

def spotify_login(request):
    sp_oauth = get_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

def spotify_callback(request):
    sp_oauth = get_spotify_oauth()
    code = request.GET.get('code')
    token_info = sp_oauth.get_access_token(code)
    request.session['token_info'] = token_info
    return redirect('dashboard')

def logout(request):
    auth_logout(request)
    return redirect('login')

def top_artists(request):
    token_info = request.session.get('token_info')
    if not token_info:
        return redirect('spotify_login')

    sp = spotipy.Spotify(auth=token_info['access_token'])
    time_range = request.GET.get('time_range', 'short_term')
    top_artists_data = sp.current_user_top_artists(limit=50, time_range=time_range)
    top_artists = top_artists_data['items']

    artists_info = []
    for index, artist in enumerate(top_artists, start=1):
        artist_info = {
            'index': index,
            'name': artist['name'],
            'image_url': artist['images'][0]['url'] if artist['images'] else None,
            'spotify_url': artist['external_urls']['spotify']
        }
        artists_info.append(artist_info)

    return render(request, 'top_artists.html', {'artists_info': artists_info, 'time_range': time_range})

def top_genres(request):
    token_info = request.session.get('token_info')
    if not token_info:
        return redirect('spotify_login')

    sp = spotipy.Spotify(auth=token_info['access_token'])
    time_range = request.GET.get('time_range', 'short_term')
    
    # Fetch top artists
    top_artists_data = sp.current_user_top_artists(limit=50, time_range=time_range)
    top_artists = top_artists_data['items']
    
    # Extract genres
    genres = []
    for artist in top_artists:
        genres.extend(artist['genres'])
    
    # Count genres
    genre_counts = Counter(genres)
    
    # Prepare data for the pie chart
    top_genres = genre_counts.most_common(10)
    labels = [genre for genre, count in top_genres]
    data = [count for genre, count in top_genres]
    
    # Generate the pie chart
    fig, ax = plt.subplots()
    ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Save the plot to a PNG image in memory
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    
    return render(request, 'data_vis.html', {'image_base64': image_base64, 'time_range': time_range})