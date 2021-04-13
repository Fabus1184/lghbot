import asyncio
import discord
from tinydb import Query, TinyDB, where
import tinydb
from sortedcontainers import SortedDict

async def stats(ctx):
    leaderboard = TinyDB("res/db/leaderboard.db")
    trio = ""
    mac100 = ""
    mac1000 = ""
    mac10000 = ""
    pipapo = ""

    for x in leaderboard.search(
        (Query().category == "mac_100") & (Query().id == ctx.author.id)
    ):
        mac100 += str(x["points"])
    for x in leaderboard.search(
        (Query().category == "mac_1000") & (Query().id == ctx.author.id)
    ):
        mac1000 += str(x["points"])
    for x in leaderboard.search(
        (Query().category == "mac_10000") & (Query().id == ctx.author.id)
    ):
        mac10000 += str(x["points"])
    for x in leaderboard.search(
        (Query().category == "trio") & (Query().id == ctx.author.id)
    ):
        trio += str(x["points"])
    for x in leaderboard.search(
        (Query().category == "pipapo") & (Query().id == ctx.author.id)
    ):
        pipapo += str(x["points"])

    if not trio:
        trio = "zerrrrooo"
    if not mac100:
        mac100 = "zerrrrooo"
    if not mac1000:
        mac1000 = "zerrrrooo"
    if not mac10000:
        mac10000 = "zerrrrooo"
    if not pipapo:
        pipapo = "zerrrrooo"

    trio += " points"
    mac100 += " points"
    mac1000 += " points"
    mac10000 += " points"
    pipapo += " points"

    embed = discord.Embed(
        title="Personal Stats:",
        color=0xF1A90F,
        description="*only games with more than one player are counted*",
    )
    embed.add_field(name="User:", value="%s" % ctx.author.mention, inline=False)
    embed.add_field(name="Trio:", value=trio, inline=False)
    embed.add_field(name="mac 100:", value=mac100, inline=False)
    embed.add_field(name="mac 1000:", value=mac1000, inline=False)
    embed.add_field(name="mac 10000:", value=mac10000, inline=False)
    embed.add_field(name="pipapo:", value=pipapo, inline=False)
    await ctx.send(embed=embed)