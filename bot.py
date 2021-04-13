import asyncio
from functions.help import print_help
import glob
import json
import math
import os
import random
import subprocess
import time
import traceback
import collections
from sortedcontainers import SortedDict
from subprocess import PIPE, Popen
from prettytable import PrettyTable, ALL
import discord
import requests
from discord.ext import commands, tasks
from discord.ext.commands import CommandNotFound
from dotenv import load_dotenv
from tinydb import Query, TinyDB, where
import tinydb
from num2words import num2words
from functions import ban, config, suggest, help, set, get, tools, leaderboard, stats, trio, mac, pppkkk

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix=config.config['prefix'], help_command=None)

@bot.command(name="leaderboard", description="show leaderboard")
async def o(ctx):
    await leaderboard.lb(ctx)

@bot.command(name="lb", description="show leaderboard")
async def k(ctx):
    await leaderboard.lb(ctx)

@bot.command(name="stats", description="show personal stats")
async def s(ctx):
    await stats.stats(ctx)

@bot.command(name="set", description='set classes and grade, like "3m1, 2mu1, 3bio1" 12 etc.')
async def a(ctx, classes, grade):
    await set.sset(ctx, classes, grade)

@bot.command(name="get", description="get set classes")
async def b(ctx):
    await get.gget(ctx)

@bot.command(name="vplan", description="get current vertretungsplan for your defined classes")
async def v(ctx):
    await vplan.vplan(ctx)

@bot.command(name="trio", description="play a game of trio")
@commands.guild_only()
async def t(ctx, incount):
    await trio.trio(ctx,incount)

@bot.command(name="mac", description="play a nice game of mirroring and complementing")
@commands.guild_only()
async def m(ctx, frange):
    await mac.mac(ctx.frange)

pipapo = False
@bot.command(name="pipapo", description="play pi-pa-po-ki-ka")
@commands.guild_only()
async def pppkkk(ctx):
    await pppkkk.pppkkk(ctx)

@bot.command(name="help")
@commands.guild_only()
async def help(ctx):
    await print_help(bot, ctx)

@bot.command(name="ban")
@commands.guild_only()
@commands.has_permissions(administrator=True)
async def bann(ctx, mention):
    await ban.wegban(ctx, mention)

@bot.command(name="pardon")
@commands.guild_only()
@commands.has_permissions(administrator=True)
async def pardon(ctx, mention):
    await ban.pardon(ctx, mention)

@bot.command(name="suggest")
@commands.guild_only()
async def a(ctx, *args):
    await suggest.suggestion(bot, ctx, *args)

@bot.event
async def on_command_error(ctx, error):
    if error != TimeoutError:
        await ctx.send(
            ("%s an error occured: %s") % (ctx.message.author.mention, str(error))
        )

bot.run(TOKEN)