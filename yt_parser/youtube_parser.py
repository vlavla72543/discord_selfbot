import requests
import sqlite3
import json
from sqlalchemy.orm import Session
from db_model import YtParser

# response = requests.get('https://www.youtube.com/c/AzazinKreet/videos')


def check_new_video(yt_channel: str, engine) -> None:
    response = requests.get(yt_channel).text.split('"title":{"runs":')[1].split(',')
    video_title = json.loads(response[0][:-1])
    video_url = json.loads(response[5][40:] + '}')
    with Session(engine) as session:
        #cur.execute("SELECT last_video_title FROM chanels WHERE yt_chanel=:chanel", {"chanel": yt_chanel})
        #db_title = cur.fetchone()
        if db_title != video_title:
            try:
                #cur.execute("UPDATE chanels SET last_video_title=:title WHERE last_video_title=:old_title",
                            #{"title": video_title, "old_title": db_title})
                #con.commit()
            except:
                print('Не удалось обновить данные')
        else:
            return


def save_channels(ds_channel: str, yt_channel: str, engine):
    with Session(engine) as session:
        data = YtParser(
            yt_channel=yt_channel,
            ds_channel=ds_channel
        )
        session.add(data)
        session.commit()
    check_new_video(yt_channel, engine)
