import asyncio
import discord
from tinydb import Query, TinyDB, where, operations
import tinydb

from functions import tools

async def wegban(ctx, id):

    id = tools.id_from_mention(ctx, id)

    if id == -1:
        return

    bandb = TinyDB("res/db/ban.db")

    if bandb.search(where(str(ctx.guild.id)) == str(id)) == []: 
        bandb.insert({ "%s" % str(ctx.guild.id) : "%s" % str(id) })
        await ctx.send("<@%s> has been banned" % id)
    else:
        await ctx.send("<@%s> is already banned" % id)

    return

async def pardon(ctx, id):
    id = tools.id_from_mention(ctx, id)

    if id == -1:
        return

    bandb = TinyDB("res/db/ban.db")

    if bandb.search(where(str(ctx.guild.id)) == str(id)) != []: 
        bandb.remove(where(str(ctx.guild.id)) == id)     
        await ctx.send("<@%s> has been pardonned" % id)
    else:
        await ctx.send("<@%s> is not banned" % id)

    return

def isbanned(ctx, id):
    bandb = TinyDB("res/db/ban.db")
    return bandb.search(where(str(ctx.guild.id)) == str(id)) != []