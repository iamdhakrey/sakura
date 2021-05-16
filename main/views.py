from logging import setLoggerClass
from django.shortcuts import render

from django.conf import settings

discord_invite = settings.DISCORD_INVITE_LINK

def home(request):
    avatar_url = None
    return render(request,'base.html',{'user':request.user,'avatar_url':avatar_url,"invite_url":discord_invite})