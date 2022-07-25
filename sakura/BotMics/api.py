
import requests
from main.settings import CLIENT_ID, CLIENT_SECRET, DISCORD_REDIRECT_URL
from sakura.BotMics.bot_db import DbConnection


class Discord_API:

    def __init__(self,
                 client_id=None,
                 client_secret=None,
                 redirect_url=None,
                 settings=True) -> None:
        if settings:
            self.client_id = CLIENT_ID
            self.client_secret = CLIENT_SECRET
            self.redirect_url = DISCORD_REDIRECT_URL

        else:
            self.client_id = client_id
            self.client_secret = client_secret
            self.redirect_url = redirect_url

    # check token in valid or expired
    def check_token(self, token):
        url = "https://discord.com/api/v8/users/@me"
        response = requests.get(url,
                                headers={'Authorization': "Bearer %s" % token})
        return response.status_code

    def exchange_code(self, code: str):
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_url,
            'scope': 'identify guilds guilds.join'
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post('https://discord.com/api/oauth2/token',
                                 data=data,
                                 headers=headers)

        credentials = response.json()

        access_token = credentials['access_token']

        response = requests.get(
            "https://discord.com/api/v8/users/@me",
            headers={'Authorization': "Bearer %s" % access_token})

        user = response.json()
        user['access_token'] = access_token
        return user

    def get_guild_list(self, access_token):
        response = requests.get(
            "https://discord.com/api/v8/users/@me/guilds",
            headers={'Authorization': "Bearer %s" % access_token})
        as_a_guild = []
        for details in response.json():
            if details['owner'] is True:
                if DbConnection.get_sync_server(server_id=details['id']):
                    as_a_guild.append(details)
        return as_a_guild

    def get_guild_channel(self, access_token, id):
        url = "https://discord.com/api/v8/guilds/" + str(id) + '/channels'
        response = requests.get(
            url, headers={'Authorization': "Bot %s" % access_token})
        return response.json()

    def _take_second(self, elem):
        return elem['name']

    def get_guild_roles(self, token, id):
        url = "https://discord.com/api/v8/guilds/" + str(id) + '/roles'
        response = requests.get(url,
                                headers={'Authorization': "Bot %s" % token})
        roles_list = []
        for roles in response.json():
            try:
                if roles['tags']:
                    pass
            except KeyError:
                roles_list.append(roles)
        roles_list.pop(0)
        roles_list.sort(key=self._take_second, reverse=True)
        return roles_list
