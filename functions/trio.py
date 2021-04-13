import asyncio
import discord
from prettytable import PrettyTable, ALL

trio_running = False

async def trio(ctx, incount):
    global trio_running
    count = 0
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
        os.remove("res/output.mp3")

        musik = ["res/music1.mp3", "res/music2.mp3", "res/music3.mp3"]

        random.shuffle(musik)

        music = musik * 7

        os.system(
            'ffmpeg -i "concat:%s|%s|%s|%s|%s|%s|%s|%s|%s|%s" -acodec copy res/output.mp3'
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
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("res/output.mp3"))
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
            % (such, config.config['wait-timeout'])
        )


        embed = discord.Embed(color=0xF1A90F)
        embed.add_field(name="Trio", value=tab, inline=False)
        embed.add_field(name="> ", value=search, inline=False)
        await ctx.send(embed=embed)

        def check(m):
            return m.channel == channel and m.content == "s"

        def combocheck(m):
            if not tools.valid(m):
                print("NOT tools.valid")
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
            if tools.conti(c1_index, c2_index, c3_index):
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

            if config.config['type-timeout'] != 15:
                config.config['type-timeout'] = 15

            msg = await bot.wait_for("message", check=check, timeout=config.config['wait-timeout'])

            user = msg.author.id

            multiple = ""

            remove = False

            try:
                if punkte[ids.index(msg.author.id)] >= config.config['trio-double']:
                    multiple = "\nyou need 2 combinations!"
                    config.config['type-timeout'] += 10
                    remove = True
            except:
                pass

            try:
                await ctx.send(
                    "%s you have ⌚ **%s seconds** to send your solution... %s"
                    % (msg.author.mention, config.config['type-timeout'], multiple)
                )
                msg = await bot.wait_for("message", check=trü, timeout=config.config['type-timeout'])
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
                config.config['type-timeout'] -= 10

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
                    if punkte[ids.index(msg.author.id)] == config.config['trio-double']:
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
            tools.to_lb(x, punkte[ids.index(x)], "trio")
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