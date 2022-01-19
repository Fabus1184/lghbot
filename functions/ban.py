import asyncio
import discord
from tinydb import Query, TinyDB, where, operations
import tinydb
from functions import tools

async def wegban(ctx, id):
    id = tools.id_from_mention(ctx, id)

    if id == -1:
        return
    bandb = TinyDB("res/db/%i/ban.db" % ctx.guild.id)

    if bandb.search(where("id") == id) == []: 
        bandb.insert({ "id" : id })
        await ctx.send("<@%i> has been banned" % id)
    else:
        await ctx.send("<@%i> is already banned" % id)
    return

async def pardon(ctx, id):
    id = tools.id_from_mention(ctx, id)

    if id == -1:
        return
    
    bandb = TinyDB("res/db/%i/ban.db" % ctx.guild.id)

    if bandb.search(where("id") == id) != []: 
        bandb.remove(where("id") == id)     
        await ctx.send("<@%i> has been pardonned" % id)
    else:
        await ctx.send("<@%i> is not banned" % id)
    return

def isbanned(ctx, id):
    bandb = TinyDB("res/db/%i/ban.db" % ctx.guild.id)
    return bandb.search(where(str(ctx.guild.id)) == str(id)) != []