from django.contrib.auth.backends import BaseBackend

from .models import DiscordUser

class SakuraAuthenticationBackend(BaseBackend):
    def authenticate(request,user) -> DiscordUser:
        find_user = DiscordUser.objects.filter(id = user['id'])
        if len(find_user) == 0:
            print("User was not Found. Saving...")
            discord_tag = '%s#%s'%(user['username'],user['discriminator'])
            new_user = DiscordUser.objects.create_new_discord_user(user)
            print(new_user)

            return new_user
        return find_user

    def get_user(self,user_id):
        try:
            return DiscordUser.objects.get(pk=user_id)
        except DiscordUser.DoesNotExist:
            return None