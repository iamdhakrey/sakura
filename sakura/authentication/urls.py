from django.contrib import admin
from django.urls import path

from .views import discord_login, discord_login_redirect, discord_logout, get_authenticate_user, home

urlpatterns = [
    path('',home,name='home'),
    path('login',discord_login,name='auth'),
    path('logout',discord_logout,name='logout'),
    path('user',get_authenticate_user,name='get_authenticate_user'),
    path('login/redirect',discord_login_redirect,name='discord_login_redirect'),
]
