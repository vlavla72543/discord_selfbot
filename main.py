from time import sleep
import schedule
from config import settings, engine, bot
from threading import Thread
from yt_parser.youtube_parser import save_channels, start_timer, event_data


timer = Thread(target=start_timer, name='start_timer')
timer.start()


def start_timer1():
    while True:
        schedule.run_pending()
        sleep(1)


timer1 = Thread(target=start_timer1, name='start_timer')
timer1.start()


schedule.every(40).seconds.do(bot.dispatch, 'timer_event', bot, event_data)


@bot.event
async def on_timer_event(bot, event_data):
    if event_data:
        for data in event_data:
            for channel in data[0]:
                ctx = bot.get_channel(int(channel))
                await ctx.send(data[1])


@bot.event
async def on_ready():
    print(f'We have logged in as {bot}')


# TODO Добавить инфу о командах


@bot.command()
async def test(ctx):
    urls = ctx.message.content.split(' ')
    ds_channel = str(ctx.message.channel.id)
    yt_channels = []
    for url in urls[1:]:
        if url.startswith('https://www.youtube.com/') and url.count('/') == 4: # TODO переделать проверку url
            yt_channels.append(url + '/videos')
        else:
            await ctx.send('Ссылка указана неверно')
    save_channels(ds_channel=ds_channel, yt_channels=yt_channels, engine=engine)

bot.run(settings['token'], bot=False)










