from messages.generel import GenerelMessages
from core.logging_handler import UserLoggingHandler
from core.general_functions import GeneralFunctions
from discord.ext import commands


class Ping(commands.Cog, name="Ping"):
    """Simple ping command to test responses and permissions of the bot"""

    def __init__(self, bot: commands.Bot):
        self.log = UserLoggingHandler('ping')
        self.g_embed = GenerelMessages(bot)
        self.bot = bot
        self.pingTitele = 'Ping'

    @commands.command()
    async def ping(self, ctx: commands.Context):
        """the bot responds to this command "pong" if the user has the "bot_commander" role"""
        # Load config
        self.config = GeneralFunctions(self.bot).load_config()
        # command sequence
        self.log.info(f'[{ctx.author}] called command ping')
        if GeneralFunctions(self.bot).user_authorization(ctx, self.config['role']['bot_commander']):
            # Checks for a response from the Bot
            try:
                # ctx.reply()
                await ctx.send(f'{ctx.message.author.mention}\nPong! {round(self.bot.latency * 1000)}ms')
            except Exception as e:
                eembed = self.g_embed(self.pingTitele, e)
                await ctx.send(embed=eembed)
                self.log.warning(f'[{ctx.author}] Error by ping command ({e})')
        else:
            pass


def setup(bot: commands.Bot):
    bot.add_cog(Ping(bot))
