from datetime import datetime, timedelta

import discord
from discord.ext import commands


class AnnouncementMessages():
    """This class creates different messages for the user"""

    def __init__(self, bot):
        self.bot = bot
        self.botVersion = '0.1'  # TODO
        self.logoPath = ''  # TODO

    def add_footer(self, ctx: commands.Context, embed: discord.Embed):
        """Adds the footer to the embed"""
        embed.set_footer(
            text=f'{ctx.author.display_name} – built with: First Vanguard Discord Bot {self.botVersion}', icon_url=ctx.author.avatar.url)
        return embed

    def add_war_remember(self, embed: discord.Embed):
        embed.add_field(name='🛠  Denkt bitte an',
                        value=' - [Warbuilds](https://first-vanguard.de/roles)\n'
                        ' - Buff Food\n'
                        ' - Honing Stone\n')
        return embed

    def event(self, ctx: commands.Context, type, area, day, time, additional, enemy, friend):
        """Returns an embed for the war announcement message"""
        __meetingTime = datetime.strptime(time, '%H:%M')
        # ----------------------------------------------------------
        if type == 'Angriffskrieg':
            __meetingTime = __meetingTime - timedelta(minutes=45)
            __meetingTime = __meetingTime.strftime('%H:%M')
            embed = discord.Embed(title='⚔  Das Kriegshorn ruft - Dein Gouverneur benötigt dich!',
                                  description=f'Am **{day}** um **{time}** führen wir einen Krieg um **{area}**\n '
                                  f'gegen **{enemy}**. Meldet euch bitte __rechtzeitig__ in {area}, '
                                  'am War Board (Kriegsbrett), für den Krieg an.',
                                  color=discord.Color.purple())
            if additional:
                embed.add_field(name='ℹ Zusaetzliche Informationen',
                                value=additional, inline=False)
            embed.add_field(
                name='\U0001F4CC Zusammenfassung',
                value=f' - Wo: `{area}`\n'
                f' - Wann (Ingame): `{day}` um `{time}`\n'
                f' - Wann (Discord): `{day}` um `{__meetingTime}`\n'
                f' - Gegen: `{enemy}`')
            embed = self.add_war_remember(embed)
        # ----------------------------------------------------------
        elif type == 'Verteidigungskrieg':
            __meetingTime = __meetingTime - timedelta(minutes=45)
            __meetingTime = __meetingTime.strftime('%H:%M')
            embed = discord.Embed(title='🛡  Das Kriegshorn ruft - Wir werden angegriffen!',
                                  description=f'Am **{day}** um **{time}** müssen wir unser geliebtes **{area}**\n '
                                  f'gegen **{enemy}** verteidigen. Meldet euch bitte __rechtzeitig__ in {area}, am '
                                  'War Board (Kriegsbrett), für den Krieg an.',
                                  color=discord.Color.purple())
            if additional:
                embed.add_field(name='Zusaetzliche Informationen',
                                value=additional, inline=False)
            embed.add_field(
                name='ℹ  Zusammenfassung',
                value=f' - Wo: `{area}`\n'
                f' - Wann (Ingame): `{day}` um `{time}`\n'
                f' - Wann (Discord): `{day}` um `{__meetingTime}`')
            embed = self.add_war_remember(embed)
        # ----------------------------------------------------------

        elif type == 'PVP-Push':
            __meetingTime = __meetingTime - timedelta(minutes=15)
            __meetingTime = __meetingTime.strftime('%H:%M')
            if friend:
                embed = discord.Embed(title='✊  Das Syndikat ruft - Wir pushen ein Gebiet!',
                                      description=f'Am **{day}** um **{time}** werden wir gnadenlos den Einfluss mit '
                                      f'der Kompanie **{friend}** in **{area}** pushen. Umso mehr helfen, desto schneller sind wir fertig.',
                                      color=discord.Color.purple())

            else:
                embed = discord.Embed(title='✊  Das Syndikat ruft - Wir pushen ein Gebiet!',
                                      description=f'Am **{day}** um **{time}** werden wir gnadenlos den Einfluss '
                                      f'in **{area}** pushen. Umso mehr helfen, desto schneller sind wir fertig.',
                                      color=discord.Color.purple())
            if additional:
                embed.add_field(name='Zusaetzliche Informationen',
                                value=additional, inline=False)
            embed.add_field(name='ℹ  Zusammenfassung',
                            value=f' - Wo: `{area}`\n'
                            f' - Wann (Ingame): `{day}` um `{time}`\n'
                            f' - Wann (Discord): `{day}` um `{__meetingTime}`\n'
                            f' - Zusammen mit: `{enemy}`')
        # ----------------------------------------------------------
        elif type == 'Invasion':
            __meetingTime = __meetingTime - timedelta(minutes=30)
            __meetingTime = __meetingTime.strftime('%H:%M')
            embed = discord.Embed(title='👺  Das Kriegshorn ruft - Die Verderbten greifen an!',
                                  description=f'Am **{day}** um **{time}** greifen die Verderbten '
                                  f'unser geliebtes **{area}** an. Meldet euch bitte __rechtzeitig__ in '
                                  f'**{area}**, am War Board (Kriegsbrett), für die Invasion an.',
                                  color=discord.Color.purple())
            if additional:
                embed.add_field(name='Zusaetzliche Informationen',
                                value=additional, inline=False)
            embed.add_field(name='ℹ  Zusammenfassung',
                            value=f' - Wo: `{area}`\n'
                            f' - Wann (Ingame): `{day}` um `{time}`\n'
                            f' - Wann (Discord): `{day}` um `{__meetingTime}`\n')
            embed.add_field(name='🛠  Denkt bitte an',
                            value=' - Trophy(s)\n'
                            ' - Corrupted Coatings\n'
                            ' - Honing Stones\n'
                            ' - T5 Saphire in Waffen\n'
                            ' - Corrupted Damage Perk auf Waffen\n')
        embed = self.add_footer(ctx, embed)
        return embed

    def delivered(self, ctx: commands.Context, channel: discord.TextChannel, commandTitle):
        """returns an embed for the delivered announcement message"""
        embed = discord.Embed(title=f'{commandTitle} - Ankündigung wurde veröffentlicht!',
                              description=f'{ctx.author.mention} deine Ankündigung '
                              f'wurde im Channel <#{channel.id}> gepostet!',
                              color=discord.Color.purple())
        return embed
