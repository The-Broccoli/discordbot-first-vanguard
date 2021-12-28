from datetime import datetime, timedelta

import discord
from discord.ext import commands


class AnnouncementMessages():
    """This class creates different messages for the user"""

    def __init__(self, bot):
        self.bot = bot
        self.botVersion = '0.1'  # TODO
        self.logoPath = ''  # TODO

    def add_footer(self, embed: discord.Embed):
        """Adds the footer to the embed"""
        embed.set_footer(
            text=f'The Forgotten Team - Forgotten-Hydra Discord Bot {self.botVersion}', icon_url=self.logoPath)
        return embed

    # Announcement messages

    def info_text(self, commandTitle):
        """Returns an embed with the info text for the announcement command"""
        embed = discord.Embed(title=f'{commandTitle} - Formular',
                              description='Wähle hintereinander bitte folgende Informationen aus\n\n'
                              '- Art des Events: `Angriffskrieg, Verteidigungskrieg, Invasion`\n'
                              '- In welchem Gebiet: `Everfall, Windsward, Mourningdale, ...`\n'
                              '- An welchen Tag: `Tue, Wed, Thu, Fri ...`\n'
                              '- Um wie viel Uhr: `17:30, 18:00, 18:30, 19:00, ...`',
                              color=discord.Color.purple())

        return embed

    def war(self, type, area, day, time, enemy):
        """Returns an embed for the war announcement message"""
        __meetingTime = datetime.strptime(time, '%H:%M')
        __meetingTime = __meetingTime - timedelta(minutes=30)
        __meetingTime = __meetingTime.strftime('%H:%M')
        if type == 'war_agression':
            embed = discord.Embed(title=f'⚔  Das Kriegshorn ruft - Dein Gouverneur benötigt dich!',
                                  description=f'Um **{time}** am **{day}** führen wir einen Krieg um **{area}**\n '
                                  f'gegen **{enemy}**. Meldet euch bitte __rechtzeitig__ in {area}, '
                                  'am War Board (Kriegs Brett) für den Krieg an.',
                                  color=discord.Color.purple())
            embed.add_field(
                name='ℹ  Zusammenfassung',
                value=f' - Wo: `{area}`\n'
                f' - Wann (Ingame): `{day}` um `{time}`\n'
                f' - Wann (Discord): `{__meetingTime}`\n'
                f' - Gegen: `{enemy}`')
            embed.add_field(
                name='🛠  Denkt bitte an',
                value=' - [buff food](https://www.google.com/)\n'
                ' - [war builds](https://www.google.com/)')
        elif type == 'war_defense':
            embed = discord.Embed(title=f'🛡  Das Kriegshorn ruft - Wir werden angegriffen!',
                                  description=f'Am **{day}** um **{time}** müssen wir unser geliebtes **{area}**\n '
                                  f'gegen **{enemy}** verteidigen. Meldet euch bitte __rechtzeitig__ in {area}, am '
                                  'War Board (Kriegs Brett) für den Krieg an.',
                                  color=discord.Color.purple())
            embed.add_field(
                name='ℹ  Zusammenfassung',
                value=f' - Wo: `{area}`\n'
                f' - Wann (Ingame): `{day}` um `{time}`\n'
                f' - Wann (Discord): `{__meetingTime}`')
            embed.add_field(
                name='🛠  Denkt bitte an',
                value=' - [buff food](https://www.google.com/)\n'
                ' - [corrupted perks](https://www.google.com/)')
        embed = self.add_footer(embed)
        return embed

    def inv(self, area, day, time):
        """Returns an embed for the invasion announcement message"""
        __meetingTime = datetime.strptime(time, '%H:%M')
        __meetingTime = __meetingTime - timedelta(minutes=15)
        __meetingTime = __meetingTime.strftime('%H:%M')
        embed = discord.Embed(title=f'👺  Das Kriegshorn ruft - Complete Invasions!',
                              description=f'Am **{day}** um **{time}** fällt die Korruption in '
                              'unser geliebtes **{area}** ein. Meldet euch bitte rechtzeitig in '
                              f'**{area}**, am War Board (Kriegs Brett) für den Invasions an.',
                              color=discord.Color.purple())
        embed.add_field(name='ℹ  Zusammenfassung',
                        value=f' - Wo: `{area}`'
                        f'\n - Wann (Ingame): `{day}` um `{time}`'
                        f'\n - Wann (Discord): `{__meetingTime}`')
        embed.add_field(name='🛠  Denkt bitte an',
                        value='- [buff food](https://www.google.com/)'
                        '\n- [corrupted perks](https://www.google.com/)')
        embed = self.add_footer(embed)
        return embed

    def delivered(self, ctx: commands.Context, channelId, commandTitle):
        """returns an embed for the delivered announcement message"""
        embed = discord.Embed(title=f'{commandTitle} - Ankündigung wurde veröffentlicht!',
                              description=f'{ctx.message.author.mention} deine Ankündigung '
                              f'wurde im Channel <#{channelId}> gepostet!',
                              color=discord.Color.purple())
        return embed

    def config_saved(self, ctx: commands.Context, channelId: str, commandTitle):
        """returns an embed for the config saved announcement message"""
        embed = discord.Embed(title=f'{commandTitle} - Konfiguration gespeichert!',
                              description=f'{ctx.message.author.mention} Die Konfiguration wurde gespeichert!\n'
                              f'Ankündigung werden jetzt in <#{channelId}> gepostet',
                              color=discord.Color.purple())
        return embed
