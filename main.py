from time import sleep
import requests
import schedule
from config import settings, engine, bot
from threading import Thread
from yt_parser.youtube_parser import save_channels, check_new_video
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import Session
from sqlalchemy import select
from Database.db_model import Base, YtParser


if not database_exists(engine.url):
    create_database(engine.url)
    Base.metadata.create_all(engine)


def start_timer1():
    while True:
        schedule.run_pending()
        sleep(1)


timer1 = Thread(target=start_timer1, name='start_timer_event')
timer1.start()


schedule.every(30).seconds.do(bot.dispatch, 'timer_event', engine, bot)


@bot.event
async def on_timer_event(engine, bot) -> None:
    with Session(engine) as session:
        result = session.execute(select(YtParser.yt_channel)).scalars().all()
        for data in check_new_video(result, session):
            for channel in data[0]:
                ctx = bot.get_channel(int(channel))
                await ctx.send(data[1])


@bot.event
async def on_ready():
    print(f'We have logged in as {bot}')


@bot.command()
async def info(ctx):
    await ctx.send('```доступные команды\n   vla!track (ссылка на ютуб канал/каналы)\n   пример: '
                   'vla!track https://www.youtube.com/c/abc https://www.youtube.com/channel/abc2```\n```На '
                   'пропитание\n   BTC: 3NnyGcFhE2hNPGe9movtxxk47w3Gq7tpmk```')


@bot.command()
async def track(ctx):
    urls = ctx.message.content.split(' ')
    ds_channel = str(ctx.message.channel.id)
    yt_channels = []
    for url in urls[1:]:
        if url.endswith('/featured'):
            url = url[:-9]
        if url.startswith('https://www.youtube.com/') and url.count('/') == 4 and 200 == requests.get(url).status_code:
            yt_channels.append(url + '/videos')
        else:
            await ctx.send(f'```Ссылка "{url}" указана неверно```')
            sleep(1)
    if yt_channels:
        await ctx.send(f'```{str(yt_channels)[1:-1]} теперь отслеживаются```')
    save_channels(ds_channel=ds_channel, yt_channels=yt_channels, engine=engine)

bot.run(settings['token'], bot=False)










