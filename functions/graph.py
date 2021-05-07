import discord
import matplotlib.pyplot as plt
import numpy as np
from Equation import Expression

async def plot(ctx, eq, s, f):

    try:
        assert s, int
        assert f, int
    except Exception:
        await ctx.send("%s unfortunately that didn't work, please check your input" % ctx.author.mention)
        return

    s = int(s)
    f = int(f)

    try:
        fn = Expression(eq,["x"])
    except Exception:
        await ctx.send("%s unfortunately that didn't work, please check your formula" % ctx.author.mention)
        return

    n = 10**3

    x = np.arange(s, f, (n**-1)*(f-s))
    y = []

    for d in np.nditer(x):
        y.append(fn(d))

    y = np.array(y)

    plt.plot(x,y)
    plt.autoscale()
    plt.savefig("tmp.png")
    plt.clf()

    with open("tmp.png","rb") as f:
        await ctx.send("%s here is your graph:" % ctx.author.mention, file=discord.File(f))