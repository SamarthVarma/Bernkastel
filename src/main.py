from asyncio.tasks import sleep
import discord
from discord.ext import commands
import asyncio
import configparser
from initialize import *
import psycopg2
import json

config_parser = configparser.ConfigParser()
config_parser.read('bot_config.ini')

config = config(config_parser)
f = open('src/questions.json',) #VSC takes root as default directory, so take care depending on the situation
data = json.load(f)
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
        channel = bern.get_channel(config.log_ch) 
        await channel.send(f'Logged in as {bern.user} (ID: {bern.user.id})')

class Options(discord.ui.Button):
    def __init__(self,option,optnumber):
        super().__init__(style=discord.ButtonStyle.secondary, label=option, row=1)
        self.option = option
        self.optnumber = optnumber + 1
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'You Selected {self.option}, {self.optnumber}, {interaction.user.id}', ephemeral=True)
        insert_query = """INSERT INTO question_scoresheet(id, username, score, option) VALUES (%s, %s, %s, %s)ON CONFLICT(id) DO UPDATE SET option = EXCLUDED.option;"""
        vars =  interaction.user.id,interaction.user.name,0,self.optnumber
        cur.execute(insert_query,vars)
        conn.commit()



class Question(discord.ui.View):
    def __init__(self, options):
        super().__init__(timeout=30.0)
        self.options = options
        for x in range (5):
                self.add_item(Options(self.options[x], x))
        self.v = self.children

    def disable(self, correct):
        for item in self.children:
            if(item.optnumber == correct): item.style = discord.ButtonStyle.success
            else : item.style = discord.ButtonStyle.danger
            item.disabled = True
        return self

    async def refresh_message(self):
            self.message: discord.Message
            await self.message.edit(view=self)
    
    async def on_timeout(self, correct):
        self.disable(correct)
        await self.refresh_message()


activity = discord.Activity(type=discord.ActivityType.listening, name="Hapiness of Marionette")
bern = Bot(activity)

@bern.command(name='ok')
async def sendmp(ctx):
    delete_query = """ DELETE FROM main_scoresheet;"""
    cur.execute(delete_query)
    conn.commit()
    delete_query = """ DELETE FROM question_scoresheet;"""
    cur.execute(delete_query)
    conn.commit()
    for i in range(len(data['AMQ'])):
        myfile = discord.File('C:/Users/Samarth/Documents/Github-Repo/discord bot testing/sample1.mp3')
        option = data['AMQ'][i]['options']
       # option = ["Attack on Titan","Sword Art Online","Gundam 79", "Shinsekai Yori", "Toradora"]
        v = Question(option)
        v.message = await ctx.send(content=data['AMQ'][i]['name'],file=myfile, view=v)
        await asyncio.sleep(10)
        await v.on_timeout(data['AMQ'][i]['answer'])
        cur.execute("""UPDATE question_scoresheet SET score=1 WHERE option=%(value)s;""", {"value": data['AMQ'][i]['answer']})
        conn.commit()
        cur.execute("""INSERT INTO main_scoresheet SELECT id, username, score FROM question_scoresheet ON CONFLICT(id) DO UPDATE SET score = main_scoresheet.score + EXCLUDED.score, username = EXCLUDED.username;""")
        conn.commit()
        cur.execute(""" DELETE FROM question_scoresheet;""")
        conn.commit()

bern.run(config.token)