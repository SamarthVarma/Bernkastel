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
f = open('AMQ.json',) #VSC takes root as default directory, so take care depending on the situation
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
        #channel = bern.get_channel(config.log_ch) 
        print(f'Logged in as {bern.user} (ID: {bern.user.id})')

class Options(discord.ui.Button):
    def __init__(self,option,optnumber):
        super().__init__(style=discord.ButtonStyle.secondary, label=option, row=1)
        self.option = option
        self.optnumber = optnumber + 1
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'You Selected {self.option}', ephemeral=True)
        insert_query = """INSERT INTO question_scoresheet(id, username, score, option) VALUES (%s, %s, %s, %s)ON CONFLICT(id) DO UPDATE SET option = EXCLUDED.option;"""
        vars =  interaction.user.id,interaction.user.name,0,self.optnumber
        cur.execute(insert_query,vars)
        conn.commit()

class Question(discord.ui.View):
    def __init__(self, options):
        super().__init__(timeout=50.0)
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
    
    async def on_timeout(self, correct=10):
        if(correct != 10):
            self.disable(correct)
            await self.refresh_message()


activity = discord.Activity(type=discord.ActivityType.listening, name="The Executioner")
bern = Bot(activity)

@commands.is_owner()
@bern.command(name='AMQ')
async def animeMusicQuiz(ctx):
    url = os.path.join(root_url, 'assets\\AMQ\\')  
    delete_query = """ DELETE FROM main_scoresheet;"""
    cur.execute(delete_query)
    conn.commit()
    delete_query = """ DELETE FROM question_scoresheet;"""
    cur.execute(delete_query)
    conn.commit()
    for i in range(len(data['AMQ'])):
        myfile = discord.File(os.path.join(url,f"Q{i+1}.mp3"))
        option = data['AMQ'][i]['options']
        v = Question(option)
        v.message = await ctx.send(content=data['AMQ'][i]['name'],file=myfile, view=v)
        await asyncio.sleep(35)
        await v.on_timeout(data['AMQ'][i]['answer'])
        await asyncio.sleep(3)
        await ctx.send('----')
        await asyncio.sleep(2)
        cur.execute("""UPDATE question_scoresheet SET score=1 WHERE option=%(value)s;""", {"value": data['AMQ'][i]['answer']})
        conn.commit()
        cur.execute("""INSERT INTO main_scoresheet SELECT id, username, score FROM question_scoresheet ON CONFLICT(id) DO UPDATE SET score = main_scoresheet.score + EXCLUDED.score, username = EXCLUDED.username;""")
        conn.commit()
        cur.execute(""" DELETE FROM question_scoresheet;""")
        conn.commit()
    
    cur.execute("""SELECT * FROM main_scoresheet ORDER BY score DESC""")
    conn.commit()
    result = cur.fetchall();
    embed = discord.Embed(colour=discord.Colour(0x31af14), url="https://discordapp.com")
    embed.set_author(name="RESULTS", url="https://discordapp.com")

    embed.add_field(name="___", value="​", inline = False)
    if(len(result)>0):
        embed.add_field(name="🥇", value=f"```{result[0][1]} (SCORE: {result[0][2]})```", inline = False)
        embed.set_thumbnail(url=ctx.guild.get_member(result[0][0]).avatar.url)
    if(len(result)>1):
        embed.add_field(name="🥈", value=f"```{result[1][1]} (SCORE: {result[1][2]})```", inline = False)
    if(len(result)>2):
        embed.add_field(name="🥉", value=f"```{result[2][1]} (SCORE: {result[2][2]})```", inline = False)

    await ctx.send(embed=embed)
    query = """SELECT RANK () OVER ( ORDER BY score DESC ) rank, username AS name, score FROM main_scoresheet;"""
    cur.execute(query)
    fieldnames = ['Rank','Name','Score']
    with open('result.csv', 'w', newline='', encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(fieldnames)
        for row in cur.fetchall():
            try:
                writer.writerow(row)
            except:
                pass
    conn.commit()
    await ctx.send(content="Complete Results", file=discord.File("result.csv"))

@animeMusicQuiz.error
async def animeMusicQuiz_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('Only Bot Owner can run this command')

bern.run(config.token)