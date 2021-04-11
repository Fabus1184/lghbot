from discord_webhook import DiscordWebhook
import requests

r = requests.get('https://inspirobot.me/api?generate=true')

data = {
"content":"<@&802180024241225789> heutiges Frühkonzil:"
}


data['embeds'] = [{'description': "**" + " " + "**", "color": 16426522, "image": {"url": r.text}}]

url='https://discord.com/api/webhooks/802177754320994314/qEuFMCtsmF7T-raiX2BnInQqTmNBrv1Cw_JWlJiHVKVUaAokH42_KjENgWkFTqsoRlt8'

result = requests.post(url, json=data)

result.raise_for_status()
