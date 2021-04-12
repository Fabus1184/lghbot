from functions import config
import discord

async def print_help(bot, ctx):
    prefix = ctx.prefix
    s = bot.get_channel(config.config['suggest-channel'])

    text = """
    > **%sset [\"class1, class2, class3, ... \"] [grade]** : set your classes and your grade\n
    (example: `%sset \"3m1, 5Ph1, 2mu1\" 12`), watch out for the quotation marks!\n
    > **%sget** : get your set classes and grade\n
    > **%ssuggest [text]** : suggest something to %s\n
    > **%svplan** : get the current vertretungsplan for your set classes and grades\n
    > **%strio [n]** : play n rounds of trio (in new channel!)\n
    > **%smac [100,1000,10000]** : play mirroring and complementing (in new channel!)\n
    > **%sleaderboard** or **lb** : show the server leaderboard\n
    > **%sstats** : show personal stats\n
    > **%spipapo** : play pi-pa-po\n
    **LGH Bot** by <@432116634807959554>
    """ % (
        prefix,
        prefix,
        prefix,
        prefix,
        s.mention,
        prefix,
        prefix,
        prefix,
        prefix,
        prefix,
        prefix,
    )

    embed = discord.Embed(title="Commands:", description=text, color=0xF1A90F)
    await ctx.send(embed=embed)
    return