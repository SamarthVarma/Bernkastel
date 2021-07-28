import discord
from discord.ext import commands
import asyncio
import configparser
from initialize import *

config_parser = configparser.ConfigParser()
config_parser.read('bot_config.ini')

config = config(config_parser)

class Bot(commands.Bot):
    def __init__(self, activity):
        super().__init__(command_prefix=commands.when_mentioned_or('$!$'), intents = discord.Intents.all(), activity = activity)

    async def on_ready(self):
        channel = bern.get_channel(config.log_ch) 
        await channel.send(f'Logged in as {bern.user} (ID: {bern.user.id})')

class Options(discord.ui.Button):
    def __init__(self,option,y,optnumber):
        super().__init__(style=discord.ButtonStyle.secondary, label=option, row=1)
        self.option = option
        self.optnumber = optnumber + 1
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'You Selected {self.option}, {self.optnumber}', ephemeral=True)


class Question(discord.ui.View):
    def __init__(self, options):
        super().__init__(timeout=5.0)
        self.options = options
        for x in range (2):
            for y in range(2):
                self.add_item(Options(self.options[y + 2*x],y, y + 2*x))
        self.v = self.children
    
    def disable(self):
        for item in self.children:
            if(item.optnumber == 2): item.style = discord.ButtonStyle.success
            else : item.style = discord.ButtonStyle.danger
            item.disabled = True
        return self

    async def refresh_message(self):
            self.message: discord.Message
            await self.message.edit(view=self)
    
    async def on_timeout(self):
        self.disable()
        await self.refresh_message()


activity = discord.Activity(type=discord.ActivityType.listening, name="Hapiness of Marionette")
bern = Bot(activity)

@bern.command(name='ok')
async def sendmp(ctx):
    myfile = discord.File('C:/Users/Samarth/Documents/Github-Repo/discord bot testing/sample1.mp3')
    option = ["Attack on Titan","Sword Art Online","Gundam 79", "Shinsekai Yori"]
    v = Question(option)
    v.message = await ctx.send(file=myfile, view=v)

bern.run(config.token)