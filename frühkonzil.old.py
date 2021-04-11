from discord_webhook import DiscordWebhook
import json
import requests
import random

urls = [
"https://media.giphy.com/media/NPKhwkGVFZyub94kl0/giphy.gif",
"https://media.giphy.com/media/Xjem6W2mjYSlFflXL2/giphy.gif",
"https://media.giphy.com/media/wwEkhxbeGAsWmM7mad/giphy.gif",
"https://media.giphy.com/media/IuUScKwIQbfVWxiCNO/giphy.gif",
"https://media.giphy.com/media/JRm3d4WhaqV6xNo3d8/giphy.gif",
"https://media.giphy.com/media/eo86p9odhdpV6dLurt/giphy.gif",
"https://media.giphy.com/media/jqvqLQRmSYnFcOLhOB/giphy.gif",
"https://media.giphy.com/media/8duPSzdj5AthgXnwc8/giphy.gif",
"https://media.giphy.com/media/wYZkxsbc4XMGggT0xh/giphy.gif"
]

#r = requests.get('https://uselessfacts.jsph.pl/random.json?language=en')
r = requests.get('https://inspirobot.me/api?generate=true')


json_string = r.text.replace("'", "\"")
d = json.loads(json_string)


data = {
"content":"<@&802180024241225789> heutiges Frühkonzil:"
}

fetz = random.choice(urls)

text = d['text'].replace("'","\'")

data['embeds'] = [{'description': "**" + text + "**", "color": 16426522, "image": {"url": fetz}}]

url='https://discord.com/api/webhooks/802177754320994314/qEuFMCtsmF7T-raiX2BnInQqTmNBrv1Cw_JWlJiHVKVUaAokH42_KjENgWkFTqsoRlt8'

result = requests.post(url, json=data)

result.raise_for_status()
