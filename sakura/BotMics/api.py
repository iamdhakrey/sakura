from sakura.BotMics.bot_db import DbConnection
from main.settings import CLIENT_ID, CLIENT_SECRET, DISCORD_REDIRECT_URL
import requests,json

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
        # print(response.json())
        for details in response.json():
            # print(details,"deatails")
            try:
                if details['owner'] == True:
                    if DbConnection.get_sync_server(server_id=details['id']):
                        as_a_guild.append(details)
            except TypeError:
                pass
        return as_a_guild

    def get_guild_channel(self,access_token,id):
        # return None
        url = "https://discord.com/api/v8/guilds/"+str(id)+'/channels'
        # print(url)
        # print(access_token)
        response = requests.get(url,headers={
            'Authorization':"Bot %s"% access_token
        })
        # print(response.json())
        return response.json()
        # print(json.dumps(response.json(),indent=5))

    def _take_second(self,elem):
        return elem['name']


    def get_guild_roles(self,token,id):
        url = "https://discord.com/api/v8/guilds/"+str(id)+'/roles'
        # print(url)
        # print(access_token)
        response = requests.get(url,headers={
            'Authorization':"Bot %s"% token
        })
        # print(response.json())
        roles_list=[]
        for roles in response.json():
            try:
                if roles['tags']:
                    pass
            except KeyError:
                roles_list.append(roles)
        roles_list.pop(0)
        roles_list.sort(key=self._take_second,reverse=True)
        return roles_list
        # print(json.dumps(response.json(),indent=5))
        pass