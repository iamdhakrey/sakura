from django.shortcuts import render

# Create your views here.

from io import BytesIO

import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import request as Request
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import View
from PIL import Image, ImageOps

from sakura.bot.BotMics.api import Discord_API
from sakura.authentication.decorator import role_required
from sakura.server.models import Server
from sakura.welcome.models import WelcomeData

discord_invite = settings.DISCORD_INVITE_LINK

@login_required()
@role_required(redirect_url='dashboard')
def welcome(request: Request, pk):
    if request.user.is_authenticated:
        success = None
        error = None
        if request.method == "POST":
            # print(request.POST)
            # post_context = {}
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
                        error = link + ' is not set valid for background ' \
                                'minimum 1920*972 resolution required'
                        success = False
                    else:
                        background = background.resize((1920, 972))
                        output = ImageOps.fit(background,
                                              background.size,
                                              centering=(0.5, 0.5))
                        output.save("media/images/" + str(pk) + "/" + str(pk) +
                                    "_" + str(i) + ".jpg")
                        image_name.append(str(pk) + "_" + str(i) + ".jpg")
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
        guild = Server.objects.get(server_id=pk, )
        context = dict(welcome=welcome_data, guild=guild)
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
        context = dict(welcome=welcome_data,
                       guild=guild,
                       text_channel=text_channel,
                       roles=roles,
                       welcome_channel=welcome_channel,
                       error=error,
                       success=success)
        return render(request, 'welcome/welcome.html', context)


@login_required()
@role_required(redirect_url='dashboard')
def enable_welcome_msg(request, pk):
    if request.method == "POST":
        # get data form request
        # post_context = {}
        welcome = WelcomeData.objects.get(server_id=int(pk))
        if request.POST.get("enable") is not None:
            if request.POST.get('enable') == "1":
                welcome.welcome_enable = True
            else:
                welcome.welcome_enable = False
        welcome.update_by = request.user.id
        welcome.save()
        return JsonResponse({'success': True})
    else:
        # redirect to previous page
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class WelcomeView(View):
    template_name = 'welcome.html'

    def get(self, request: Request, pk):
        # get welcome data

        welcome_data = WelcomeData.objects.get(server_id=int(pk))
        print(welcome_data)
        # get guild
        # guild = Server.objects.get(server_id=pk)
        # get channels
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
            # guild=guild,
            text_channel=text_channel,
            roles=roles,
            welcome_channel=welcome_channel,
            error=None,
            success=None)
        return render(request, 'welcome.html', context)
