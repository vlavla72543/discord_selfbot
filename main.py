from discord import Embed
from discord.ext import commands
from config import settings

bot = commands.Bot(command_prefix=settings['prefix'])


@bot.event
async def on_ready():
    print(f'We have logged in as {bot}')


@bot.command()
async def info(ctx):
    embed = Embed(colour=0xff9900, title='title aboba', description='desk')
    embed.add_field(name='hello', value='cd')
    ctx.message.content = 'aoeu'
    await ctx.send(embed=embed)


bot.run(settings['token'], bot=False)