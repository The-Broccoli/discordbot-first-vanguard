from configparser import ConfigParser

import discord
from discord.ext import commands


class Taxes(commands.Cog, name="Taxes"):
    """TODO Taxes cog"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        # Load config
        file = 'config.ini'
        self.config = ConfigParser()
        self.config.read(file)
        del file

    @commands.command()
    async def taxes(self, ctx: commands.Context):
        """TODO Taxes command"""
        try:
            for i in ctx.author.roles:
                if i.id == int(self.config['role']['bot_commander']):
                    """With this command you can start the tax notification"""
                    pass # TODO Sequence of the command
            # await ctx.message.delete() # Delete message, does this make sense ?
        except Exception as e:
            errorEmbed = discord.Embed(title='Something went wrong!',
                                        description=f'**This command is not available here**\n||{e}||',
                                        color=discord.Color.red())
            await ctx.send(embed=errorEmbed)

def setup(bot: commands.Bot):
    bot.add_cog(Taxes(bot))
