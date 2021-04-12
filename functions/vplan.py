from functions import config
import discord
import asyncio
import tinydb
from tinydb import Query, TinyDB

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
        process = Popen(["pdfgrep", "-i", "Standard", "res/plan.pdf"], stdout=PIPE)
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