import asyncio
import discord
import time
import random
from num2words import num2words
from functions import tools, config

pipapo = []

async def pppkkk(ctx, bot):
    global pipapo
    
    ban = []
    if ctx.guild.id in pipapo:
        await ctx.send(
            "%s ❌ theres already a game running!" % ctx.message.author.mention
        )
        return

    pipapo.append(ctx.guild.id)

    pipapo = True
    await bot.change_presence(activity=discord.Game(name="pi-pa-po-ki-ka"))

    punkte = []
    ids = []
    category = bot.get_channel(config.config['games-category'])
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
            tools.to_lb(ctx, x, punkte[ids.index(x)], "pipapo")
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
    pipapo.remove(ctx.guild.id)