from django.http.response import JsonResponse
from sakura.models import Server, WelcomeData
from django.contrib.auth.decorators import login_required
from sakura.BotMics.api import Discord_API
from django.http import request as Request
from django.shortcuts import render
from ast import literal_eval

from django.conf import settings

discord_invite=settings.DISCORD_INVITE_LINK
# Create your views here.
@login_required
def dashboard(request:Request):
    content = {}
    for servers in Server.objects.all():
        if servers.admin is not None:
            if request.user.id in  literal_eval(servers.admin):
                print(request.user.id)
    guild_list = []
    guild_list = Discord_API().get_guild_list(request.user.access_token)
    for key in guild_list:
        check = Server.objects.get(server_id=int(key['id']))
        if check.is_active:
            key['exists'] = True
        else:
            key['exists'] = False
    print(guild_list)
    for servers in Server.objects.all():
        if servers.admin is not None:
            if request.user.id in  literal_eval(servers.admin):
                temp_server = dict (
                    id = str(servers.server_id),
                    name = servers.server_name,
                    icon = servers.avatar,
                    exists = servers.is_active
                )
                guild_list.append(temp_server)
    return render(request,'new_dashboard.html',{'username':request.user,'guild_list':guild_list,'invite_url':discord_invite})

@login_required(redirect_field_name="login")
def server(request,pk):
    if request.user.is_authenticated:
        guild = Server.objects.get(server_id=pk,)
        print(guild.avatar)
        return render(request,'new_base.html',{'guild':guild})


def welcome(request:Request,pk):
    if request.user.is_authenticated:
        if request.method =="POST":
            # print(request.POST)
            post_context = {}
            welcome = WelcomeData.objects.get(server_id = int(pk))
            if request.POST.get("welcome_channel",None) is not None:
                welcome.welcome_channel =request.POST.get('welcome_channel')
            if request.POST.get("welcome_enable",None) is not None:
                if request.POST.get('welcome_enable') == "Enable":
                    welcome.welcome_enable = True
                else:
                    welcome.welcome_enable = False
                # welcome.welcome_enable =request.POST.get('welcome_enable')
            if request.POST.get("welcome_message",None) is not None:
                welcome.welcome_msg = request.POST.get('welcome_message')
            if request.POST.get("welcome_role",None) is not None:
                welcome.self_role =request.POST.get('welcome_role')
            if request.POST.get("welcome_channel",None) is not None:
                __image_link = request.POST.get('welcome_images')
                for image in __image_link:
                    if image == "":
                        __image_link.remove(image)
                if len(__image_link) > 6:
                    __image_link = __image_link[0:4]
                
                welcome.save()

            # WelcomeData.save()
            

            

        text_channel = []
        context= {}
        data = Discord_API()

        sata = data.get_guild_channel(settings.TOKEN,id=pk)
        roles = data.get_guild_roles(settings.TOKEN,id=pk)
        welcome_data = WelcomeData.objects.get(server_id=pk)
        guild = Server.objects.get(server_id=pk,)
        context = dict(
            welcome = welcome_data,
            guild = guild
        )
        welcome_channel = {}
        for i in sata:
            # print((type(i['type'])))
            if i['type'] == 0:

                text_channel.append(i)
                if int(welcome_data.welcome_channel) == int(i['id']):
                    welcome_channel['id'] = i['id'] 
                    welcome_channel['name'] = i['name'] 
        for role in roles:
            if int(welcome_data.self_role) == int(role['id']):
                welcome_channel['role_id'] = role['id']
                welcome_channel['role_name'] = role['name']
        context = dict(
            welcome = welcome_data,
            guild = guild,
            text_channel =text_channel,
            roles = roles,
            welcome_channel = welcome_channel
        )
        # return JsonResponse(roles,safe=False)
        return render(request,'welcome.html',context) 
