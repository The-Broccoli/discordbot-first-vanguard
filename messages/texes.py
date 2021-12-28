from datetime import datetime, timedelta

import discord
from discord.ext import commands


class TexesMessages():
    """This class creates different messages for the user"""

    def __init__(self, bot):
        self.bot = bot

    def info(self, ctx: commands.Context, intervalValue: int, unpaidTaxes, paidTaxes, blacklist, presenceTime, taxesTitele):
        embed = discord.Embed(title=f'{taxesTitele} - Benachrichtigung',
                                  description=f'Hallo {ctx.message.author.mention}, mit diesem Befehl kannst du eine Private Notification **an alle Mitglieder** automatisiert versenden, die noch keine Steuern in dieser KW gezahlt haben (aufgenommen Mitglieder, die diesen Dienst verweigert haben).',
                                  color=discord.Colour.green())
        embed.add_field(name="Ablauf",
                            value=f'Sobald du auf "Absenden" klickst, werde die Nachrichten in einem Intervall von {intervalValue} Minuten versendet. Zwischen dem Versenden der Nachrichten ist so genügen Zeit, um die Beiträge einzutragen.\n`({unpaidTaxes} (Unbezahlt) - {len(blacklist)} (Blacklist)) * {intervalValue} Minuten = {presenceTime[1]}`\n Anwesenheit gewähren bis **{presenceTime[0]}**',
                            inline=True)
        embed.add_field(name='Tax status',
                            value=f'Offen: **{unpaidTaxes}**\tBezahlt: **{paidTaxes}**',
                            inline=True)
        return embed