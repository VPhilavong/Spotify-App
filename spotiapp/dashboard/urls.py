from django.urls import path
from . import views
from spotify.views import auth_url, spotify_callback, logout

urlpatterns = [
    path('spotify/login/', auth_url, name='spotify_login'),
    path('spotify/callback/', spotify_callback, name='spotify_callback'),
    path('spotify/logout/', logout, name='spotify_logout'),
    path('top_artists/', views.top_artists, name='top_artists'),
    path('top_tracks/', views.top_tracks, name='top_tracks'),
    path('top_genres/', views.top_genres, name='top_genres'),
    path('recently_played/', views.recently_played, name='recently_played'),
    path('test/', views.test, name='test'),
    path('', views.login, name='login'),
]