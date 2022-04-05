# インストールした discord.py を読み込む
from enum import Flag
# from tkinter import N
import discord
import random
import re

from os import getenv

# 自分のBotのアクセストークンに置き換えてください
TOKEN = getenv('DISCORD_BOT_TOKEN')

# 接続に必要なオブジェクトを生成
client = discord.Client()

from email import message
import gspread

# ServiceAccountCredentials：Googleの各サービスへアクセスできるservice変数を生成します。
from oauth2client.service_account import ServiceAccountCredentials

# 2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

# 認証情報設定
# ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'nita-bot-ae316e898c9d.json', scope)

# OAuth2の資格情報を使用してGoogle APIにログインします。
gc = gspread.authorize(credentials)

# 共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
SPREADSHEET_KEY = '1GPGg9N6-KPyX1fFUtgt_5fzobqb7o2F3a4Zn6HZo3gg'

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    
    if message.content == '/nitahow':
        await message.channel.send(
            "--本botの使い方 登録削除--\n・初期設定\n/nita-userset\n\n・登録\n/nitas track time name\n例: /nitaset 1 200000 そーすけ (そーすけのマリカスが2:00.000の場合)\n\n・削除\n/nitad track name\n(例: /nitad 1 そーすけ)\n\n・記録はここから見れます！\nhttps://docs.google.com/spreadsheets/d/1GPGg9N6-KPyX1fFUtgt_5fzobqb7o2F3a4Zn6HZo3gg/edit?usp=sharing\n\ntrackは下記を参考\nパリ49|キノサ50|うん山51|ココモ52|東京53|キノリ54|GBAスカ55|ニンニン56\nhttps://cdn.discordapp.com/attachments/949955031552114708/952426641374720021/1-48R_trackList.png"
        )

    # /nassy と言ったらなっしーさんのしょうもないダジャレが聞けます
    if message.content == '/nassy':
        dazyare = [
            "言い訳は言い訳？\nhttps://twitter.com/nanako_mk/status/1498711214842519555?s=21",
            "サンダー誰だ？ ななこさんだー\nhttps://twitter.com/nanako_mk/status/1497967069752479745?s=21",
            "そんなバナナ\nhttps://twitter.com/nanako_mk/status/1497084622794289152?s=21",
            "相方コインとってコイン！\nhttps://twitter.com/nanako_mk/status/1489662815593910272?s=21",
            "スタダミスっただー\nhttps://twitter.com/nanako_mk/status/1497966486006030339?s=21",
            "たんたんが間に合ったんたん\nhttps://twitter.com/nanako_mk/status/1495043157188558851?s=21",
            "4とったよーん\nhttps://twitter.com/nanako_mk/status/1493301824677289984?s=21",
            "ツルツルツイルスター\nhttps://cdn.discordapp.com/attachments/949955031552114708/952426186863153193/unknown.png",
            "I have a harbor.\nhttps://twitter.com/nanako_mk/status/1477750319870521344?s=21",
            "イカ!? それは行かんなあ\nhttps://twitter.com/nanako_mk/status/1488569454090801154?s=21",
            "交流戦で俺の布団ば吹っ飛んだってね\nhttps://twitter.com/nanako_mk/status/1482770006995726336?s=21",
            "赤スルーするんだ\nhttps://twitter.com/nanako_mk/status/1480211177716477953?s=21"
            ]
        await message.channel.send(random.choice(dazyare))
    
    pattern = re.compile(r'\A/nitas')
    if pattern.search(message.content):
        worksheet = gc.open_by_key(SPREADSHEET_KEY).worksheet('List')
        input_sample = message.content.split()
        input_sample.pop(0)

        input_sample[0] = int(input_sample[0])
        input_sample[1] = int(input_sample[1])

        await message.channel.send(input_sample[2])

        data = str(int(worksheet.acell('A1').value) + 1)

        flag = True
        
        reply = ""
        range_user = worksheet.range('A2:A' + data)
        
        for i in range(len(range_user)):
            #print(str(str(range_user[i].value) == str(input_sample[2])))
            #print(str(range_user[i].value))
            #print(str(input_sample[2]))
            if (str(range_user[i].value) == str(input_sample[2])):
                flag = False
                print(worksheet.cell(i + 2, input_sample[0] * 2).value)
                target_cell = worksheet.cell(i + 2, input_sample[0] * 2).value
                print(input_sample)
                if(not(bool(target_cell))):
                    worksheet.update_cell(i + 2, input_sample[0] * 2, input_sample[1])
                    reply = "記録を追加しました。"
                    break
                if(int(target_cell) > input_sample[1]):
                    worksheet.update_cell(i + 2, input_sample[0] * 2, input_sample[1])
                    reply = "記録を更新しました。"
                else:
                    reply = "それより高い記録があったので更新しませんでした。"
                break
        if(flag):
            reply = "そんなuserいないよ？"
        await message.channel.send(reply)


    pattern = re.compile(r'\A/nitad')
    if pattern.search(message.content):
        worksheet = gc.open_by_key(SPREADSHEET_KEY).worksheet('List')
        input_sample = message.content.split()
        input_sample.pop(0)

        input_sample[0] = int(input_sample[0])

        await message.channel.send(input_sample[1])

        flag = True
         
        data = str(int(worksheet.acell('A1').value) + 1)
        
        reply = ""
        range_user = worksheet.range('A2:A' + data)
        
        for i in range(len(range_user)):
            #print(str(str(range_user[i].value) == str(input_sample[2])))
            #print(str(range_user[i].value))
            #print(str(input_sample[2]))
            if (str(range_user[i].value) == str(input_sample[1])):
                flag = False
                worksheet.update_cell(i + 2, input_sample[0] * 2, "")
                reply = "記録を削除しました"
                break
        if(flag):
            reply = "そんなuserいないよ？"
        await message.channel.send(reply)
    
    
    pattern = re.compile(r'\A/nita-userset')
    if pattern.search(message.content):
        worksheet = gc.open_by_key(SPREADSHEET_KEY).worksheet('List')
        input_sample = message.content.split()
        input_sample.pop(0)

        data = str(int(worksheet.acell('A1').value) + 1)

        flag = True

        data = str(int(worksheet.acell('A1').value) + 1)
        
        reply = ""
        range_user = worksheet.range('A2:A' + data)

        for i in range(len(range_user)):
            if (str(range_user[i].value) == str(input_sample[0])):
                flag = False
                reply = "userがもう登録されています。"
                break
        if(flag):
            worksheet.update_acell("A1", int(data))
            worksheet.update_cell(int(data) + 1, 1, input_sample[0])
            reply = "userを登録しました。"
        await message.channel.send(reply)


# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
