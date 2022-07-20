from sakura.bot.events.on_guild import event_setup as on_guild_event
from sakura.bot.events.events import event_setup as on_event
from sakura.bot.events.on_member import event_setup as on_member_event
from sakura.bot.events.on_reaction import event_setup as on_reaction_event
from sakura.bot.events.on_commnad import event_setup as on_command_event


def event_setup(bot):
    pass
    on_guild_event(bot)
    on_event(bot)
    on_member_event(bot)
    on_reaction_event(bot)
    on_command_event(bot)