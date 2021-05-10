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
    user = exchange_code(code)
    discord_user = SakuraAuthenticationBackend.authenticate(request=request,user=user)
    discord_user = list(discord_user).pop()
    print(discord_user)
    login(request,discord_user,backend='sakuralogin.auth.SakuraAuthenticationBackend')
    return redirect('/auth/user')

def discord_logout(request:HttpResponse):
    logout(request)
    return redirect('home')


def exchange_code(code:str):
    data = {
        "client_id":"840573842958450719",
        "client_secret":"-d8OTn0UHko45Gl5aMcoE-3ITLsjpuUP",
        "grant_type":"authorization_code",
        "code":code,
        "redirect_uri":"http://127.0.0.1:8000/auth/login/redirect",
        'scope':'identify'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post('https://discord.com/api/oauth2/token',data=data,headers=headers)

    print(response)
    credentials = response.json()
    print(credentials)

    access_token = credentials['access_token']

    response = requests.get("https://discord.com/api/v8/users/@me",headers={
        'Authorization':"Bearer %s"% access_token
    })

    print(response)
    user = response.json()
    print(user)
    return user