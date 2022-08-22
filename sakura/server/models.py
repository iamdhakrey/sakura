from asgiref.sync import sync_to_async
from django.db import models

# Create your models here.






class Server(models.Model):
    server_id = models.BigIntegerField(verbose_name="Guild ID",
                                       primary_key=True)
    server_name = models.CharField(verbose_name="Guild Name", max_length=100)
    avatar = models.CharField(null=True, max_length=50)
    admin = models.CharField(null=True, max_length=100)
    owner = models.BigIntegerField(null=True)
    admin_role = models.CharField(null=True, max_length=100)
    is_active = models.BooleanField(default=True)
    members = models.ManyToManyField("User")

    def __str__(self) -> str:
        """GUILD"""
        return '{0} ({1})'.format(self.server_name, self.server_id)

    def member_count(self):
        return self.members.count()

    class Meta():
        verbose_name = "Guild"

    objects = models.Manager()


class User(models.Model):
    member_id = models.BigIntegerField(verbose_name="Discord ID",
                                       primary_key=True)
    discord_tag = models.CharField(verbose_name="Member Name", max_length=50)

    @property
    def mention(self):
        return "<@" + str(self.member_id) + ">"

    @sync_to_async
    def join_server(self, server):
        if not server.member.filter(id=self.member_id).exists():
            server.member.add(self)

    def __str__(self) -> str:
        return self.discord_tag

    objects = models.Manager()

