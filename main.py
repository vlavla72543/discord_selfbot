import discord
from config import settings, engine, bot
from threading import Thread
from yt_parser.youtube_parser import save_channels, start_timer
from discord.ext import commands


timer = Thread(target=start_timer, name='start_timer')
timer.start()


@bot.event
async def on_ready():
    print(f'We have logged in as {bot}')


@bot.command()
async def info(ctx):
    await ctx.send('uoeu')


@bot.command()
async def test(ctx):
    urls = ctx.message.content.split(' ')
    ds_channel = str(ctx.message.channel.id)
    yt_channels = []
    for url in urls[1:]:
        if url.startswith('https://www.youtube.com/') and url.count('/') == 4:
            yt_channels.append(url + '/videos')
        else:
            await ctx.send('Ссылка указана неверно')
    save_channels(ds_channel=ds_channel, yt_channels=yt_channels, engine=engine)

bot.run(settings['token'], bot=False)
