from django.db import models

from django.contrib.auth.models import User, UserManager
# Create your models here.


class DiscordUserManager(UserManager):
    def create_new_discord_user(self,user):
        discord_tag = '%s#%s'%(user['username'],user['discriminator'])
        new_user = self.create(
            id = user['id'],
            avatar = user['avatar'],
            public_flags = user['public_flags'],
            flags = user['flags'],
            locale = user['locale'],
            mfa_enabled = user['mfa_enabled'],
            discord_tag = discord_tag
        )
        return new_user

class DiscordUser(models.Model):
    objects = DiscordUserManager()
    id = models.BigIntegerField(primary_key=True)
    discord_tag = models.CharField(max_length=100)
    avatar = models.CharField(max_length=100,null=True)
    public_flags = models.IntegerField()
    flags = models.IntegerField()
    locale = models.CharField(max_length=100)
    mfa_enabled = models.BooleanField()
    last_login = models.DateTimeField(null=True)
    
    def is_authenticated(self,request):
        return True

    def __str__(self):
        if len(self.discord_tag) >13:
            return self.discord_tag[:13]
        else:
            return self.discord_tag
    