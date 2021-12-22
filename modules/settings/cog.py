from configparser import ConfigParser

import discord
from core.logging_handler import UserLoggingHandler
from core.general_functions import GeneralFunctions
from discord.ext import commands


class Settings(commands.Cog, name="Settings"):
    """TODO"""

    def __init__(self, bot: commands.Bot):
        self.log = UserLoggingHandler('settings')
        self.bot = bot

        # Load config
        file = 'config.ini'
        self.config = ConfigParser()
        self.config.read(file)
        del file

    def error_embed(self, error_message):
        """Returns an error embed for a error message"""
        errorEmbed = discord.Embed(title=f'{self.annonewTitle} - Something went wrong!',
                                   description=f'**Error**\n||{error_message}||',
                                   color=discord.Color.red())
        return errorEmbed

    def wrong_argument_embed(self, ctx: commands.Context, argument: str):
        wrongArgumentEmbed = discord.Embed(title='Falsches Agument',
                                           description=f'`{argument}` ist kein gültiges oder vollständigest Argument für diesen Befehl!',
                                           color=discord.Color.red())
        wrongArgumentEmbed.add_field(name='Bot-Commander',
                                     value='`>commander <add/remove> <user>`')
        return wrongArgumentEmbed

    @commands.command()
    async def commander(self, ctx: commands.Context, *args: str):
        """TODO"""
        # command sequence
        self.log.info(f'[{ctx.author}] called command commander ({ctx.message.content})')
        if GeneralFunctions(self.bot).user_authorization(ctx, self.config['role']['bot_commander']):
            try:
                if args[0] == 'add':
                    if len(args[1]) == 18:
                        newRole = int(args[1])
                        roleList = GeneralFunctions(self.bot).config_str_to_list(self.config['role']['bot_commander'])
                        roleList.append(newRole)
                        newRoleStr = ','.join(str(i) for i in roleList)
                        self.config['role']['bot_commander'] = newRoleStr
                        with open('config.ini', 'w') as configfile:
                            self.config.write(configfile)
                        await ctx.send(f'{ctx.message.author.mention}\n<@{newRole}> wurde zur Liste hinzugefügt!')
                    else:
                        await ctx.send(embed=self.wrong_argument_embed(ctx, args[1]))
                elif args[0] == 'remove':
                    if len(args[1]) == 18:
                        pass
                else:
                    await ctx.send(embed=self.wrong_argument_embed(ctx, args[0]))
            except IndexError as e:
                await ctx.send(embed=self.wrong_argument_embed(ctx, ctx.message.content[11:]))
            except Exception as e:
                await ctx.send(embed=self.error_embed(e))
                self.log.warning(
                    f'[{ctx.author}] error by annosetup command ({e})')
        else:
            print('User is NOT authorized')

def setup(bot: commands.Bot):
    bot.add_cog(Settings(bot))