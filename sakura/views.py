from sakura.decorator import role_required
from django.http.response import JsonResponse
from requests import api
from sakura.models import Server, WelcomeData
from django.contrib.auth.decorators import login_required, permission_required
from sakura.BotMics.api import Discord_API
from django.http import request as Request
from django.shortcuts import redirect, render
from ast import literal_eval
import requests
from io import BytesIO
from PIL import Image, ImageOps

from django.conf import settings

discord_invite = settings.DISCORD_INVITE_LINK
# Create your views here.


@login_required
def dashboard(request: Request):
    print("redirect")
    content = {}
    for servers in Server.objects.all():
        if servers.admin is not None:
            if request.user.id in literal_eval(servers.admin):
                print(request.user.id, request.user)
    guild_list = []
    guild_list = Discord_API().get_guild_list(request.user.access_token)
    for key in guild_list:
        check = Server.objects.get(server_id=int(key['id']))
        if check.is_active:
            key['exists'] = True
        else:
            key['exists'] = False

    for servers in Server.objects.all():
        if servers.admin is not None:
            if request.user.id in literal_eval(servers.admin):
                temp_server = dict(
                    id=str(servers.server_id),
                    name=servers.server_name,
                    icon=servers.avatar,
                    exists=servers.is_active
                )
                guild_list.append(temp_server)
    return render(request, 'new_dashboard.html', {'username': request.user, 'guild_list': guild_list, 'invite_url': discord_invite})


@login_required(redirect_field_name="login")
@role_required(redirect_url='dashboard')
def server(request, pk):
    if request.user.is_authenticated:
        guild = Server.objects.get(server_id=pk,)
        return render(request, 'new_base.html', {'guild': guild})


@login_required()
@role_required(redirect_url='dashboard')
def welcome(request: Request, pk):
    if request.user.is_authenticated:
        success = None
        error = None
        if request.method == "POST":
            # print(request.POST)
            post_context = {}
            welcome = WelcomeData.objects.get(server_id=int(pk))
            if request.POST.get("welcome_channel", None) is not None:
                welcome.welcome_channel = request.POST.get('welcome_channel')
            if request.POST.get("welcome_enable") is not None:
                if request.POST.get('welcome_enable') == "on":
                    welcome.welcome_enable = True
                else:
                    welcome.welcome_enable = False
            else:
                welcome.welcome_enable = False
                # welcome.welcome_enable =request.POST.get('welcome_enable')
            if request.POST.get("welcome_message", None) is not None:
                welcome.welcome_msg = request.POST.get('welcome_message')
            if request.POST.get("welcome_role", None) is not None:
                welcome.self_role = request.POST.get('welcome_role')
            if request.POST.get("welcome_images", None) is not None:
                __image_link = request.POST.get('welcome_images').split(" ")
                for image in __image_link:
                    if image == "":
                        __image_link.remove(image)
                if len(__image_link) > 6:
                    __image_link = __image_link[0:4]

            image_name = []
            success = True
            i = 0
            for link in __image_link:
                try:
                    if link == '':
                        break
                    i = i + 1
                    url = requests.get(link)
                    background = Image.open(BytesIO(url.content))
                    width, height = background.size
                    if width <= 1920 and height <= 972:
                        error = link+' is not set valid for background \nminimum 1920*972 resolution required'
                        success = False
                    else:
                        background = background.resize((1920, 972))
                        output = ImageOps.fit(
                            background, background.size, centering=(0.5, 0.5))
                        output.save("media/images/"+str(pk) +
                                    "/"+str(pk)+"_"+str(i)+".jpg")
                        image_name.append(str(pk)+"_"+str(i)+".jpg")
                        if i == 1:
                            welcome.image1 = "images/" + \
                                str(pk)+"/"+str(pk)+"_"+str(i)+".jpg"
                        elif i == 2:
                            welcome.image2 = "images/" + \
                                str(pk)+"/"+str(pk)+"_"+str(i)+".jpg"
                        elif i == 3:
                            welcome.image3 = "images/" + \
                                str(pk)+"/"+str(pk)+"_"+str(i)+".jpg"
                        elif i == 4:
                            welcome.image4 = "images/" + \
                                str(pk)+"/"+str(pk)+"_"+str(i)+".jpg"
                        elif i == 5:
                            welcome.image5 = "images/" + \
                                str(pk)+"/"+str(pk)+"_"+str(i)+".jpg"
                except requests.exceptions.MissingSchema:
                    pass

            if success:
                welcome.update_by = request.user.id
                welcome.save()
                success = "welcome message set successfully"

        text_channel = []
        context = {}
        data = Discord_API()
        servers = Server.objects.get(pk=pk)
        servers = Server.objects.filter(pk=pk).filter(
            admin__contains=str(request.user.id))
        if servers is None:
            return redirect('dashboard')
        sata = data.get_guild_channel(settings.TOKEN, id=pk)
        roles = data.get_guild_roles(settings.TOKEN, id=pk)
        welcome_data = WelcomeData.objects.get(server_id=pk)
        guild = Server.objects.get(server_id=pk,)
        context = dict(
            welcome=welcome_data,
            guild=guild
        )
        welcome_channel = {}

        for i in sata:
            # print((type(i['type'])))
            if i['type'] == 0:

                text_channel.append(i)
                try:
                    if int(welcome_data.welcome_channel) == int(i['id']):
                        welcome_channel['id'] = i['id']
                        welcome_channel['name'] = i['name']
                except TypeError:
                    pass
        try:
            for role in roles:
                if int(welcome_data.self_role) == int(role['id']):
                    welcome_channel['role_id'] = role['id']
                    welcome_channel['role_name'] = role['name']
        except TypeError:
            pass
        context = dict(
            welcome=welcome_data,
            guild=guild,
            text_channel=text_channel,
            roles=roles,
            welcome_channel=welcome_channel,
            error=error,
            success=success
        )
        return render(request, 'welcome.html', context)
