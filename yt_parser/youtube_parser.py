import requests
import schedule
from sqlalchemy import select
from sqlalchemy.orm import Session
from Database.db_model import YtParser
from time import sleep


def check_new_video(yt_channels: list, engine) -> None:  # TODO возможно добавить сессию в параметры
    for yt_channel in yt_channels:
        sleep(5)  # TODO переместить
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


def save_channels(ds_channel: str, yt_channels: list, engine) -> None:
    with Session(engine) as session:
        for yt_channel in yt_channels:
            result = session.execute(select(YtParser.yt_channel, YtParser.ds_channel)).scalar_one()
            print(result.yt_channel)
            if yt_channel in session.scalars(result.yt_channel) and \
                    ds_channel not in session.scalars(result.ds_channel):
                sql_update_yt = select(YtParser).where(YtParser.yt_channel == yt_channel)
                row = session.scalar(sql_update_yt)
                row.ds_channel = row.ds_channel + ',' + str(ds_channel)
            else:
                data = YtParser(
                    yt_channel=yt_channel,
                    ds_channel=ds_channel
                )
                session.add(data)
        session.commit()
    check_new_video(yt_channel, engine)
    return


def yt_parser_timer(engine) -> None:
    with Session(engine) as session:
        result = session.execute(select(YtParser.yt_channel)).scalars().all()
        print(len(result))
        # for data in result:
        #    print(data)
