import requests
import json
from sqlalchemy import select
from sqlalchemy.orm import Session
from Database.db_model import YtParser

# response = requests.get('https://www.youtube.com/c/AzazinKreet/videos')


def check_new_video(yt_channel: str, engine) -> None:
    response = requests.get(yt_channel).text.split('"title":{"runs":')[1].split('"')
    video_title = response[response.index('text') + 2]
    video_url = response[response.index('url') + 2]
    with Session(engine) as session:
        db_video_title = session.execute(select(YtParser.video_title).where(YtParser.yt_channel == yt_channel))
        if db_video_title != video_title:
            video_url = 'https://www.youtube.com' + video_url
            result = session.execute(select(YtParser).where(YtParser.yt_channel == yt_channel)).scalar_one()
            result.video_title = video_title
            result.video_url = video_url
            session.commit()
        else:
            return


def save_channels(ds_channel: str, yt_channel: str, engine) -> None:
    with Session(engine) as session:
        data = YtParser(                # TODO Сделать проверку на повторяющиеся каналы
            yt_channel=yt_channel,
            ds_channel=ds_channel
        )
        session.add(data)
        session.commit()
    check_new_video(yt_channel, engine)
    return
