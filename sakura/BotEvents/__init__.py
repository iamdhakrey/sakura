from sakura.BotEvents.on_guild import event_setup as on_guild_event
from sakura.BotEvents.events import event_setup as on_event
from sakura.BotEvents.on_member import event_setup as on_member_event

def event_setup(bot):
    on_guild_event(bot)
    on_event(bot)
    on_member_event(bot)