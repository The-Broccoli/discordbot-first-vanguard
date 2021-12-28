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

    def wrong_argument(self, ctx: commands.Context, argument: str, commandTitle: str):
        """Returns an embed for a wrong argument"""
        # ---------- Ankündigung ----------
        if commandTitle == 'Ankündigung':
            embed = discord.Embed(title=f'{commandTitle} - Gegner Name fehlt.',
                                  description='Du hast keinen Gegner angegeben. Bitte gib den '
                                  'Gegner an, wenn du "Angriffskrieg" oder "Verteidigungskrieg" auswählst.',
                                  color=discord.Color.red())
            embed.add_field(name='Beispiele',
                            value='✅ Richtige schreibweiße:\n'
                            '`>annonew Falling-Moon`\n\n'
                            '⛔ Falsche Schreibweise:\n'
                            '`>annonew Falling Moon`')
        # ---------- Einstellungen ----------
        elif commandTitle == 'Einstellungen':
            embed = discord.Embed(title=f'{commandTitle} - Falsches Agument',
                                  description=f'`{argument}` ist kein gültiges oder vollständigest Argument für diesen Befehl!',
                                  color=discord.Color.red())
            embed.add_field(name='Bot-Commander',
                            value='`>commander <add/remove> <role ID>`',
                            inline=True)
            embed.add_field(name='Bot-Commander - List',
                            value='`>commander list`',
                            inline=False)
            embed.add_field(name='Member Ping',
                            value='`>memberping <add/remove> <role ID>`',
                            inline=True)
            embed.add_field(name='Member Ping - List',
                            value='`>memberping list`',
                            inline=False)

        return embed
