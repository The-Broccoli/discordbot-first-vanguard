from configparser import ConfigParser

import discord
from core.logging_handler import UserLoggingHandler
from discord.ext import commands


class Ping(commands.Cog, name="Ping"):
    """Simple ping command to test responses and permissions of the bot"""

    def __init__(self, bot: commands.Bot):
        self.log = UserLoggingHandler('ping')
        self.bot = bot

        # Load config
        file = 'config.ini'
        self.config = ConfigParser()
        self.config.read(file)
        del file

    @commands.command()
    async def ping(self, ctx: commands.Context):
        """the bot responds to this command "pong" if the user has the "bot_commander" role"""
        # command sequence
        self.log.info(f'[{ctx.author}] called command ping')
        try:
            for i in ctx.author.roles:
                if i.id == int(self.config['role']['bot_commander']):
                    """Checks for a response from the Bot"""
                    await ctx.send(f'{ctx.message.author.mention}\nPong! {round(self.bot.latency * 1000)}ms')
            # await ctx.message.delete() # Delete message, does this make sense ?
        except Exception as e:
            errorEmbed = discord.Embed(title='Something went wrong!',
                                        description=f'**This command is not available here**\n||{e}||',
                                        color=discord.Color.red())
            await ctx.send(embed=errorEmbed)
            self.log.warning(f'[{ctx.author}] Error by ping command ({e})')

def setup(bot: commands.Bot):
    bot.add_cog(Ping(bot))
