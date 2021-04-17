from functions import config
import discord
import asyncio
import tinydb
from tinydb import Query, TinyDB
import sys
import os
from subprocess import PIPE, Popen
from functions import pyplan, tools
import glob

async def vplan_user(bot, id):
    try:
        assert id, int
    except:
        return

    db = TinyDB("res/db/classes.db")
    classes = db.search(Query().id == id)[0]["classes"].split(",")
    grade = db.search(Query().id == id)[0]["grade"]

    if not classes:
        return

    (plan, datum) = pyplan.plan(classes,grade)
    channel = await (await bot.fetch_user(id)).create_dm()

    if len(plan) >= 2000:

        text1 = plan[0:1955]
        text2 = plan[1955:]
    
        await channel.send(
            "%s, here is your current :calendar_spiral: Vertretungsplan **(%s)**: \n```\n%s```"
            % ("<@%i>" % id, datum, text1)
        )
        await channel.send("```\n%s```" % text2)

    else:
        await channel.send(
            "%s, here is your current :calendar_spiral: Vertretungsplan **(%s)**: \n```\n%s```"
            % ("<@%i>" % id, datum, plan)
        )



async def vplan(ctx):
    db = TinyDB("res/db/classes.db")
    classes = db.search(Query().id == ctx.message.author.id)[0]["classes"].split(",")
    grade = db.search(Query().id == ctx.message.author.id)[0]["grade"]

    if not classes:
        await ctx.send(
            "%s, please set your desired classes first!"
            % ctx.message.author.mention
        )
        return

    (plan, datum) = pyplan.plan(classes,grade)

    channel = await ctx.message.author.create_dm()

    if len(plan) >= 2000:

        text1 = plan[0:1955]
        text2 = plan[1955:]
    
        await channel.send(
            "%s, here is your current :calendar_spiral: Vertretungsplan **(%s)**: \n```\n%s```"
            % (ctx.message.author.mention, datum, text1)
        )
        await channel.send("```\n%s```" % text2)

    else:
        await channel.send(
            "%s, here is your current :calendar_spiral: Vertretungsplan **(%s)**: \n```\n%s```"
            % (ctx.message.author.mention, datum, plan)
        )

async def push(bot):
    if pyplan.fetch() == True:
        return

    db = TinyDB("res/db/classes.db")
    users = db.search(Query().id != "")

    for u in users:
        await vplan_user(bot, u['id'])

async def schedule(bot):
     while True:
        try:
            await asyncio.sleep(60)
            await push(bot)
        except:
            pass

