from configparser import ConfigParser
from datetime import datetime, timedelta

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

        intervalValue = int(self.config.get('dc_taxes_commands', 'interval_value'))
        unpaidTaxes = 45 # TODO DEMO VALUE
        paidTaxes = 23 # TODO DEMO VALUE
        blacklisted = 5 # TODO DEMO VALUE
        presenceTime = [datetime.today() + (timedelta(hours=0, minutes=(unpaidTaxes * intervalValue)) - timedelta(hours=0, minutes=(blacklisted * intervalValue))),
                        (unpaidTaxes * intervalValue) - (blacklisted * intervalValue)]
        presenceTime[0] = presenceTime[0].strftime('%H:%M - (%m/%d/%Y)')

        try:
            for i in ctx.author.roles:
                if i.id == int(self.config['role']['bot_commander']):
                    """With this command you can start the tax notification"""
                    embedVar01 = discord.Embed(title='Gildensteuer Benachrichtigung',
                                            description=f'Hallo {ctx.message.author.mention}, mit diesem Befehl kannst du eine Private Notification **an alle Mitglieder** automatisiert versenden, die noch keine Steuern in dieser KW gezahlt haben (aufgenommen Mitglieder, die diesen Dienst verweigert haben).',
                                            color=discord.Colour.green())
                    embedVar01.add_field(name="Ablauf",
                                        value=f'Sobald du auf "Absenden" klickst, werde die Nachrichten in einem Intervall von {intervalValue} Minuten versendet. Zwischen dem Versenden der Nachrichten ist so genügen Zeit, um die Beiträge einzutragen.\n`({unpaidTaxes} (Unbezahlt) - 5 (Blacklist)) * {intervalValue} Minuten = {presenceTime[1]}`\n Anwesenheit gewähren bis **{presenceTime[0]}**',
                                        inline=True)
                    embedVar01.add_field(name='Tax status',
                                        value=f'Offen: **{unpaidTaxes}**\tBezahlt: **{paidTaxes}**',
                                        inline=True)
                    await ctx.send(embed=embedVar01)
            # await ctx.message.delete() # Delete message, does this make sense ?
        except Exception as e:
            errorEmbed = discord.Embed(title='Something went wrong!',
                                        description=f'**This command is not available here**\n||{e}||',
                                        color=discord.Color.red())
            await ctx.send(embed=errorEmbed)

def setup(bot: commands.Bot):
    bot.add_cog(Taxes(bot))
