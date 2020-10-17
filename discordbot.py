import discord
import random
import os

token = os.environ['DISCORD_BOT_TOKEN']
client = discord.Client()

@client.event
async def on_ready():
    print("ログインしました")

async def reply(message):
    operations = message.content.split(' ')
    content = ""
    if operations[1] == "run":
        if len(operations)>=2 and operations[2][0] == '@' and operations[2][1:].isdigit():
            content = operations[2][1:]
        elif len(operations)>=3 and operations[2].isdigit() and operations[3].isdigit():
            content = random.randint(int(operations[2]),int(operations[3]))
    await message.channel.send(content)

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if client.user in message.mentions:
        await reply(message)

client.run(token)