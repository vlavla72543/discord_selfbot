import discord
from discord import Embed
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
    embed = Embed(colour=0xff9900, title='title aboba', description='desk')
    embed.add_field(name='hello', value='cd')
    ctx.message.content = 'aoeu'
    await ctx.send(embed=embed)


@bot.command()
async def test(ctx):
    url = ctx.message.content.split(' ')
    if url[1].startswith('https://www.youtube.com/'):
        save_channels(ds_channel=ctx.message.channel.id, yt_channel=url[1], engine=engine)


bot.run(settings['token'], bot=False)
