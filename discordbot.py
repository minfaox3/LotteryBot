import psycopg2
import discord
import random
import os

token = os.environ['DISCORD_BOT_TOKEN']
client = discord.Client()
connection = psycopg2.connect(os.environ['DATABASE_URL'])
cursor = connection.cursor()

@client.event
async def on_ready():
    print("ログインしました")

async def reply(message):
    operations = message.content.split(' ')
    content = ""
    if len(operations)>=2:
        if operations[1] == "run":
            if len(operations) >= 3 and operations[2][0] == '@' and operations[2][1:].isdigit():
                content = operations[2][1:]
            elif len(operations) >= 4 and operations[2].isdigit() and operations[3].isdigit():
                content = random.randint(int(operations[2]), int(operations[3]))
        elif operations[1] == "create":
            content = ""
        elif operations[1] == "list":
            if len(operations) >= 3 and operations[2] == "public":
                content = "public"
            else:
                cursor.execute("\\dt")
                print(cursor)
                content = ""
    await message.channel.send(content)

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if client.user in message.mentions:
        await reply(message)

client.run(token)