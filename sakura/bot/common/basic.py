import discord
from discord.ext.commands.context import Context


class Basic:

    async def avatar(self, ctx: Context, user: discord.Member):
        embed = discord.Embed(title="Avatar")
        embed.set_author(icon_url=user.avatar, name=user)
        embed.set_image(url=user.avatar)
        return embed

    async def ping(self, ctx: Context):
        ping = round(self.bot.latency, 2)
        data = "Pong 🟢 {}ms ".format(ping)
        embed = discord.Embed(title=None, description=data, color=0x000000)
        return embed

    async def say(self, ctx: Context, text: str, *args):
        txt = " ".join((text, ) + args)
        await ctx.trigger_typing()
        await ctx.send(txt)

    async def info(self, ctx: Context, user: discord.Member):
        embed = discord.Embed(title=f"{user} Info")
        embed.color = user.color
        embed.set_author(icon_url=user.avatar, name=user)
        embed.set_image(url=user.avatar)
        embed.add_field(name="Name", value=user.name, inline=True)
        embed.add_field(name="User ID", value=user.id, inline=True)
        embed.add_field(name="Status", value=user.status, inline=True)
        embed.add_field(name="Created at",
                        value=user.created_at.date(),
                        inline=True)
        embed.add_field(name="Joined at",
                        value=user.joined_at.date(),
                        inline=True)
        embed.add_field(name="Roles", value=len(user.roles), inline=True)
        embed.add_field(name="Nickname", value=user.nick, inline=True)
        embed.add_field(name="Top Role", value=user.top_role, inline=True)
        embed.add_field(name="Bot", value=user.bot, inline=True)
        embed.add_field(name="Discriminator",
                        value=user.discriminator,
                        inline=True)
        embed.add_field(name="Color", value=user.color, inline=True)
        return embed
