from configparser import ConfigParser

import discord
from messages.generel import GenerelMessages
from core.logging_handler import UserLoggingHandler
from core.general_functions import GeneralFunctions
from discord.ext import commands


class Settings(commands.Cog, name="Settings"):
    """TODO"""

    def __init__(self, bot: commands.Bot):
        self.log = UserLoggingHandler('settings')
        self.g_embed = GenerelMessages(bot)
        self.bot = bot
        self.settingTitle = 'Einstellungen'

        # Load config
        file = 'config.ini'
        self.config = ConfigParser()
        self.config.read(file)
        del file

    @commands.command()
    async def commander(self, ctx: commands.Context, *args: str):
        """TODO"""
        # command sequence
        self.log.info(
            f'[{ctx.author}] called command commander ({ctx.message.content})')
        if GeneralFunctions(self.bot).user_authorization(ctx, self.config['role']['bot_commander']):
            try:
                if args[0] == 'add':
                    if len(args[1]) == 18:
                        __newRole = int(args[1])
                        __roleList = GeneralFunctions(self.bot).config_str_to_list(
                            self.config['role']['bot_commander'])
                        __roleList.append(__newRole)
                        __newRoleStr = ','.join(str(i) for i in __roleList)
                        self.config['role']['bot_commander'] = __newRoleStr
                        with open('config.ini', 'w') as configfile:
                            self.config.write(configfile)
                        await ctx.send(f'{ctx.message.author.mention}\n<@{__newRole}> wurde zur Liste hinzugefügt!')
                        return
                    else:
                        await ctx.send(embed=self.g_embed.wrong_argument(ctx, args[1], self.settingTitle))
                        return
                elif args[0] == 'remove':
                    if len(args[1]) == 18:
                        __removeRole = int(args[1])
                        __roleList = GeneralFunctions(self.bot).config_str_to_list(
                            self.config['role']['bot_commander'])
                        __roleList.remove(__removeRole)
                        __newRoleStr = ','.join(str(i) for i in __roleList)
                        self.config['role']['bot_commander'] = __newRoleStr
                        with open('config.ini', 'w') as configfile:
                            self.config.write(configfile)
                        await ctx.send(f'{ctx.message.author.mention}\n<@{__removeRole}> wurde aus der Liste entfernt!')
                        return
                    else:
                        await ctx.send(embed=self.g_embed.wrong_argument(ctx, args[1], self.settingTitle))
                        return
                elif args[0] == 'list':
                    __roleList = GeneralFunctions(self.bot).config_str_to_list(
                        self.config['role']['bot_commander'])
                    __roleListStr = ''
                    for __role in __roleList:
                        __roleListStr += f'<@&{__role}> - ID:||{__role}||\n'
                    await ctx.send(f'{ctx.message.author.mention}\n{__roleListStr}')
                    return
                else:
                    await ctx.send(embed=self.g_embed.wrong_argument(ctx, args[0], self.settingTitle))
            except IndexError as e:
                await ctx.send(embed=self.g_embed.wrong_argument(ctx, ctx.message.content[11:], self.settingTitle))
            except Exception as e:
                await ctx.send(embed=self.g_embed.error(self.settingTitle, e))
                self.log.warning(
                    f'[{ctx.author}] error by annosetup command ({e})')
        else:
            pass


def setup(bot: commands.Bot):
    bot.add_cog(Settings(bot))
