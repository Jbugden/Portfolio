import discord
from discord.ext import commands
import config 
import asyncio
import pandas as pd
from discord import File
import dataframe_image as dfi
import io

class discord_bot:

    def __init__(self):
        
        # Getting tokens and ids from config file
        self.bot_token = config.TOKEN
        self.guild_id = config.GUILD_ID
        self.channel_id = config.CHANNEL_ID


        # setting intents 
        intents = discord.Intents.default()
        intents.typing = False
        intents.presences = False

        # initialise a client for discord and pass the intents
        self.client = discord.Client(intents=intents)
        

    # Function to send a message through Discord
    def send_message(self, content):
        @self.client.event
        async def on_ready():
            guild = self.client.get_guild(self.guild_id)
            channel = guild.get_channel(self.channel_id)
            await channel.send(content)
            await self.client.close()

        self.client.run(self.bot_token)

    # send image 
    def send_image(self, df):
        @self.client.event
        async def on_ready():
            guild = self.client.get_guild(self.guild_id)
            channel = guild.get_channel(self.channel_id)
            
            buffer = io.BytesIO()
            dfi.export(df,buffer)
            buffer.seek(0)

            file = File(buffer, filename='image.png')

            await channel.send(file=file)
            await self.client.close()

        self.client.run(self.bot_token)

    def convert_df_to_image(self,df):
        buffer = io.BytesIO()
        dfi.export(df,buffer)
        buffer.seek(0)
        file = File(buffer, filename='image.png')
        return file

    def send_investment_message(self,df,mkt,message):
        @self.client.event
        async def on_ready():
            guild = self.client.get_guild(self.guild_id)
            channel = guild.get_channel(self.channel_id)
            
            portfolio =self.convert_df_to_image(df)
            await channel.send(file=portfolio)

            market =self.convert_df_to_image(mkt)
            await channel.send(file=market)

            await channel.send(message)

            await self.client.close()

        self.client.run(self.bot_token)
    
