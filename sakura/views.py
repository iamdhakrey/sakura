from django.contrib.auth.decorators import login_required
from sakura.BotMics.api import Discord_API
from django.http import request as Request
from django.shortcuts import render

# Create your views here.
@login_required
def dashboard(request:Request):
    content = {}
    print(request.user.access_token)
    guild_list = Discord_API().get_guild_list(request.user.access_token)
    print(guild_list)
    return render(request,'channels.html',{'username':request.user,'guild_list':guild_list})
