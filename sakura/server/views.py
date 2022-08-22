from ast import literal_eval
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
from sakura.selfrole.models import SelfRole

discord_invite = settings.DISCORD_INVITE_LINK
# Create your views here.


@login_required(redirect_field_name="login")
@role_required(redirect_url='dashboard')
def server(request, pk):
    if request.user.is_authenticated:
        guild = Server.objects.get(server_id=pk, )
        return render(request, 'new_base.html', {'guild': guild})





class ServerMain(View):
    template_name = 'server/main.html'

    def get(self, request, pk):
        # fetch custom roles
        context = dict()
        self_roles = SelfRole.objects.filter(server=pk)

        if len(self_roles) < 1:
            self_roles = None
        
        context.update(self_roles=self_roles)
        

        return render(request, 'server/main.html') 