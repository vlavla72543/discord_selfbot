import discord
from discord.ext import commands
from config import settings
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from Database.db_model import Base
from yt_parser.youtube_parser import save_channels

bot = commands.Bot(command_prefix=settings['prefix'])
engine = create_engine('sqlite:///Database/YtParser.db')
if not database_exists(engine.url):
    create_database(engine.url)
    Base.metadata.create_all(engine)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot}')


@bot.command()
async def info(ctx):
    await ctx.send('')


@bot.command()
async def test(ctx):
    urls = ctx.message.content.split(' ')
    yt_channels = []
    for url in urls[1:]:
        if url.startswith('https://www.youtube.com/') and url.count('/') == 4:
            yt_channels.append(url + '/videos')
        else:
            await ctx.send('Ссылка указана неверно')
    save_channels(ds_channel=ctx.message.channel.id, yt_channels=yt_channels, engine=engine)

bot.run(settings['token'], bot=False)
