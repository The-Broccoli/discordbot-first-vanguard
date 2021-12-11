from configparser import ConfigParser

from discord.ext import commands


class Ping(commands.Cog, name="Ping"):
    """Simple ping command to test responses and permissions of the bot"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        # Load config
        file = 'config.ini'
        self.config = ConfigParser()
        self.config.read(file)
        del file

    @commands.command()
    async def ping(self, ctx: commands.Context):
        """the bot responds to this command "pong" if the user has the "bot_commander" role"""
        try:
            for i in ctx.author.roles:
                if i.id == int(self.config['role']['bot_commander']):
                    """Checks for a response from the Bot"""
                    await ctx.send(f'{ctx.message.author.mention}\nPong! {round(self.bot.latency * 1000)}ms')
        except Exception as e:
            await ctx.send('Something went wrong! - This command is not available here')

def setup(bot: commands.Bot):
    bot.add_cog(Ping(bot))
