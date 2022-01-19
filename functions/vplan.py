from io import BytesIO

import discord
from tinydb import Query, TinyDB
from functions import pyplan


async def vplan_user(bot, acc_id):
    assert type(acc_id) == int, "wrong user!"

    db = TinyDB("res/db/classes.db")
    classes = db.search(Query().id == acc_id)[0]["classes"].split(",")
    grade = db.search(Query().id == acc_id)[0]["grade"]

    assert classes is not None, "no classes defined!"

    (plan, datum) = pyplan.plan(classes, grade)
    channel = await (await bot.fetch_user(acc_id)).create_dm()

    if len(plan) >= 2000:

        text1 = plan[0:1955]
        text2 = plan[1955:]

        await channel.send(
            "%s, here is your current :calendar_spiral: Vertretungsplan **(%s)**: \n```\n%s```"
            % ("<@%i>" % acc_id, datum, text1)
        )
        await channel.send("```\n%s```" % text2)

    else:
        await channel.send(
            "%s, here is your current :calendar_spiral: Vertretungsplan **(%s)**: \n```\n%s```"
            % ("<@%i>" % acc_id, datum, plan)
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

    (plan, datum) = pyplan.plan(classes, grade)

    channel = await ctx.message.author.create_dm()

    k = BytesIO()
    plan.save(k, "png")
    k.seek(0)

    await channel.send(
        "%s, here is your current :calendar_spiral: Vertretungsplan **(%s)**:"
        % (ctx.message.author.mention, datum),
        file=discord.File(fp=k, filename="%s.png" % datum)
    )
