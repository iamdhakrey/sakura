from sakura.BotMics.bot_db import DbConnection
from main.settings import CLIENT_ID, CLIENT_SECRET, DISCORD_REDIRECT_URL
import requests


class Discord_API:
    def __init__(self,client_id=None,client_secret=None,redirect_url=None,settings=True) -> None:
        if settings:
            self.client_id  = CLIENT_ID
            self.client_secret = CLIENT_SECRET
            self.redirect_url = DISCORD_REDIRECT_URL

        else:   
            self.client_id  = client_id
            self.client_secret = client_secret
            self.redirect_url = redirect_url

    def exchange_code(self,code:str):
        data = {
            "client_id":self.client_id,
            "client_secret":self.client_secret,
            "grant_type":"authorization_code",
            "code":code,
            "redirect_uri":self.redirect_url,
            'scope':'identify guilds guilds.join'
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.post('https://discord.com/api/oauth2/token',data=data,headers=headers)

        print(response)
        credentials = response.json()
        print(credentials)

        access_token = credentials['access_token']

        response = requests.get("https://discord.com/api/v8/users/@me",headers={
            'Authorization':"Bearer %s"% access_token
        })

        print(response)
        user = response.json()
        user['access_token'] = access_token
        print(user)
        return user

    def get_guild_list(self,access_token):
        response = requests.get("https://discord.com/api/v8/users/@me/guilds",headers={
            'Authorization':"Bearer %s"% access_token
        })
        as_a_guild = []
        for details in response.json():
            if details['owner'] == True:
                if DbConnection.get_sync_server(server_id=details['id']):
                    as_a_guild.append(details)
        return as_a_guild