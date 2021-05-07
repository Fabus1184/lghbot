import discord
from matplotlib import rc
import matplotlib.pyplot as plt
import numpy as np
from Equation import Expression
import os
import sys
import re

async def plot(ctx, eq, s, f):

    try:
        assert s, int
        assert f, int
        
        if s == f:
            raise Exception

    except Exception:
        await ctx.send("%s unfortunately that didn't work, please check your input" % ctx.author.mention)
        return

    s = int(s)
    f = int(f)

    try:
        fn = Expression(eq, ["x"])

        if not fn:
            raise Exception
    
        label = "$$" + str(fn) + "$$"

        n = 10**3
        x = np.arange(s, f, (n**-1)*(f-s))
        y = []

        for d in np.nditer(x):

            if len(re.findall("\^",str(fn))) == 2:
                kek = eq.split("^")
                fa = Expression(kek[0], ["x"])
                fb = Expression(kek[1]+"^"+kek[2], ["x"])
                fa = fa(d)
                fb = fb(d)
                y.append(fa**fb)
            else:
                y.append(fn(d))

        y = np.array(y)
        
    except Exception as fuck:
        await ctx.send("%s unforunately that didn't work, please check your formula: %s" % (ctx.author.mention, str(fuck)))
        return

    try:
        sys.stderr = open(os.devnull,"a")
        sys.stdout = open(os.devnull,"a")
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.spines['left'].set_position('center')
        ax.spines['bottom'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        plt.rc('text', usetex=True)
        plt.rc('font', family='serif')
        plt.plot(x, y, 'navy', label=label)
        plt.grid(True)
        plt.title(label)
        plt.savefig("tmp.png", dpi=600)
        plt.clf()
    except Exception as kacke:
        await ctx.send("%s unfortunately that didn't work, please check your formula" % ctx.author.mention)
        print(kacke)
        return

    with open("tmp.png","rb") as f:
        await ctx.send("%s here is your graph of %s:" % (ctx.author.mention, eq), file=discord.File(f))


try:
    plt.rc('text', usetex=True)
    plt.title("$$test$$")
    plt.clf()
except Exception:
    pass