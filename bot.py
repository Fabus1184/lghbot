import asyncio
import glob
import json
import math
import os
import random
import subprocess
import time
import sys
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


def valid(input):
    input = input.split(" ")
    if len(input) != 3:
        return False
    if not (len(input[0]) == 2 and len(input[1]) == 2 and len(input[2]) == 2):
        return False

    alphabet = ["a", "b", "c", "d", "e", "f", "g", "A", "B", "C", "D", "E", "F", "G"]
    numbers = ["1", "2", "3", "4", "5", "6", "7"]
    if not input[0][0] in alphabet:
        return False
    if not input[1][0] in alphabet:
        return False
    if not input[2][0] in alphabet:
        return False
    if not input[0][1] in numbers:
        return False
    if not input[1][1] in numbers:
        return False
    if not input[2][1] in numbers:
        return False
    return True


def conti(c1, c2, c3):

    clist = [c1, c2, c3]
    clist.sort()
    (c1, c2, c3) = clist


    if c2 == c1 + 1 and c3 == c2 + 1 and c3 // 7 == c1 // 7:
        return True
    if c2 == c1 + 8 and c3 == c2 + 8 and c3 // 7 == c1 // 7 + 2:
        return True
    if c2 == c1 + 7 and c3 == c2 + 7:
        return True
    if c2 == c1 + 6 and c3 == c2 + 6 and c3 // 7 == c1 // 7 + 2:
        return True
    return False


with open("config", "r") as f:
    a = f.readline()
    waittimeout = int(a[0:2])
    type_timeout = int(a[2:4])
    print(waittimeout)
    print(type_timeout)
    f.close()

ban = []

with open("ban", "r") as f:
    for x in f.readlines():
        if x.replace("\n", ""):
            ban.append(x.replace("\n", ""))

print("BAN:")
print(ban)

count = 0

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

db = TinyDB("classes.db")

leaderboard = TinyDB("leaderboard.db")

trio_double = 4

prefix = "-"


general_error_message = "%s this didn't work, please check your syntax."

bot = commands.Bot(command_prefix=prefix, help_command=None)


def to_lb(id, points, category):
    tmp = leaderboard.search((where("id") == id) & (where("category") == category))
    if tmp:
        leaderboard.update(
            {"points": (int(tmp[0]["points"]) + int(points))},
            (where("id") == id) & (where("category") == category),
        )
    else:
        leaderboard.insert({"id": id, "points": points, "category": category})


@bot.command(name="leaderboard", description="show leaderboard")
async def lb(ctx):

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


bot.command(name="lb", description="show leaderboard")(lb.callback)


@bot.command(name="stats", description="show personal stats")
async def stats(ctx):

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


@bot.command(
    name="set", description='set classes and grade, like "3m1, 2mu1, 3bio1" 12 etc.'
)
async def settz(ctx, classes, grade):
    try:
        if not (classes and grade):
            await ctx.send(
                "%s, please set classes and grade as shown in %shelp"
                % (ctx.message.author.mention, ctx.prefix)
            )
            return
        if not db.search(Query().id == ctx.message.author.id):
            classes = str(classes).replace(" ", "")
            db.insert(
                {"id": ctx.message.author.id, "classes": str(classes), "grade": (grade)}
            )
            await ctx.send(
                "%s updated classes: %s"
                % (
                    ctx.message.author.mention,
                    db.search(Query().id == ctx.message.author.id)[0]["classes"],
                )
            )
        else:
            db.remove(Query().id == ctx.message.author.id)
            classes = str(classes).replace(" ", "")
            db.insert(
                {"id": ctx.message.author.id, "classes": str(classes), "grade": (grade)}
            )
            await ctx.send(
                "%s updated classes: %s"
                % (
                    ctx.message.author.mention,
                    db.search(Query().id == ctx.message.author.id)[0]["classes"],
                )
            )
    except Exception:
        await ctx.send(str(general_error_message) % ctx.message.author.mention)


@bot.command(name="get", description="get set classes")
async def get(ctx):
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
        await ctx.send(str(general_error_message) % ctx.message.author.mention)


@bot.command(
    name="vplan", description="get current vertretungsplan for your defined classes"
)
async def vplan(ctx):
    try:
        classes = db.search(Query().id == ctx.message.author.id)[0]["classes"]
        if not classes:
            await ctx.send(
                "%s, please set your desired classes first!"
                % ctx.message.author.mention
            )
            return
        grade = db.search(Query().id == ctx.message.author.id)[0]["grade"]
        process = Popen(["python3", "pyplan.py", str(classes), str(grade)], stdout=PIPE)
        (output, err) = process.communicate()
        exit_code = process.wait()
        process = Popen(["pdfgrep", "-i", "Standard", "plan.pdf"], stdout=PIPE)
        (datum, err) = process.communicate()
        datum = datum.decode("UTF-8")
        exit_code = process.wait()
        datum = datum.split("\n")[0][18:]

        text = output.decode("UTF-8")

        channel = await ctx.message.author.create_dm()

        if len(output.decode("UTF-8")) >= 2000:
            i = 0
            text1 = ""
            text2 = ""
            for x in text.split("\n"):
                if i < 17:
                    text1 += x
                    text1 += "\n"
                else:
                    text2 += x
                    text2 += "\n"
                i += 1
            await ctx.send(
                "%s your vplan is too long, sending as dm" % ctx.message.author.mention
            )
            await channel.send(
                "%s, here is your current :calendar_spiral: Vertretungsplan **(%s)**: \n```\n%s```"
                % (ctx.message.author.mention, datum, text1)
            )
            await channel.send("```\n%s```" % text2)
        else:
            dm = False
            for x in str(text).split("\n"):
                if len(str(x)) > 104:
                    dm = True
            print(dm)
            if dm:
                await ctx.send(
                    "%s your vplan is too long, sending as dm"
                    % ctx.message.author.mention
                )
                await channel.send(
                    "%s, here is your current :calendar_spiral: Vertretungsplan **(%s)**: \n```\n%s```"
                    % (ctx.message.author.mention, datum, text)
                )
            else:
                await ctx.send(
                    "%s, here is your current :calendar_spiral: Vertretungsplan **(%s)**: \n```\n%s```"
                    % (ctx.message.author.mention, datum, text)
                )

    except Exception:
        await ctx.send(str(general_error_message) % ctx.message.author.mention)


@bot.command(name="speedtest", description="do speedtest")
@commands.guild_only()
@commands.has_permissions(manage_webhooks=True)
async def test(ctx):
    try:
        await ctx.send("probing internet speed, please stand by....")
        process = Popen(["speedtest"], stdout=PIPE)
        (output, err) = process.communicate()
        exit_code = process.wait()
        await ctx.send("```\n%s```" % output.decode("UTF-8").replace("..", ""))
    except Exception:
        await ctx.send(str(general_error_message) % ctx.message.author.mention)


@bot.command(
    name="set_type_timeout", description="set the timeout when typing in trio game"
)
@commands.guild_only()
@commands.has_permissions(manage_webhooks=True)
async def stt(ctx, arg):
    global type_timeout
    try:
        if len(arg) > 2:
            raise Exception
        arg = int(arg)
    except Exception:
        await ctx.send("%s invalid number" % ctx.message.author.mention)
        return

    with open("config", "w") as f:
        f.write(str(waittimeout) + str(arg))

    type_timeout = arg

    await ctx.send("type timeout changed to %s" % type_timeout)


@bot.command(
    name="set_wait_timeout",
    description="set the timeout when waiting for a found combination in trio game",
)
@commands.guild_only()
@commands.has_permissions(manage_webhooks=True)
async def swt(ctx, arg):
    global waittimeout
    try:
        if len(arg) > 2:
            raise Exception
        arg = int(arg)
    except Exception:
        await ctx.send("%s invalid number" % ctx.message.author.mention)
        return

    with open("config", "w") as f:
        f.write(str(arg) + str(type_timeout))

    waittimeout = arg

    await ctx.send("wait timeout changed to %s" % waittimeout)


trio_running = False


@bot.command(name="trio", description="play a game of trio")
@commands.guild_only()
async def trio(ctx, incount):
    global trio_double
    global waittimeout
    global type_timeout
    try:
        count = int(incount)
    except Exception:
        await ctx.send("%s ❌ wrong amount of rounds" % ctx.message.author.mention)
        return
    if count <= 0 or count > 20:
        await ctx.send("%s ❌ noooo >:(" % ctx.message.author.mention)
        return

    global trio_running
    if trio_running:
        await ctx.send("%s some game is already running" % ctx.message.author.mention)
        return

    trio_running = True
    await bot.change_presence(activity=discord.Game(name="Trio"))

    category = bot.get_channel(802864419902062612)
    await ctx.message.guild.create_text_channel("trio-tmp", category=category)
    channel = discord.utils.get(ctx.guild.channels, name="trio-tmp")
    ctx.channel = channel

    time.sleep(3)

    feld = [None] * 49

    for x in range(0, 49):
        feld[x] = random.randint(1, 9)

    table = PrettyTable()

    table.field_names = [" ", "A", "B", "C", "D", "E", "F", "G"]
    side = "１２３４５６７"
    for x in range(0, 49, 7):
        table.add_row([side[x // 7]] + feld[x : x + 7])

    table.hrules = ALL


    user = None

    punkte = []
    ids = []


    try:
        os.remove("output.mp3")

        musik = ["music1.mp3", "music2.mp3", "music3.mp3"]

        random.shuffle(musik)

        music = musik * 7

        os.system(
            'ffmpeg -i "concat:%s|%s|%s|%s|%s|%s|%s|%s|%s|%s" -acodec copy output.mp3'
            % (
                music[0],
                music[1],
                music[2],
                music[3],
                music[4],
                music[5],
                music[6],
                music[7],
                music[8],
                music[9],
            )
        )

    except:
        print("ZAPPZARAPP ERROR MIT MUSIK KAPUTT")
        pass

    try:
        voice_channel = ctx.author.voice.channel
        vc = await voice_channel.connect()
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("output.mp3"))
        vc.play(source)
    except:
        pass


    suchs = []

    while count != 0:

        await bot.change_presence(activity=discord.Game(name="Trio"))
        tab = "```python\n" + str(table) + "```"
        such = random.randint(1, 50)
        while such in suchs:
            such = random.randint(1, 50)
        suchs.append(such)
        search = (
            '🔎 SEARCHING FOR NUMBER: **%d**\n write "s" when you found a combination - you have **%s** seconds '
            % (such, waittimeout)
        )


        embed = discord.Embed(color=0xF1A90F)
        embed.add_field(name="Trio", value=tab, inline=False)
        embed.add_field(name="> ", value=search, inline=False)
        await ctx.send(embed=embed)

        def check(m):
            return m.channel == channel and m.content == "s"

        def combocheck(m):
            if not valid(m):
                print("NOT VALID")
                return [False, None]

            comb = m.split(" ")
            c1 = comb[0]
            c2 = comb[1]
            c3 = comb[2]

            if c1[0] == "g" or c1[0] == "G":
                c1_x = 7
            else:
                c1_x = int(c1[0], 16) - 9

            if c2[0] == "g" or c2[0] == "G":
                c2_x = 7
            else:
                c2_x = int(c2[0], 16) - 9

            if c3[0] == "g" or c3[0] == "G":
                c3_x = 7
            else:
                c3_x = int(c3[0], 16) - 9

            c1_index = (int(c1[1]) - 1) * 7 + int(c1_x) - 1
            c2_index = (int(c2[1]) - 1) * 7 + int(c2_x) - 1
            c3_index = (int(c3[1]) - 1) * 7 + int(c3_x) - 1
            if conti(c1_index, c2_index, c3_index):
                if feld[c1_index] * feld[c2_index] + feld[c3_index] == such:
                    antwort = "%s*%s+%s=%s" % (
                        feld[c1_index],
                        feld[c2_index],
                        feld[c3_index],
                        such,
                    )
                    return [True, antwort]
                if feld[c1_index] * feld[c2_index] - feld[c3_index] == such:
                    antwort = "%s*%s-%s=%s" % (
                        feld[c1_index],
                        feld[c2_index],
                        feld[c3_index],
                        such,
                    )
                    return [True, antwort]
                if feld[c2_index] * feld[c3_index] + feld[c1_index] == such:
                    antwort = "%s*%s+%s=%s" % (
                        feld[c2_index],
                        feld[c3_index],
                        feld[c1_index],
                        such,
                    )
                    return [True, antwort]
                if feld[c2_index] * feld[c3_index] - feld[c1_index] == such:
                    antwort = "%s*%s-%s=%s" % (
                        feld[c2_index],
                        feld[c3_index],
                        feld[c1_index],
                        such,
                    )
                    return [True, antwort]
                if feld[c1_index] * feld[c3_index] + feld[c2_index] == such:
                    antwort = "%s*%s+%s=%s" % (
                        feld[c1_index],
                        feld[c3_index],
                        feld[c2_index],
                        such,
                    )
                    return [True, antwort]
                if feld[c1_index] * feld[c3_index] - feld[c2_index] == such:
                    antwort = "%s*%s-%s=%s" % (
                        feld[c1_index],
                        feld[c3_index],
                        feld[c2_index],
                        such,
                    )
                    return [True, antwort]
            return [False, None]

        def trü(m):
            return m.author.id == user and m.channel == channel

        try:

            if type_timeout != 15:
                type_timeout = 15

            msg = await bot.wait_for("message", check=check, timeout=waittimeout)

            user = msg.author.id

            multiple = ""

            remove = False

            try:
                if punkte[ids.index(msg.author.id)] >= trio_double:
                    multiple = "\nyou need 2 combinations!"
                    type_timeout += 10
                    remove = True
            except:
                pass

            try:
                await ctx.send(
                    "%s you have ⌚ **%s seconds** to send your solution... %s"
                    % (msg.author.mention, type_timeout, multiple)
                )
                msg = await bot.wait_for("message", check=trü, timeout=type_timeout)
            except asyncio.TimeoutError:
                await ctx.send(
                    "**%s 😔 no solution sent in time!**" % msg.author.mention
                )
                if msg.author.id in ids:
                    punkte[ids.index(msg.author.id)] -= 1
                else:
                    ids += [msg.author.id]
                    punkte += [-1]
                count -= 1
                continue

            if remove:
                type_timeout -= 10

            feett = [True, None]
            if multiple != "":
                fetz = combocheck(str(msg.content)[0:8])
                feett = combocheck(str(msg.content)[9:])
            else:
                fetz = combocheck(msg.content)

            if fetz[0] and feett[0] and str(msg.content)[0:8] != str(msg.content)[9:]:
                if multiple == "":
                    await ctx.send(
                        "%s %s is **correct!** ✅" % (msg.author.mention, fetz[1])
                    )
                else:
                    await ctx.send(
                        "%s %s is **correct!** ✅"
                        % (
                            msg.author.mention,
                            (str(fetz[1]) + " & " + str(feett[1])).replace("*", "\*"),
                        )
                    )

                if msg.author.id in ids:
                    punkte[ids.index(msg.author.id)] += 1
                    if punkte[ids.index(msg.author.id)] == trio_double:
                        await ctx.send(
                            "%s you need 2 combinations from now on!"
                            % (msg.author.mention)
                        )
                else:
                    ids += [msg.author.id]
                    punkte += [1]
            else:
                await ctx.send(
                    "%s %s is **incorrect!** ❌" % (msg.author.mention, msg.content)
                )
                if msg.author.id in ids:
                    punkte[ids.index(msg.author.id)] -= 1
                else:
                    ids += [msg.author.id]
                    punkte += [-1]

            count -= 1

            time.sleep(2)

        except asyncio.TimeoutError:
            await ctx.send("**😔 no solution sent in time!**")
            count -= 1


    list = [x for _, x in sorted(zip(punkte, ids), key=lambda pair: pair[0])]
    list.reverse()
    place = 0
    value = ""
    if not list:
        value = "."
    for x in list:
        medal = ""
        if place == 0:
            medal = ":first_place:"
        if place == 1:
            medal = ":second_place:"
        if place == 2:
            medal = ":third_place:"
        value += "%s <@%s>: %s points\n" % (medal, x, punkte[ids.index(x)])
        if len(list) > 1:
            to_lb(x, punkte[ids.index(x)], "trio")
        place += 1

    embed = discord.Embed(
        title=":checkered_flag:  :ribbon:  FINISHED  :ribbon:  :checkered_flag:",
        color=0xF1A90F,
    )
    embed.add_field(name="RANKING:", value=value, inline=False)
    await ctx.send(embed=embed)


    time.sleep(10)

    await bot.change_presence(status=discord.Status.online)
    await channel.delete()
    try:
        for x in bot.voice_clients:
            await x.disconnect()
    except:
        pass

    trio_running = False


mac_running = False


@bot.command(name="mac", description="play a nice game of mirroring and complementing")
@commands.guild_only()
async def mac(ctx, frange):

    try:
        frange = int(frange)
        if not (frange == 100 or frange == 1000 or frange == 10000):
            raise Exception
    except:
        await ctx.send(
            "%s ❌ invalid range! (has to be 100,1000 or 10000)"
            % ctx.message.author.mention
        )
        return

    global mac_running
    if mac_running:
        await ctx.send(
            "%s ❌ theres already a game running!" % ctx.message.author.mention
        )
        return

    mac_running = True
    await bot.change_presence(activity=discord.Game(name="mirroring and complementing"))

    punkte = []
    ids = []
    category = bot.get_channel(802864419902062612)
    await ctx.message.guild.create_text_channel("mac-tmp", category=category)
    channel = discord.utils.get(ctx.guild.channels, name="mac-tmp")
    ctx.channel = channel

    time.sleep(3)
    number = random.randint(1, frange - 1)

    def mirror(kek, ln):
        if ln == 2:
            dec = int(kek / 10)
            rst = kek - dec * 10
            return rst * 10 + dec
        elif ln == 3:
            hun = int(kek / 100)
            dec = int((kek - hun * 100) / 10)
            rst = kek - hun * 100 - dec * 10
            return rst * 100 + dec * 10 + hun
        elif ln == 4:
            tho = int(kek / 1000)
            hun = int((kek - tho * 1000) / 100)
            dec = int((kek - tho * 1000 - hun * 100) / 10)
            rst = kek - tho * 1000 - hun * 100 - dec * 10
            return rst * 1000 + dec * 100 + hun * 10 + tho
        else:
            return kek

    if frange == 100:
        flen = 2
    elif frange == 1000:
        flen = 3
    elif frange == 10000:
        flen = 4

    chain = [number]

    for i in range(1, 50):
        if i % 2 == 0 and flen == 3:
            number = 1000 - number
        elif flen == 3 and i % 2 != 0:
            number = mirror(number, 3)
        elif i % 2 != 0 and flen == 2:
            number = mirror(number, 2)
        elif i % 2 == 0 and flen == 2:
            number = 100 - number
        elif i % 2 == 0 and flen == 4:
            number = 10000 - number
        elif i % 2 != 0 and flen == 4:
            number = mirror(number, 4)
        chain.append(number)

    await ctx.send("**mirroring and complementing:**-")

    progress = 1

    def check(msg):
        return msg.channel == ctx.channel

    correct = True

    while mac_running:
        await bot.change_presence(
            activity=discord.Game(name="mirroring and complementing")
        )
        if progress == 44 and frange != 10000:
            number = random.randint(1, frange - 1)
            await ctx.send("**starting with new number:...**")
            progress = 1

            chain = [number]

            for i in range(1, 50):
                if i % 2 == 0 and flen == 3:
                    number = 1000 - number
                elif flen == 3 and i % 2 != 0:
                    number = mirror(number, 3)
                elif i % 2 != 0 and flen == 2:
                    number = mirror(number, 2)
                elif i % 2 == 0 and flen == 2:
                    number = 100 - number
                elif i % 2 == 0 and flen == 4:
                    number = 10000 - number
                elif i % 2 != 0 and flen == 4:
                    number = mirror(number, 4)
                chain.append(number)

        try:
            time.sleep(0.5)
            if correct:
                if progress % 2 != 0:
                    text = (
                        ":white_square_button:   mirror: **%i**" % chain[progress - 1]
                    )

                    embed = discord.Embed(color=0xF1A90F, description=text)
                    await ctx.send(embed=embed)

                else:
                    text = ":inbox_tray:   complement: **%i**" % chain[progress - 1]

                    embed = discord.Embed(color=0xF1A90F, description=text)
                    await ctx.send(embed=embed)


            msg = await bot.wait_for("message", check=check, timeout=20)

            try:
                msg.content = str(int(msg.content))

                if msg.content == str(chain[progress]):
                    correct = True
                    emoji = "\U00002705"
                    await msg.add_reaction(emoji)
                    if msg.author.id in ids:
                        punkte[ids.index(msg.author.id)] = (
                            int(punkte[ids.index(msg.author.id)]) + 1
                        )
                    else:
                        ids += [msg.author.id]
                        punkte += [1]
                    progress += 1
                else:
                    emoji = "\U0000274C"
                    await msg.add_reaction(emoji)
                    correct = False
            except:
                correct = False
                pass

        except asyncio.TimeoutError:
            break



    list = [x for _, x in sorted(zip(punkte, ids), key=lambda pair: pair[0])]
    list.reverse()
    place = 0
    value = ""
    if not list:
        value = "."
    for x in list:
        medal = ""
        if place == 0:
            medal = ":first_place:"
        if place == 1:
            medal = ":second_place:"
        if place == 2:
            medal = ":third_place:"
        value += "%s <@%s>: %s points\n" % (medal, x, punkte[ids.index(x)])
        if len(list) > 1:
            to_lb(x, punkte[ids.index(x)], "mac_%s" % frange)
        place += 1

    embed = discord.Embed(
        title=":checkered_flag:  :ribbon:  FINISHED  :ribbon:  :checkered_flag:",
        color=0xF1A90F,
    )
    embed.add_field(name="RANKING:", value=value, inline=False)
    await ctx.send(embed=embed)

    time.sleep(10)
    await channel.delete()
    await bot.change_presence(status=discord.Status.online)
    mac_running = False


pipapo = False


@bot.command(name="pipapo", description="play pi-pa-po-ki-ka")
@commands.guild_only()
async def pppkkk(ctx):

    ban = []

    global pipapo
    if pipapo:
        await ctx.send(
            "%s ❌ theres already a game running!" % ctx.message.author.mention
        )
        return

    pipapo = True
    await bot.change_presence(activity=discord.Game(name="pi-pa-po-ki-ka"))

    punkte = []
    ids = []
    category = bot.get_channel(802864419902062612)
    await ctx.message.guild.create_text_channel("pipapo-tmp", category=category)
    channel = discord.utils.get(ctx.guild.channels, name="pipapo-tmp")
    ctx.channel = channel


    embed = discord.Embed(
        title="pi-pa-po-ki-ka",
        color=0xF1A90F,
        description="pi: **2**\npa: **3**\n po: **5**\nki: **7**\nka: **11**",
    )
    await ctx.send(embed=embed)

    chain = []
    for i in range(1, 5000):
        temp = ""
        if i % 2 == 0:
            temp += "pi"
        if i % 3 == 0:
            temp += "pa"
        if i % 5 == 0:
            temp += "po"
        if i % 7 == 0:
            temp += "ki"
        if i % 11 == 0:
            temp += "ka"
        if temp == "":
            temp = str(i)
        chain.append(temp)

    progress = 1

    if progress == 4980:
        await ctx.send("**Bruh, jetzt ist mal schluss**")
        pipapo = False

    def check(msg):
        return msg.channel == ctx.channel and msg.author.id not in ban


    await bot.change_presence(activity=discord.Game(name="pi-pa-po"))

    while pipapo:

        t = random.randint(1, 15)
        time.sleep(t / 10)

        captcha = random.randint(1, 50)

        if captcha == 5 and progress != 1 and False:
            r = str(random.randint(123, 123456))

            list = [x for _, x in sorted(zip(punkte, ids), key=lambda pair: pair[0])]
            list.reverse()
            cap_id = list[0]

            if cap_id in ban:
                cap_id = list[1]

            def cap(msg):
                return (
                    msg.channel == ctx.channel
                    and msg.content == r
                    and msg.author.id == cap_id
                )

            num = (
                num2words(r)
                .replace("q", "𝕢")
                .replace("w", "𝕨")
                .replace("e", "𝕖")
                .replace("r", "𝕣")
                .replace("t", "𝕥")
                .replace("z", "𝕫")
                .replace("u", "𝕦")
                .replace("i", "𝕚")
                .replace("o", "𝕠")
            )
            num = (
                num.replace("p", "𝕡")
                .replace("a", "𝕒")
                .replace("m", "𝕞")
                .replace("n", "𝕟")
                .replace("b", "𝕓")
                .replace("v", "𝕧")
                .replace("c", "𝕔")
                .replace("x", "𝕩")
                .replace("y", "𝕪")
            )
            num = (
                num.replace("l", "𝕝")
                .replace("k", "𝕜")
                .replace("j", "𝕛")
                .replace("h", "𝕙")
                .replace("g", "𝕘")
                .replace("f", "𝕗")
                .replace("d", "𝕕")
                .replace("s", "𝕤")
            )

            await ctx.send(
                "<@%s> please prove that you are alive by typing %s as a number, you have 15 seconds"
                % (cap_id, num)
            )
            try:
                await bot.wait_for("message", check=cap, timeout=15)
                await ctx.send("not a bot... ok....")
            except:
                await ctx.send(
                    "<@%s> you are now banned from this round!" % str(cap_id)
                )
                ban.append(cap_id)
                punkte.remove(punkte[ids.index(cap_id)])
                ids.remove(ids[ids.index(cap_id)])

        try:

            msg = await bot.wait_for("message", check=check, timeout=30)
            while (msg.content).lower() != str(chain[progress - 1]):
                msg = await bot.wait_for("message", check=check, timeout=30)

            emoji = "\U00002705"
            await msg.add_reaction(emoji)

            if msg.author.id in ids:
                punkte[ids.index(msg.author.id)] = (
                    int(punkte[ids.index(msg.author.id)]) + 1
                )
            else:
                ids += [msg.author.id]
                punkte += [1]
            progress += 1

            if progress % 5 == 0:
                embed = discord.Embed(
                    title="Number: %s" % str(progress), color=0xF1A90F
                )
                await ctx.send(embed=embed)

        except:
            pipapo = False

    list = [x for _, x in sorted(zip(punkte, ids), key=lambda pair: pair[0])]
    list.reverse()
    place = 0
    value = ""
    if not list:
        value = "."
    for x in list:
        medal = ""
        if place == 0:
            medal = ":first_place:"
        if place == 1:
            medal = ":second_place:"
        if place == 2:
            medal = ":third_place:"
        value += "%s <@%s>: %s points\n" % (medal, x, punkte[ids.index(x)])
        if len(list) > 1 or len(ban) > 0:
            to_lb(x, punkte[ids.index(x)], "pipapo")
        place += 1

    embed = discord.Embed(
        title=":checkered_flag:  :ribbon:  FINISHED  :ribbon:  :checkered_flag:",
        color=0xF1A90F,
    )
    embed.add_field(name="RANKING:", value=value, inline=False)
    await ctx.send(embed=embed)

    time.sleep(10)
    await channel.delete()
    await bot.change_presence(status=discord.Status.online)
    pipapo = False


@bot.command(name="help")
@commands.guild_only()
async def help(ctx):

    prefix = ctx.prefix
    s = bot.get_channel(808305618733498410)

    text = """
    > **%sset [\"class1, class2, class3, ... \"] [grade]** : set your classes and your grade\n
    (example: `%sset \"3m1, 5Ph1, 2mu1\" 12`), watch out for the quotation marks!\n
    > **%sget** : get your set classes and grade\n
    > **%ssuggest [text]** : suggest something to %s\n
    > **%svplan** : get the current vertretungsplan for your set classes and grades\n
    > **%strio [n]** : play n rounds of trio (in new channel!)\n
    > **%smac [100,1000,10000]** : play mirroring and complementing (in new channel!)\n
    > **%sleaderboard** or **lb** : show the server leaderboard\n
    > **%sstats** : show personal stats\n
    > **%spipapo** : play pi-pa-po\n
    **LGH Bot** by <@432116634807959554>
    """ % (
        prefix,
        prefix,
        prefix,
        prefix,
        s.mention,
        prefix,
        prefix,
        prefix,
        prefix,
        prefix,
        prefix,
    )

    embed = discord.Embed(title="Commands:", description=text, color=0xF1A90F)
    await ctx.send(embed=embed)



@bot.command(name="ban")
@commands.guild_only()
@commands.has_permissions(manage_webhooks=True)
async def wegban(ctx, mention):
    global ban
    id = mention.replace("<", "").replace(">", "").replace("@", "").replace("!", "")
    ban.append(id)
    with open("ban", "a") as f:
        f.write("\n%s" % id)
    await ctx.send("%s has been banned from suggesting" % mention)


@bot.command(name="pardon")
@commands.guild_only()
@commands.has_permissions(manage_webhooks=True)
async def pardon(ctx, mention):
    global ban
    id = mention.replace("<", "").replace(">", "").replace("@", "").replace("!", "")
    ban.remove(id)
    with open("ban", "w") as f:
        for x in ban:
            f.write("\n%s" % id)
    await ctx.send("%s has been unbanned from suggesting" % mention)


@bot.command(name="suggest")
@commands.guild_only()
async def suggest(ctx, *args):
    print(ctx.message.author.id)
    print(ban)
    if str(ctx.message.author.id) in ban:
        await ctx.send(
            "%s unfortunately you are banned from using this command"
            % ctx.message.author.mention
        )
        return

    sugg = ""
    for x in args:
        sugg += x
        sugg += " "
    channel = bot.get_channel(808305618733498410)
    sugg = ("**by %s:**\n\n" % ctx.author.mention) + sugg
    embed = discord.Embed(title="New Suggestion", description=sugg, color=0xF1A90F)
    message = await channel.send(embed=embed)
    await message.add_reaction("\N{THUMBS UP SIGN}")
    await message.add_reaction("\N{THUMBS DOWN SIGN}")


@bot.event
async def on_command_error(ctx, error):
    if error != TimeoutError:
        await ctx.send(
            ("%s an error occured: %s") % (ctx.message.author.mention, str(error))
        )


bot.run(TOKEN)
