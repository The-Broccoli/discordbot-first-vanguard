#!/usr/bin/python

import os
from configparser import ConfigParser

import discord
from discord.ext import commands


def main():

    # Load config
    file = 'config.ini'
    config = ConfigParser()
    config.read(file)
    del file

    intents = discord.Intents.all()
    client = commands.Bot(command_prefix=">", intents=intents)

    # Ready message
    @client.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(client))
        await client.change_presence(activity=discord.Game(name=">help"))

    # Load cogs
    for folder in os.listdir("modules"):
        if os.path.exists(os.path.join('modules', folder, 'cog.py')):
            client.load_extension(f'modules.{folder}.cog')

    client.run(config.get('bot_info', 'token'))


if __name__ == '__main__':
    main()
