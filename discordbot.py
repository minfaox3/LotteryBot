import discord
import os

token = os.environ['DISCORD_BOT_TOKEN']
client = discord.Client()

@client.event
async def on_ready():
    print("ログインしました")

async def reply(message):
    reply = f'{message.author.mention} こんにちわ'
    await message.channel.send(reply)

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if client.users in message.mentions:
        await reply(message)

client.run(token)