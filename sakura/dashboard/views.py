from ast import literal_eval

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import request as Request
from django.shortcuts import render

from sakura.bot.BotMics.api import Discord_API
from sakura.server.models import Server

discord_invite = settings.DISCORD_INVITE_LINK
# Create your views here.


@login_required
def dashboard(request: Request):
    print("redirect to dashboard")
    # for servers in Server.objects.all():
        # if servers.admin is not None:
            # if request.user.id in literal_eval(servers.admin):
                # print(request.user.id, request.user)
    # guild_list = []
    guild_list = Discord_API().get_guild_list(request.user.access_token)
    print(guild_list)
    print(Discord_API().check_token(request.user.access_token))
    # for key in guild_list:
        # check = Server.objects.get(server_id=int(key['id']))
        # if check.is_active:
            # key['exists'] = True
        # else:
            # key['exists'] = False

    for servers in Server.objects.all():
        if servers.admin is not None:
            if request.user.id in literal_eval(servers.admin):
                dict(id=str(servers.server_id),
                     name=servers.server_name,
                     icon=servers.avatar,
                     exists=servers.is_active)
        for guild in guild_list:
            if str(servers.server_id
                   ) == guild['id'] and servers.avatar != guild['icon']:
                servers.server_name = guild['name']
                servers.avatar = guild['icon']
                # save data in datavase
                servers.save()
                # guild_list.append(temp_server)
    return render(
        request, 'new_dashboard.html', {
            'username': request.user,
            'guild_list': guild_list,
            'invite_url': discord_invite
        })
