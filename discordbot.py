import discord
import os

token = os.environ['DISCORD_BOT_TOKEN']
client = discord.Client()

@client.event
async def on_ready():
    print("ログインしました")

async def reply(message):
    operations = message.content.split(' ')
    await message.channel.send(operations[0])

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if client.user in message.mentions:
        await reply(message)

client.run(token)