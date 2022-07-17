import requests
from time import sleep
from sqlalchemy import select
from sqlalchemy.orm import Session
from Database.db_model import YtParser


def check_new_video(yt_channels: list, session) -> tuple:
    for yt_channel in yt_channels:
        response = requests.get(yt_channel).text.split('"title":{"runs":')[1].split('"')
        sleep(5)
        if not response[response.index('url') + 2].startswith('/watch'):
            continue
        video_title = response[response.index('text') + 2]
        result = session.execute(select(YtParser).where(YtParser.yt_channel == yt_channel)).scalar_one()
        if not result.video_title:
            result.video_title = video_title
            result.video_title2 = video_title
            session.commit()
            continue
        elif result.video_title != video_title:
            if result.video_title2 == video_title:
                result.video_title = video_title
                session.commit()
            else:
                video_url = 'https://www.youtube.com' + response[response.index('url') + 2]
                title = result.video_title
                result.video_title2 = title
                result.video_title = video_title
                data = (result.ds_channel.split(' '), video_url)
                session.commit()
                yield data


def save_channels(ds_channel: str, yt_channels: list, engine) -> None:
    with Session(engine) as session:
        for yt_channel in yt_channels:
            try:
                result = session.execute(select(YtParser).where(YtParser.yt_channel == yt_channel)).scalar_one()
            except:
                data = YtParser(
                    yt_channel=yt_channel,
                    ds_channel=ds_channel
                )
                session.add(data)
            else:
                if ds_channel in result.ds_channel:
                    pass
                else:
                    result.ds_channel += ' ' + ds_channel
        session.commit()
