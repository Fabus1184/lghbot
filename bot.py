import os
import subprocess
import sys
import traceback
import discord
import random
import asyncio
import glob
import requests
import math
import json
from dotenv import load_dotenv
from discord.ext import commands, tasks
from discord.ext.commands import CommandNotFound
from tinydb import TinyDB, Query
from subprocess import Popen, PIPE

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

db = TinyDB('classes.db')
#db.insert({"id":0,"classes":"null"})
#for x in db.all():
    #print(x)

prefix = "-"

#with open("prefix","r") as f:
#    prefix = f.readline()[0]

print(prefix)

bot = commands.Bot(command_prefix=prefix, help_command=None)

@bot.command(name="prefix",description="change bot prefix")
@commands.has_permissions(administrator=True)
async def prefix(ctx, new_prefix):
    try:
        if not prefix:
            raise Exception
        if len(str(new_prefix)) != 1:
            await ctx.send("Error new prefix too short or too long: %s" % str(new_prefix))
            return
        with open("prefix","w") as f:
            f.write(str(new_prefix))
        await ctx.send("Restarting bot...")
        os.system("systemctl restart lgh_bot")
    except:
        await ctx.send("%s something went wrong, please check your syntax or refer to the help command")

@bot.command(name="set",description="set classes and grade, like \"3m1, 2mu1, 3bio1\" 12 etc.")
async def settz(ctx, classes, grade):
    try:
        if not (classes and grade):
            raise Exception
        if not db.search(Query().id == ctx.message.author.id):
            #print("NEW ENTRY")
            db.insert({"id":ctx.message.author.id,"classes":str(classes),"grade":(grade)})
            await ctx.send("%s updated classes: %s" % (ctx.message.author.mention,db.search(Query().id == ctx.message.author.id)[0]['classes']))
        else:
            db.remove(Query().id == ctx.message.author.id)
            db.insert({"id":ctx.message.author.id,"classes":str(classes),"grade":(grade)})
            await ctx.send("%s updated classes: %s" % (ctx.message.author.mention,db.search(Query().id == ctx.message.author.id)[0]['classes']))
    except Exception:
        await ctx.send("%s something went wrong, please check your syntax or refer to the help command" % ctx.message.author.mention)

@bot.command(name="vplan",description="get current vertretungsplan for your defined classes")
async def vplan(ctx):
    try:
        classes = (db.search(Query().id == ctx.message.author.id)[0]['classes'])
        #print(classes)
        grade = (db.search(Query().id == ctx.message.author.id)[0]['grade'])
        process = Popen(["python3", "pyplan.py", str(classes), str(grade)], stdout=PIPE)
        (output, err) = process.communicate()
        exit_code = process.wait()
        process = Popen(["pdfgrep", "-i", "Standard", "plan.pdf"], stdout=PIPE)
        (datum, err) = process.communicate()
        datum = datum.decode("UTF-8")
        exit_code = process.wait()
        datum = datum.split("\n")[0][18:]
        await ctx.send("%s, here is your current Vertretungsplan (%s): \n```\n%s```" % (ctx.message.author.mention,datum,output.decode("UTF-8")))
    except Exception:
        await ctx.send("%s something went wrong, please check your syntax or refer to the help command" % ctx.message.author.mention)

@bot.command(name="speedtest",description="do speedtest")
async def test(ctx):
    try:
        await ctx.send("probing internet speed, please stand by....")
        process = Popen(["speedtest"], stdout=PIPE)
        (output, err) = process.communicate()
        exit_code = process.wait()
        await ctx.send("```\n%s```" % output.decode("UTF-8").replace("..",""))
    except Exception:
        await ctx.send("%s something went wrong, please check your syntax or refer to the help command" % ctx.message.author.mention)

@bot.command(name="help")
async def help(ctx):
    prefix = ctx.prefix
    await ctx.send("> Available commands:\n%sprefix [prefix] : change the prefix for the bot (requires admin role)\n%sset [\"class1, class2, class3\"] [grade] : set your classes and your grade (example: `%sset \"3m1, 5Ph1, 2mu1\" 12`), watch out for the quotation marks!\n%svplan : get the current vertretungsplan for your set classes and grades" % (prefix,prefix,prefix,prefix))

@bot.event
async def on_command_error(ctx, error):
    await ctx.send((f"%s an error occured: {str(error)}") % ctx.message.author.mention)

bot.run(TOKEN)