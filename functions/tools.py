import re
import discord
from tinydb import Query, TinyDB, where
import tinydb

def id_from_mention(ctx, mention):
    assert mention, str
    assert ctx, discord.ext.commands.context.Context

    try:
        if not re.match("<@!?[0-9]*>", mention):
            raise Exception 

        id = re.findall("[0-9]+", mention)[0]

    except:
        ctx.send("Not a valid user!")
        return -1

    return int(id)

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

def to_lb(ctx, id, points, category):
    leaderboard = TinyDB("res/db/%i/leaderboard.db" % ctx.guild.id)
    tmp = leaderboard.search((where("id") == id) & (where("category") == category))
    if tmp:
        leaderboard.update(
            {"points": (int(tmp[0]["points"]) + int(points))},
            (where("id") == id) & (where("category") == category),
        )
    else:
        leaderboard.insert({"id": id, "points": points, "category": category})

