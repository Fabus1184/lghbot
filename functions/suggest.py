import discord
from functions import ban, config

async def suggestion(bot, ctx, *args):
    if ban.isbanned(ctx, ctx.message.author.id):
        await ctx.send(
            "%s unfortunately you are banned from using this command"
            % ctx.message.author.mention
        )
        return

    sugg = ""
    for x in args:
        sugg += x
        sugg += " "

    channel = bot.get_channel(config.config['suggest-channel'])

    sugg = ("**by %s:**\n\n" % ctx.author.mention) + sugg
    embed = discord.Embed(title="New Suggestion", description=sugg, color=0xF1A90F)
    message = await channel.send(embed=embed)
    await message.add_reaction("\N{THUMBS UP SIGN}")
    await message.add_reaction("\N{THUMBS DOWN SIGN}")
    return