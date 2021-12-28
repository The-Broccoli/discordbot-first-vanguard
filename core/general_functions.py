from configparser import ConfigParser

import discord
import discord.ext.commands as commands


class GeneralFunctions():

    def __init__(self, bot):
        self.bot = bot

    def load_config(self):
        """Loads the config file"""
        __file = 'config.ini'
        config = ConfigParser()
        config.read(__file)
        del __file
        return config

    def config_str_to_list(self, config_str: str):
        """Converts a string to a list"""
        config_list = config_str.split(',')
        config_list = [int(i) for i in config_list]
        return config_list

    def user_authorization(self, ctx: commands.Context, config_str: int):
        """check if the author is authorized"""
        __serverOwner = self.bot.get_user(int(ctx.guild.owner.id))
        __config_list = self.config_str_to_list(config_str)
        for i in ctx.author.roles or ctx.author.id == __serverOwner.id:
            if i.id in __config_list:
                return True
        return False
