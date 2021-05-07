import asyncio
import glob
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from functions import ban, config, suggest, help, set, get, tools, leaderboard, stats, trio, mac, pppkkk, vplan, graph

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
bot = commands.Bot(command_prefix=config.config['prefix'], help_command=None)

@bot.command(name="leaderboard", description="show leaderboard")
async def a(ctx):
    await leaderboard.lb(ctx)

@bot.command(name="lb", description="show leaderboard")
async def b(ctx):
    await leaderboard.lb(ctx)

@bot.command(name="stats", description="show personal stats")
async def c(ctx):
    await stats.stats(ctx)

@bot.command(name="set", description='set classes and grade, like "3m1, 2mu1, 3bio1" 12 etc.')
async def d(ctx, classes, grade):
    await set.sset(ctx, classes, grade)

@bot.command(name="get", description="get set classes")
async def e(ctx):
    await get.gget(ctx)

@bot.command(name="vplan", description="get current vertretungsplan for your defined classes")
async def f(ctx):
    await vplan.vplan(ctx)

@bot.command(name="trio", description="play a game of trio")
@commands.guild_only()
async def g(ctx, incount):
    await trio.trio(ctx,incount, bot)

@bot.command(name="mac", description="play a nice game of mirroring and complementing")
@commands.guild_only()
async def h(ctx, frange):
    await mac.mac(ctx, frange, bot)

@bot.command(name="pipapo", description="play pi-pa-po-ki-ka")
@commands.guild_only()
async def i(ctx):
    await pppkkk.pppkkk(ctx, bot)

@bot.command(name="help")
@commands.guild_only()
async def j(ctx):
    await help.print_help(bot, ctx)

@bot.command(name="ban")
@commands.guild_only()
@commands.has_permissions(administrator=True)
async def k(ctx, mention):
    await ban.wegban(ctx, mention)

@bot.command(name="pardon")
@commands.guild_only()
@commands.has_permissions(administrator=True)
async def l(ctx, mention):
    await ban.pardon(ctx, mention)

@bot.command(name="suggest")
@commands.guild_only()
async def m(ctx, *args):
    await suggest.suggestion(bot, ctx, *args)

@bot.command(name="graph")
async def plot(ctx, eq, s, f):
    await graph.plot(ctx, eq, s, f)


@bot.event
async def on_command_error(ctx, error):
    if error != TimeoutError:
        await ctx.send(
            ("%s an error occured: %s") % (ctx.message.author.mention, str(error))
        )

@bot.event
async def on_ready():
    for s in bot.guilds:
        try:
            os.mkdir("res/db/%i" % s.id)
        except FileExistsError:
            pass
    print("READY")
    await vplan.schedule(bot)

bot.run(TOKEN)