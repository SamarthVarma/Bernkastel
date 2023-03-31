from asyncio.tasks import sleep
import discord
from discord.ext import commands
import asyncio
import configparser
from initialize import *
import psycopg2
import json
import os
import csv
from datetime import datetime

root_url = os.path.dirname(os.getcwd())
config_parser = configparser.ConfigParser()
config_parser.read('bot_config.ini')
print(root_url)
url = os.path.join(root_url, 'bernkastel\\assets') 

config = config(config_parser)
conn = psycopg2.connect(    
            host=config.host,
            database=config.database,
            user=config.user,
            password=config.password
            )

cur = conn.cursor()

class Bot(commands.Bot):
    def __init__(self, activity):
        super().__init__(command_prefix=commands.when_mentioned_or('$!$'), intents = discord.Intents.all(), activity = activity)

    async def on_ready(self):
        channel = bern.get_channel(829406490934116403) 
        print(f'Logged in as {bern.user} (ID: {bern.user.id})')
        myfile = discord.File(os.path.join(url,f"nipah.gif"))
        await channel.send(file=myfile)

activity = discord.Activity(type=discord.ActivityType.listening, name="The Executioner")
bern = Bot(activity)

bern.run(config.token)