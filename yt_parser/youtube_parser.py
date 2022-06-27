import requests
import sqlite3
import json

# response = requests.get('https://www.youtube.com/c/AzazinKreet/videos')


def check_new_video(yt_chanel: str) -> None:
    response = requests.get(yt_chanel).text.split('"title":{"runs":')\
            [1].split(',')
    video_title = json.loads(response[0][:-1])
    video_url = json.loads(response[5][40:] + '}')
    with sqlite3.connect('chanels.db') as con:
        cur = con.cursor()
        cur.execute("SELECT last_video_title FROM chanels\
                WHERE yt_chanel=:chanel", {"chanel": yt_chanel})
        db_title = cur.fetchone()
        if db_title != video_title:
            try:
                cur.execute("UPDATE chanels SET last_video_title=:title\
                        WHERE last_video_title=:old_title",\
                        {"title": video_title,\
                        "old_title": db_title})
                con.commit()
            except:
                print('Не удалось обновить данные')
        else:
            return


def save_chanels(ds_chanel: str, yt_chanel: str):
    with sqlite3.connect('chanels.db') as con:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS chanels\
                (dc_chanel text, yt_chanel text,\
                last_video_title text, last_video_url text)")
        cur.execute("INSERT INTO chanels VALUES (?,?)",\
                (ds_chanel, yt_chanel))
    check_new_video(yt_chanel)