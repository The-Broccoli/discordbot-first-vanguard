import discord
from discord.ext import commands


class GenerelMessages():
    """This class creates generel messages for the user (error, wrong argument, ...)"""

    def __init__(self, bot):
        self.bot = bot

    def error(self, commandTitle, error):
        """Returns an error embed for a error message"""
        embed = discord.Embed(title=f'{commandTitle} - Error',
                              description=f'Hier lauft etwas nicht so wie es sein sollte! :sweat:`\n```{error}```',
                              color=discord.Color.red())

        return embed
