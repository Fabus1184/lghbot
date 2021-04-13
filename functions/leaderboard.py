import asyncio
import discord
from tinydb import Query, TinyDB, where
import tinydb
from sortedcontainers import SortedDict

async def lb(ctx):
    leaderboard = TinyDB("res/db/leaderboard.db")
    trio = ""
    mac100 = ""
    mac1000 = ""
    mac10000 = ""
    pipapo = ""

    ids = []
    punkte = []
    for x in leaderboard.search(Query().category == "mac_100"):
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
        mac100 += "%s <@%s>: %s points\n" % (":first_place:", list[0], erster)
        mac100 += "%s <@%s>: %s points\n" % (":second_place:", list[1], zweiter)
        mac100 += "%s <@%s>: %s points\n" % (":third_place:", list[2], dritter)

    ids = []
    punkte = []
    for x in leaderboard.search(Query().category == "mac_1000"):
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
            erster = str(erster / 1000).replace(".", ",").split("points")[0] + "k"
        if zweiter > 1000:
            zweiter = str(zweiter / 1000).replace(".", ",").split("points")[0] + "k"
        if dritter > 1000:
            dritter = str(dritter / 1000).replace(".", ",").split("points")[0] + "k"

        mac1000 += "%s <@%s>: %s points\n" % (":first_place:", list[0], erster)
        mac1000 += "%s <@%s>: %s points\n" % (":second_place:", list[1], zweiter)
        mac1000 += "%s <@%s>: %s points\n" % (":third_place:", list[2], dritter)

    ids = []
    punkte = []
    for x in leaderboard.search(Query().category == "mac_10000"):
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
            erster = str(erster / 1000).replace(".", ",").split("points")[0] + "k"
        if zweiter > 1000:
            zweiter = str(zweiter / 1000).replace(".", ",").split("points")[0] + "k"
        if dritter > 1000:
            dritter = str(dritter / 1000).replace(".", ",").split("points")[0] + "k"

        mac10000 += "%s <@%s>: %s points\n" % (":first_place:", list[0], erster)
        mac10000 += "%s <@%s>: %s points\n" % (":second_place:", list[1], zweiter)
        mac10000 += "%s <@%s>: %s points\n" % (":third_place:", list[2], dritter)

    ids = []
    punkte = []
    for x in leaderboard.search(Query().category == "trio"):
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
            erster = str(erster / 1000).replace(".", ",").split("points")[0] + "k"
        if zweiter > 1000:
            zweiter = str(zweiter / 1000).replace(".", ",").split("points")[0] + "k"
        if dritter > 1000:
            dritter = str(dritter / 1000).replace(".", ",").split("points")[0] + "k"

        trio += "%s <@%s>: %s points\n" % (":first_place:", list[0], erster)
        trio += "%s <@%s>: %s points\n" % (":second_place:", list[1], zweiter)
        trio += "%s <@%s>: %s points\n" % (":third_place:", list[2], dritter)

    ids = []
    punkte = []
    for x in leaderboard.search(Query().category == "pipapo"):
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
            erster = str(erster / 1000).replace(".", ",").split("points")[0] + "k"
        if zweiter > 1000:
            zweiter = str(zweiter / 1000).replace(".", ",").split("points")[0] + "k"
        if dritter > 1000:
            dritter = str(dritter / 1000).replace(".", ",").split("points")[0] + "k"

        pipapo += "%s <@%s>: %s points\n" % (":first_place:", list[0], erster)
        pipapo += "%s <@%s>: %s points\n" % (":second_place:", list[1], zweiter)
        pipapo += "%s <@%s>: %s points\n" % (":third_place:", list[2], dritter)

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
