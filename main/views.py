from logging import setLoggerClass
from django.shortcuts import redirect, render

from django.conf import settings

discord_invite = settings.DISCORD_INVITE_LINK

def home(request):
    if request.user.is_authenticated:
        print(discord_invite)
        avatar_url = None
        return redirect('dashboard')
    avatar_url = None
    return render(request,'base.html',{'user':request.user,'avatar_url':avatar_url,"invite_url":discord_invite})

def new_home(request):
    if request.user.is_authenticated:
        print(discord_invite)
        avatar_url = None
        return redirect('dashboard')
    else:
        return render(request,'new_base.html',{'user':request.user,'avatar_url':None,"invite_url":discord_invite})
