from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('spotify/login/', views.spotify_login, name='spotify_login'),
    path('spotify/callback/', views.spotify_callback, name='spotify_callback'),
    path('logout/', views.logout, name='logout'),
    path('top_artists/', views.top_artists, name='top_artists'),
    path('top_genres/', views.top_genres, name='top_genres'),
]