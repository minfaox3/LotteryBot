import psycopg2
import discord
import random
import os

token = os.environ['DISCORD_BOT_TOKEN']
client = discord.Client()


def create_connection():
    return psycopg2.connect(os.environ['DATABASE_URL'])


@client.event
async def on_ready():
    print("ログインしました")


async def reply(message):
    operations = message.content.split(' ')
    content = ""
    if len(operations) >= 2:
        if operations[1] == "run":
            if len(operations) >= 3 and operations[2][0] == '@' and operations[2][1:].isdigit():
                content = operations[2][1:]
            elif len(operations) >= 4 and operations[2].isdigit() and operations[3].isdigit():
                content = random.randint(int(operations[2]), int(operations[3]))
        elif operations[1] == "create":
            if len(operations) >= 4 and operations[2] == "public":
                with create_connection() as connection:
                    with connection.cursor() as cursor:
                        cursor.execute("INSERT INTO lottery_table(user_name, lottery_name) VALUES ('public', %s);",
                                       (operations[3],))
                    connection.commit()
                content=operations[3]+"を作成しました。"
            elif len(operations) >= 3:
                with create_connection() as connection:
                    with connection.cursor() as cursor:
                        cursor.execute("INSERT INTO lottery_table(user_name, lottery_name) VALUES (%s,%s);",
                                       (message.author.name, operations[2]))
                    connection.commit()
                content=operations[2]+"を作成しました。"
        elif operations[1] == "add":
            if len(operations) >= 4:
                with create_connection() as connection:
                    with connection.cursor() as cursor:
                        cursor.execute("INSERT INTO lottery_data(lottery_name, lottery_data) VALUES (%s,%s);",
                                       (operations[2], operations[3]))
                    connection.commit()
        elif operations[1] == "list":
            content="公開くじリスト\n"
            if len(operations) >= 3 and operations[2] == "public":
                with create_connection() as connection:
                    with connection.cursor() as cursor:
                        cursor.execute("SELECT lottery_name from lottery_table where user_name='public'")
                        for index, row in enumerate(cursor):
                            content += index + " | " + row + '\n'
            else:
                content=message.author.name+"の保存済みくじリスト\n"
                with create_connection() as connection:
                    with connection.cursor() as cursor:
                        cursor.execute("SELECT lottery_name from lottery_table where user_name=%s", (message.author.name,))
                        for index, row in enumerate(cursor):
                            content += index + " | " + row + '\n'
        elif operations[1] == "show":
            if len(operations)>=3:
                content=operations[2]+"のデータ\n"
                with create_connection() as connection:
                    with connection.cursor() as cursor:
                        cursor.execute("SELECT lottery_data from lottery_data where lottery_name=%s and user_name=%s", (operations[2],message.author.name,))
                        for index, row in enumerate(cursor):
                            content += index + " | " + row + '\n'
    if content != "":
        await message.channel.send(content)


@client.event
async def on_message(message):
    if message.author.bot:
        return
    if client.user in message.mentions:
        await reply(message)


client.run(token)
