from sakura.authentication.models import DiscordUser
from sakura.bot.BotMics.api import Discord_API
from sakura.settings import CLIENT_ID, CLIENT_SECRET
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
import requests
from django.conf import settings

from .auth import SakuraAuthenticationBackend
# Create your views here.
auth_url_discord = settings.DISCORD_AUTH_URL


def home(request:HttpResponse) -> JsonResponse:
    return JsonResponse({"msg":'Hello'})

@login_required(login_url='/auth/login')
def get_authenticate_user(request:HttpResponse):
    print(request.user.id)
    return render(request,'index.html')
    # return JsonResponse({"msg":"authenticated"})

def discord_login(request: HttpResponse):
    return redirect(auth_url_discord)

def discord_login_redirect(request:HttpResponse):
    code = request.GET.get('code')
    print(code)
    api = Discord_API()
    user = api.exchange_code(code)
    discord_user = SakuraAuthenticationBackend.authenticate(request=request,user=user)
    print(user['access_token'],"token")
    change= DiscordUser.objects.get(pk=user['id'])
    print(change)
    change.access_token = user['access_token']
    change.save()
    discord_user = list(discord_user).pop()
    print("discord_user",discord_user)
    login(request,discord_user,backend='sakura.authentication.auth.SakuraAuthenticationBackend')
    return redirect('dashboard')

def discord_logout(request:HttpResponse):
    logout(request)
    return redirect('home')
