from os import access
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
            discord_tag = discord_tag,
            access_token = user['access_token']
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
    access_token = models.CharField(verbose_name='access_token', max_length=50,null=True)
    mfa_enabled = models.BooleanField()
    last_login = models.DateTimeField(null=True)
    
    def is_authenticated(self,request):
        return True

    def change_access(self,access_token):
        self.access_token = access_token
        self.save()

    def __str__(self):
        if len(self.discord_tag) >13:
            return self.discord_tag[:13]
        else:
            return self.discord_tag
    

from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)


class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have a valid address')

        user = self.model(
            username=username,

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            username,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(
        verbose_name='username',
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['date_of_birth']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin