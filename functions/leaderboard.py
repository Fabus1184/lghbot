import asyncio
import discord
from tinydb import Query, TinyDB, where
import tinydb
from sortedcontainers import SortedDict

async def lb(ctx):
    leaderboard = TinyDB("res/db/%i/leaderboard.db" % ctx.guild.id)

    trio = punkte("trio", leaderboard)
    mac100 = punkte("mac_100", leaderboard)
    mac1000 = punkte("mac_1000", leaderboard)
    mac10000 = punkte("mac_10000", leaderboard)
    pipapo = punkte("pipapo", leaderboard)

    embed = discord.Embed(
        title="Server Leaderboard",
        color=0xF1A90F,
        description="*only games with more than one player are counted*",
    )

    embed.add_field(name="Trio:", value=trio, inline=False)
    embed.add_field(name="mac 100:", value=mac100, inline=False)
    embed.add_field(name="mac 1000:", value=mac1000, inline=False)
    embed.add_field(name="mac 10000:", value=mac10000, inline=False)
    embed.add_field(name="pi-pa-po:", value=pipapo, inline=False)
    await ctx.send(embed=embed)


def punkte(name, leaderboard):
    r = ""
    ids = []
    punkte = []
    for x in leaderboard.search(Query().category == name):
        ids.append(x["id"])
        punkte.append(x["points"])

    list = [x for _, x in sorted(zip(punkte, ids), key=lambda pair: pair[0])]
    list.reverse()
    if list:
        for x in range(len(list), 3):
            list.append(list[len(list) - 1])

        erster = punkte[ids.index(list[0])]
        zweiter = punkte[ids.index(list[1])]
        dritter = punkte[ids.index(list[2])]
        if erster > 1000:
            erster = (
                str(erster / 1000)
                .replace(".", ",")
                .replace(".", ",")
                .split("points")[0]
                + "k"
            )
        if zweiter > 1000:
            zweiter = str(zweiter / 1000).replace(".", ",").split("points")[0] + "k"
        if dritter > 1000:
            dritter = str(dritter / 1000).replace(".", ",").split("points")[0] + "k"
        r += "%s <@%s>: %s points\n" % (":first_place:", list[0], erster)
        r += "%s <@%s>: %s points\n" % (":second_place:", list[1], zweiter)
        r += "%s <@%s>: %s points\n" % (":third_place:", list[2], dritter)
    else:
        r += "%s %s: %s points\n" % (":first_place:", "---", 0)
        r += "%s %s: %s points\n" % (":second_place:", "---", 0)
        r += "%s %s: %s points\n" % (":third_place:", "---", 0)

    return r
