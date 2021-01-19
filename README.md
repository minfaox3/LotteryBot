# くじ引きBot(LotteryBot)
## 情報(Information)
* 最終更新日(Last updated): 2021/01/19
    * Readmeの充実
* メンテナー(Maintainer): minfaox3(spdlci30@gmail.com)
* ライセンス(License): Creative Commons Zero v1.0 Universal(CC0)
* プログラミング言語(Language)： python 3.8.6
* 使用外部モジュール(Third party modules)
    * aiohttp 3.6.3
    * async-timeout 3.0.1
    * attrs 20.2.0
    * chardet 3.0.4
    * discord.py 1.5.0
    * idna 2.10
    * multidict 4.7.6
    * psycopg2 2.8.6
    * yarl 1.5.1
 * 使用データベース(Used DataBase): PostgreSQL
 
## 説明(Description)
これはDiscordサーバー上でくじ引きができるようになるBotのソースコードです。
内容はBotサーバーのデータベースに保存されるので、チャットのピン止めなどにごみは残りません。
このソースはそのままHeroku+PostgreSQL上で動作します。(環境変数はHerokuダッシュボードから設定してください。)

## 導入方法(Installation)
