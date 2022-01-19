from functions import config
import discord
import asyncio
import tinydb
from tinydb import Query, TinyDB

async def sset(ctx, classes, grade):
    db = TinyDB("res/db/classes.db")
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
        await ctx.send("%s, %s" % (config.config['general-error-message'], ctx.message.author.mention))
