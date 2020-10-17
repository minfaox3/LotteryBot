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
        if operations[1] == "help" or operations[1]=='h':
            content="```" \
                    "ランダム数字：run 下限 上限" \
                    "公開くじをひく(数字には引きたいくじのid)：run public @数字" \
                    "自分のくじをひく(数字には引きたいくじのid)：run @数字" \
                    "公開くじを作成する：create public くじの名前" \
                    "自分のくじを作成する：create くじの名前" \
                    "公開くじにデータを追加する：add " \
                    "自分のくじにデータを追加する："  \
                    "```"
        elif operations[1] == "run":
            if len(operations) >= 3 and operations[2][0] == '@' and operations[2][1:].isdigit():
                content = operations[2][1:]
            elif len(operations) >= 3 and operations[2]=="public" and operations[3][0] == '@' and operations[3][1:].isdigit():
                content = operations[3][1:]
            elif len(operations) >= 4 and operations[2].isdigit() and operations[3].isdigit():
                content = random.randint(int(operations[2]), int(operations[3]))
        elif operations[1] == "create":
            if len(operations) >= 4 and operations[2] == "public":
                with create_connection() as connection:
                    with connection.cursor() as cursor:
                        cursor.execute("INSERT INTO lottery_table(user_name, lottery_name) VALUES ('public', %s);",
                                       (operations[3],))
                    connection.commit()
                content="くじ「"+operations[3]+"」を作成しました。"
            elif len(operations) >= 3:
                with create_connection() as connection:
                    with connection.cursor() as cursor:
                        cursor.execute("INSERT INTO lottery_table(user_name, lottery_name) VALUES (%s,%s);",
                                       (message.author.name, operations[2]))
                    connection.commit()
                content="くじ「"+operations[2]+"」を作成しました。"
        elif operations[1] == "add":
            if len(operations) >= 5 and operations[2]=="public":
                with create_connection() as connection:
                    with connection.cursor() as cursor:
                        cursor.execute("INSERT INTO lottery_data(lottery_name, lottery_data, user_name) VALUES (%s,%s,'public');",
                                       (operations[3], operations[4],))
                    connection.commit()
                content="くじ「"+operations[3]+"」に「"+operations[4]+"」を追加しました。"
            elif len(operations) >= 4:
                with create_connection() as connection:
                    with connection.cursor() as cursor:
                        cursor.execute("INSERT INTO lottery_data(lottery_name, lottery_data, user_name) VALUES (%s,%s,%s);",
                                       (operations[2], operations[3],message.author.name))
                    connection.commit()
                content="くじ「"+operations[2]+"」に「"+operations[3]+"」を追加しました。"
        elif operations[1] == "delete":
            if len(operations) >= 5 and operations[2]=="public":
                with create_connection() as connection:
                    with connection.cursor() as cursor:
                        cursor.execute("DELETE FROM lottery_data WHERE user_name='public' and lottery_name=%s and lottery_data=%s);",
                                       (operations[3], operations[4],))
                    connection.commit()
                content="くじ「"+operations[3]+"」から「"+operations[4]+"」を削除しました。"
            elif len(operations) >= 4:
                with create_connection() as connection:
                    with connection.cursor() as cursor:
                        cursor.execute("DELETE FROM lottery_data WHERE user_name=%s and lottery_name=%s and lottery_data=%s);",
                                       (message.author.name,operations[2], operations[3],))
                    connection.commit()
                content="くじ「"+operations[2]+"」から「"+operations[3]+"」を削除しました。"
        elif operations[1] == "list":
            content="公開くじリスト\n"
            if len(operations) >= 3 and operations[2] == "public":
                with create_connection() as connection:
                    with connection.cursor() as cursor:
                        cursor.execute("SELECT lottery_name from lottery_table where user_name='public'")
                        for row in cursor:
                            content += row[0] + '\n'
                        content+="計:"+str(len(cursor))
            else:
                content=message.author.name+"の保存済みくじリスト\n"
                with create_connection() as connection:
                    with connection.cursor() as cursor:
                        cursor.execute("SELECT lottery_name from lottery_table where user_name=%s", (message.author.name,))
                        for row in cursor:
                            content += row[0] + '\n'
                        content+="計:"+str(len(cursor))
        elif operations[1] == "show":
            if len(operations) >= 4 and operations[2] == "public":
                content = operations[3] + "のデータ\n"
                with create_connection() as connection:
                    with connection.cursor() as cursor:
                        cursor.execute("SELECT id,lottery_data from lottery_data where lottery_name=%s and user_name='public'",
                                       (operations[3],))
                        for index, row in enumerate(cursor):
                            content += row[0] + " | " + row[1] + '\n'
            elif len(operations)>=3:
                content=operations[2]+"のデータ\n"
                with create_connection() as connection:
                    with connection.cursor() as cursor:
                        cursor.execute("SELECT id,lottery_data from lottery_data where lottery_name=%s and user_name=%s", (operations[2],message.author.name,))
                        for index, row in cursor:
                            content += row[0] + " | " + row[1] + '\n'
    if content != "":
        await message.channel.send(content)


@client.event
async def on_message(message):
    if message.author.bot:
        return
    if client.user in message.mentions:
        await reply(message)


client.run(token)
