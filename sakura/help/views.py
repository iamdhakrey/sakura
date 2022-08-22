from django.shortcuts import render

from django.conf import settings
from django.shortcuts import render
from django.views.generic import View

from sakura.help.models import HelpCmd

discord_invite = settings.DISCORD_INVITE_LINK
# Create your views here.
# Create your views here.


class CommandView(View):
    template_name = 'command.html'

    def get(self, request):
        # if request.user.is_authenticated:
        help_cmds = HelpCmd.objects.all()
        # get unique categories in help_cmds
        categories = set([help_cmd.category for help_cmd in help_cmds])
        # guild = Server.objects.get(server_id=pk,

        return render(request, 'command.html', {
            'helpcmds': help_cmds,
            'categories': categories
        })
        # else:
        # return redirect('auth')


