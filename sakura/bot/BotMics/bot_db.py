import discord
import django
from asgiref.sync import sync_to_async
from django.db import connection, connections
from sakura.server.models import  Server
from sakura.welcome.models import WelcomeData
from sakura.help.models import HelpCmd
from sakura.selfrole.models import SelfRole

from sakura.authentication.models import DiscordUser


class DbConnection():

    def __init__(self, d_user, d_guild) -> None:
        self.d_user = d_user
        self.d_guild = d_guild
        self._db_server = None
        self._db_user = None

    @classmethod
    def check_connections(self):
        if connection.connection and connection.is_usable():
            del connections._connections.default

    @classmethod
    @sync_to_async
    def _exists(self, model, **filters):
        self.check_connections()
        return model.objects.filter(**filters).exists()

    @classmethod
    async def _has(self, model, **filters):
        return await self._exists(model, **filters)

    @classmethod
    @sync_to_async
    def _get(self, model, **filters):
        self.check_connections()
        return model.objects.get(**filters)

    @classmethod
    @sync_to_async
    def _delete(self, model):
        self.check_connections()
        return model.delete()

    @classmethod
    @sync_to_async
    def _filter(self, model, **filters):
        self.check_connections()
        filter = []
        for _filter in model.objects.all().filter(**filters):
            filter.append(_filter)
        return filter

    @classmethod
    @sync_to_async
    def _left_update(self, model, **filters):
        self.check_connections()
        return model.objects.filter(**filters).update(is_active=False)

    @classmethod
    async def _left(self, model, **filters):
        self.check_connections()
        return self._left_update(model, **filters)

    @classmethod
    @sync_to_async
    def _save(self, obj):
        self.check_connections()
        obj.save()

    @classmethod
    @sync_to_async
    def _create(self, model, **kwargs):
        self.check_connections()
        return model.objects.create(**kwargs)

    @classmethod
    def get_sync_server(self, **filters):
        try:
            return Server.objects.get(**filters)
        except Server.DoesNotExist:
            return None

    @classmethod
    async def fetch_server(self, d_guild, **filter):
        if not await self._has(Server, server_id=int(d_guild.id)):
            server = await self._create(Server,
                                        server_id=int(d_guild.id),
                                        server_name=str(d_guild.name),
                                        avatar=str(d_guild.icon),
                                        owner=d_guild.owner_id)
        else:
            server = await self._get(Server, server_id=int(d_guild.id))
            if server.server_name == d_guild.name:
                server.server_name = d_guild.name
                server.is_active = True
                server.owner = d_guild.owner_id
                for key, values in filter.items():
                    if key == "admin":
                        server.admin = values
                    if key == "admin_role":
                        server.admin_role = values

                await self._save(server)
        return server

    @classmethod
    async def left_server(self, d_guild):
        if await self._has(Server, server_id=int(d_guild.id)):
            server = await self._get(Server, server_id=int(d_guild.id))
            server.is_active = False
            await self._save(server)
            return server

    @classmethod
    async def fetch_user(self, dc_user):
        if not await self._has(DiscordUser, id=str(dc_user.id)):
            user = await self._create(DiscordUser,
                                      id=str(dc_user.id),
                                      name=dc_user.name + "#" +
                                      dc_user.discriminator)
        else:
            user = await self._get(DiscordUser, id=str(dc_user.id))
            if not user.name == (dc_user.name + "#" + dc_user.discriminator):
                user.name = (dc_user.name + "#" + dc_user.discriminator)
                await self._save(user)
        return user

    @classmethod
    async def get_user(self):
        if self._db_user is None:
            self._db_user = await self.fetch_user(self.d_user)

    @classmethod
    async def fetch_welcome(self, d_guild, **kwargs):
        if not await self._has(WelcomeData, server_id=int(d_guild.id)):
            welcome = await self._create(
                WelcomeData,
                server_id=int(d_guild.id),
                server_name=str(d_guild.name),
                server_active=True,
                welcome_enable=False,
                welcome_msg="hey buddy [[member.name]] \n you are the " +
                "[[member.count]] of the [[server_name]] ",
            )
            server = await self._get(WelcomeData, server_id=int(d_guild.id))
            server.image1 = 'default/welcome1.jpg'
            server.image2 = 'default/welcome2.jpg'
            server.image3 = 'default/welcome3.jpg'
            server.image4 = 'default/welcome4.jpg'
            server.image5 = 'default/welcome5.jpg'

            welcome = await self._save(server)
        else:
            welcome = await self._get(WelcomeData, server_id=int(d_guild.id))
            for key, values in kwargs.items():
                if key == "welcome_enable":
                    welcome.welcome_enable = values
                if key == "self_role":
                    welcome.self_role = values
                if key == 'welcome_channel':
                    welcome.welcome_channel = values

                if key == "welcome_msg":
                    welcome.welcome_msg = values

                if key == 'update_by':
                    welcome.update_by = values

                if key == 'image1':
                    welcome.image1 = values

                if key == 'image2':
                    welcome.image2 = values

                if key == 'image3':
                    welcome.image3 = values

                if key == 'image4':
                    welcome.image4 = values

                if key == 'image5':
                    welcome.image5 = values

            await self._save(welcome)
        return welcome

    @classmethod
    async def fetch_self_role(self,
                              message_id=None,
                              guild: discord.Guild = None,
                              **kwargs) -> django.db.models.Model:
        if message_id:
            if not await self._has(SelfRole, message_id=int(message_id)):
                self_role = await self._create(
                    SelfRole,
                    message_id=int(message_id),
                    server=kwargs.get("guild_id", None),
                    max_role=kwargs.get("max_role", None),
                    reaction=kwargs.get('reaction', None))
            else:
                self_role = await self._get(SelfRole,
                                            message_id=int(message_id))
            return self_role
        elif guild:
            # print(await self._has(SelfRole, server=str(guild.id)))
            if kwargs.get("check_server", False):
                if await self._has(SelfRole, server=str(guild.id)):
                    self_role = await self._get(SelfRole, server=str(guild.id))
                    return self_role
                else:
                    return None
            if not await self._has(SelfRole, server=str(guild.id)):
                self_role = await self._create(
                    SelfRole,
                    server=int(guild.id),
                    max_role=kwargs.get("max_role", None),
                    reaction=kwargs.get('reaction', None))
            else:
                self_role = await self._filter(SelfRole, server=int(guild.id))
            return self_role

    @classmethod
    async def delete_self_role(self, message_id):
        print(await self._has(SelfRole, message_id=message_id))
        if await self._has(SelfRole, message_id=int(message_id)):
            self_role = await self._get(SelfRole, message_id=int(message_id))
            await self._delete(self_role)
            return True

    @classmethod
    async def fetch_help(self, cmd, **kwargs):
        if not await self._has(HelpCmd, cmd=cmd.name):
            help = await self._create(
                HelpCmd,
                cmd=cmd.name,
                description=cmd.description,
                usage=cmd.usage,
                category=cmd.cog_name,
                brief=cmd.brief,
                alias=cmd.aliases,
            )
        else:
            help = await self._get(HelpCmd, cmd=cmd.name)
            # help.cmd = cmd.name
            help.description = cmd.description
            help.usage = cmd.usage
            help.category = cmd.cog_name
            help.brief = cmd.brief
            help.alias = cmd.aliases
            await self._save(help)
