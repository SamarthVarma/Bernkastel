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

root_url = os.path.dirname(os.getcwd())
config_parser = configparser.ConfigParser()
config_parser.read('bot_config.ini')

config = config(config_parser)
#f = open('AMQ.json',) #VSC takes root as default directory, so take care depending on the situation
#data = json.load(f)
conn = psycopg2.connect(    
            host=config.host,
            database=config.database,
            user=config.user,
            password=config.password
            )

cur = conn.cursor()

