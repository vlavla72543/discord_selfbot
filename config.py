from sqlalchemy import create_engine
from discord.ext import commands
from discord import Activity, ActivityType

engine = create_engine('sqlite:///Database/YtParser.db', )

activity = Activity(type=ActivityType.watching, name="vla!info")

settings = {
    'prefix': 'vla!',
    'token': 'token',
}

bot = commands.Bot(command_prefix=settings['prefix'], activity=activity)
