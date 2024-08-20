from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('spotify/login/', views.spotify_login, name='spotify_login'),
    path('spotify/callback/', views.spotify_callback, name='spotify_callback'),
    #test
    path('test_spotify_api/', views.test_spotify_api, name='test_spotify_api'),
]