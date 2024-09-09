from django.shortcuts import render, redirect
from django.conf import settings
from requests import Request, post
import requests
from .util import update_tokens, get_user_tokens


CLIENT_ID = settings.SPOTIFY_CLIENT_ID
CLIENT_SECRET = settings.SPOTIFY_CLIENT_SECRET
REDIRECT_URI =  settings.SPOTIFY_REDIRECT_URI

# Create your views here.
def auth_url(request):
    scopes = 'user-top-read user-library-read user-read-recently-played'
    url = Request('GET', 'https://accounts.spotify.com/authorize', params={
            'scope': scopes,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID
        }).prepare().url
    return redirect(url)

def spotify_callback(request, format=None):
    code = request.GET.get('code')
    error = request.GET.get('error')

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')
    
    if expires_in is None:
        expires_in = 3600
    
    if not request.session.exists(request.session.session_key):
        request.session.create()

    update_tokens(
        request.session.session_key, access_token, token_type, expires_in, refresh_token)

    return redirect('test')

def logout(request):
    request.session.flush()
    return redirect('login')