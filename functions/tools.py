import re

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

    return id
