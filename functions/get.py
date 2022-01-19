from functions import config
import discord
import asyncio
import tinydb
from tinydb import Query, TinyDB

async def gget(ctx):
    db = TinyDB("res/db/classes.db")
    try:
        if not db.search(Query().id == ctx.message.author.id):
            await ctx.send("%s you haven't set any classes yet" % ctx.author.mention)
            return
        else:
            gett = db.search(Query().id == ctx.message.author.id)
            await ctx.send(
                str(
                    "%s\nclasses: `"
                    + str(gett[0]["classes"])
                    + "`\ngrade: `"
                    + str(gett[0]["grade"])
                    + "`"
                )
                % ctx.author.mention
            )
    except Exception:
        await ctx.send("%s, %s" % (config.config['general-error-message'], ctx.message.author.mention))
