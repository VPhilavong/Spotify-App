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

def top_tracks(request):
    token_info = request.session.get('token_info')
    if not token_info:
        return redirect('spotify_login')

    sp = spotipy.Spotify(auth=token_info['access_token'])
    time_range = request.GET.get('time_range', 'short_term')
    
    top_tracks_data = sp.current_user_top_tracks(limit=50, time_range=time_range)
    top_tracks = top_tracks_data['items']
    
    tracks_info = []
    for index, track in enumerate(top_tracks, start=1):
        track_info = {
            'index': index,
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'image_url': track['album']['images'][0]['url'] if track['album']['images'] else None,
            'spotify_url': track['external_urls']['spotify']
        }
        tracks_info.append(track_info)
    
    return render(request, 'top_tracks.html', {'tracks_info': tracks_info, 'time_range': time_range})

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
    
    top_artists_data = sp.current_user_top_artists(limit=50, time_range=time_range)
    top_artists = top_artists_data['items']
    
    genres = []
    for artist in top_artists:
        genres.extend(artist['genres'])
    
    # Count the occurrences of each genre
    genre_counts = {}
    for genre in genres:
        if genre in genre_counts:
            genre_counts[genre] += 1
        else:
            genre_counts[genre] = 1
    
    # Sort genres by count
    sorted_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)
    top_genres = [genre for genre, count in sorted_genres[:10]]  # Get top 10 genres

    # Generate a pie chart
    labels, sizes = zip(*sorted_genres[:10])
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('#F5F5F5')  # Set the background color of the figure
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Save the plot to a PNG in memory
    buf = io.BytesIO()
    plt.savefig(buf, format='png', facecolor=fig.get_facecolor())  # Save with the background color
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return render(request, 'data_vis.html', {'genres': top_genres, 'image_base64': image_base64, 'time_range': time_range})