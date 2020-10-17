from psycopg2.extras import DictCursor
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
            content="```\n" \
                    "**ひく**\n" \
                    "ランダム数字：run 下限 上限\n" \
                    "公開くじをひく(数字には引きたいくじのid)：run public @数字\n" \
                    "自分のくじをひく(数字には引きたいくじのid)：run @数字\n" \
                    "**つくる**\n" \
                    "公開くじを作成する：create public くじの名前\n" \
                    "自分のくじを作成する：create くじの名前\n" \
                    "**ついかする**\n" \
                    "公開くじにデータを追加する：add public くじid データ\n" \
                    "自分のくじにデータを追加する：add くじid データ\n" \
                    "**けす**\n" \
                    "公開くじのデータを削除する：delete public くじid データid\n" \
                    "自分のくじのデータを削除する：delete くじid データid\n" \
                    "**みる**\n" \
                    "公開くじのリストを見る：list public\n" \
                    "自分のリストを見る：list\n" \
                    "公開くじのデータを見る：show public くじid\n" \
                    "自分のくじのデータを見る：show くじid\n"  \
                    "```"
        elif operations[1] == "run":
            if len(operations) >= 3 and operations[2][0] == '@' and operations[2][1:].isdigit():
                data = list()
                with create_connection() as connection:
                    with connection.cursor() as cursor:
                        cursor.execute("SELECT lottery_value from lottery_data where lottery_id=%s and user_name=%s",
                                       (operations[2][1:],message.author.name))
                        for row in cursor:
                            data.append(row[0])
                content = str(data[random.randint(0,len(data)-1)])
            elif len(operations) >= 3 and operations[2]=="public" and operations[3][0] == '@' and operations[3][1:].isdigit():
                data = list()
                with create_connection() as connection:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "SELECT lottery_value from lottery_data where lottery_id=%s and user_name='public'",
                            (operations[3][1:],))
                        for row in cursor:
                            data.append(row[0])
                content = str(data[random.randint(0, len(data) - 1)])
            elif len(operations) >= 4 and operations[2].isdigit() and operations[3].isdigit():
                content = random.randint(int(operations[2]), int(operations[3]))
        elif operations[1] == "create":
            if len(operations) >= 4 and operations[2] == "public":
                with create_connection() as connection:
                    with connection.cursor() as cursor:
                        cursor.execute("INSERT INTO lottery_table(user_name, lottery_name) VALUES ('public', %s);",
                                       (operations[3],))
                    connection.commit()
                content="公開くじ「"+operations[3]+"」を作成しました。"
            elif len(operations) >= 3:
                with create_connection() as connection:
                    with connection.cursor() as cursor:
                        cursor.execute("INSERT INTO lottery_table(user_name, lottery_name) VALUES (%s,%s);",
                                       (message.author.name, operations[2]))
                    connection.commit()
                content="自分のくじ「"+operations[2]+"」を作成しました。"
        elif operations[1] == "add":
            if len(operations) >= 5 and operations[2]=="public":
                if ',' in operations[4]:
                    values = operations[4].split(',')
                    for value in values:
                        with create_connection() as connection:
                            with connection.cursor() as cursor:
                                cursor.execute(
                                    "INSERT INTO lottery_data(lottery_id, lottery_value, user_name) VALUES (%s,%s,'public');",
                                    (operations[3], value,))
                            connection.commit()
                        content = "公開くじ「" + operations[3] + "」に「" + value + "」を追加しました。\n"
                else:
                    with create_connection() as connection:
                        with connection.cursor() as cursor:
                            cursor.execute(
                                "INSERT INTO lottery_data(lottery_id, lottery_value, user_name) VALUES (%s,%s,'public');",
                                (operations[3], operations[4],))
                        connection.commit()
                    content = "公開くじ「" + operations[3] + "」に「" + operations[4] + "」を追加しました。"
            elif len(operations) >= 4:
                if ',' in operations[3]:
                    values = operations[3].split(',')
                    for value in values:
                        with create_connection() as connection:
                            with connection.cursor() as cursor:
                                cursor.execute(
                                    "INSERT INTO lottery_data(lottery_id, lottery_value, user_name) VALUES (%s,%s,%s);",
                                    (operations[2], value, message.author.name))
                            connection.commit()
                        content = "自分のくじ「" + operations[2] + "」に「" + value + "」を追加しました。\n"
                else:
                    with create_connection() as connection:
                        with connection.cursor() as cursor:
                            cursor.execute(
                                "INSERT INTO lottery_data(lottery_id, lottery_value, user_name) VALUES (%s,%s,%s);",
                                (operations[2], operations[3], message.author.name))
                        connection.commit()
                    content = "自分のくじ「" + operations[2] + "」に「" + operations[3] + "」を追加しました。"
        elif operations[1] == "delete":
            if len(operations) >= 5 and operations[2]=="public":
                if ',' in operations[4]:
                    values = operations[4].split(',')
                    for value in values:
                        with create_connection() as connection:
                            with connection.cursor() as cursor:
                                cursor.execute(
                                    "DELETE FROM lottery_data WHERE user_name='public' and lottery_id=%s and id=%s);",
                                    (operations[3], value,))
                            connection.commit()
                        content = "公開くじ「" + operations[3] + "」から「" + value + "」を削除しました。\n"
                else:
                    with create_connection() as connection:
                        with connection.cursor() as cursor:
                            cursor.execute("DELETE FROM lottery_data WHERE user_name='public' and lottery_id=%s and id=%s);",
                                           (operations[3], operations[4],))
                        connection.commit()
                    content="公開くじ「"+operations[3]+"」から「"+operations[4]+"」を削除しました。"
            elif len(operations) >= 4:
                if ',' in operations[3]:
                    values = operations[3].split(',')
                    for value in values:
                        with create_connection() as connection:
                            with connection.cursor() as cursor:
                                cursor.execute(
                                    "DELETE FROM lottery_data WHERE user_name=%s and lottery_id=%s and id=%s);",
                                    (message.author.name, operations[2], value,))
                            connection.commit()
                        content = "自分のくじ「" + operations[2] + "」から「" + value + "」を削除しました。\n"
                else:
                    with create_connection() as connection:
                        with connection.cursor() as cursor:
                            cursor.execute("DELETE FROM lottery_data WHERE user_name=%s and lottery_id=%s and id=%s);",
                                           (message.author.name, operations[2], operations[3],))
                        connection.commit()
                    content = "自分のくじ「" + operations[2] + "」から「" + operations[3] + "」を削除しました。"
        elif operations[1] == "list":
            if len(operations) >= 3 and operations[2] == "public":
                length=0
                content="公開くじリスト\nid | くじ名\n"
                with create_connection() as connection:
                    with connection.cursor(cursor_factory=DictCursor) as cursor:
                        cursor.execute("SELECT * from lottery_table where user_name='public'")
                        for row in cursor:
                            content += str(row["id"]) + " | " + str(row["lottery_name"]) + '\n'
                            length+=1
                        content+="計:"+str(length)
            else:
                length=0
                content=message.author.name+"の保存済みくじリスト\nid | くじ名\n"
                with create_connection() as connection:
                    with connection.cursor(cursor_factory=DictCursor) as cursor:
                        cursor.execute("SELECT * from lottery_table where user_name=%s", (message.author.name,))
                        for row in cursor:
                            content += str(row["id"]) + " | " + str(row["lottery_name"]) + '\n'
                            length+=1
                        content+="計:"+str(length)
        elif operations[1] == "show":
            if len(operations) >= 4 and operations[2] == "public":
                length=0
                content = "公開くじ「"+operations[3] + "」のデータ\nid | データ内容\n"
                with create_connection() as connection:
                    with connection.cursor(cursor_factory=DictCursor) as cursor:
                        cursor.execute("SELECT * from lottery_data where lottery_id=%s and user_name='public'",
                                       (operations[3],))
                        for row in cursor:
                            content += str(row["id"]) + " | " + str(row["lottery_value"]) + '\n'
                            length+=1
                        content+="計:"+str(length)
            elif len(operations)>=3:
                length=0
                content=message.author.name+"のくじ「"+operations[2]+"」のデータ\nid | データ内容\n"
                with create_connection() as connection:
                    with connection.cursor(cursor_factory=DictCursor) as cursor:
                        cursor.execute("SELECT * from lottery_data where lottery_id=%s and user_name=%s", (operations[2],message.author.name,))
                        for row in cursor:
                            content += str(row["id"]) + " | " + str(row["lottery_value"]) + '\n'
                            length+=1
                        content+="計:"+str(length)
    if content != "":
        await message.channel.send(content)


@client.event
async def on_message(message):
    if message.author.bot:
        return
    if client.user in message.mentions:
        await reply(message)


client.run(token)
