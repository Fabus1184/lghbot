import asyncio
import discord
import time

mac_running = False

async def mac(ctx, frange, bot):
    global mac_running
    try:
        frange = int(frange)
        if not (frange == 100 or frange == 1000 or frange == 10000):
            raise Exception
    except:
        await ctx.send(
            "%s ❌ intools.valid range! (has to be 100,1000 or 10000)"
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
            tools.to_lb(x, punkte[ids.index(x)], "mac_%s" % frange)
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