import time as pytime
from datetime import datetime

import discord
from core.general_functions import GeneralFunctions
from core.logging_handler import UserLoggingHandler
from discord.commands import Option, slash_command
from discord.ext import commands
from messages.announcement import AnnouncementMessages
from messages.generel import GenerelMessages


class Announcement(commands.Cog, name='Announcement'):
    def __init__(self, bot):
        self.bot = bot
        self.log = UserLoggingHandler('slash_command_announcement')
        self.a_embed = AnnouncementMessages(bot)  # Announcement embeds
        self.g_embed = GenerelMessages(bot)  # General embeds
        self.commandTitel = "Ankündigung"  # Command Titel for the embed

    @slash_command(name='announcement', description='Erstelle eine Ankündigung', guild_ids=[881238086644817920])
    async def annonew(self,
                      ctx: commands.Context,
                      channel: discord.TextChannel,
                      type: Option(str,
                                   'Um welches Event handelt es sich? (war_attack, war_defend, invasion, pvp_push)',
                                   choices=['Angriffskrieg', 'Verteidigungskrieg',
                                            'Invasion', 'PVP-Push'],
                                   required=True,
                                   default=''),
                      region: Option(str,
                                     'Um welcher Gebiet handelt es sich?',
                                     choices=['First Light (Erstes Licht)',
                                              'Monarch\'s Bluffs (Königsfels)',
                                              'Everfall (Immerfall)',
                                              'Windsward (Windkreis)',
                                              'Cutless Keys (Entermesserriff)',
                                              'Reekwater (Brackwasser)',
                                              'Ebonscale Reach (Ebenmaß)',
                                              'Weaver\'s Fen (Webermoor)',
                                              'Restless Shore (Unstete Küste)',
                                              'Mourningdale (Klagental)',
                                              'Brightwood (Lichtholz)'],
                                     required=True,
                                     default=''),
                      date: Option(str,
                                   'Wann ist das Event? (DD.MM.YYYY)',
                                   required=True,
                                   default=''),
                      time: Option(str,
                                   'Um welche Uhrzeit findet es statt? (HH:MM)',
                                   required=True,
                                   default=''),
                      additional: Option(str,
                                         'Zusatzinformationen zum Event?',
                                         required=False,
                                         default=''),
                      enemy: Option(str,
                                    'Welcher Gegner greift an?',
                                    required=False,
                                    default=''),
                      friend: Option(str,
                                     'Mit welchem Verbündeten greift wir an? (Zusatzinformation "friend" wird nur in PVP-Push angezeigt)',
                                     required=False,
                                     default='')):
        # logging - who uses the commands and with which augments
        self.log.info(
            f'{ctx.author} called command /annonew (channel: {channel}, type: {type}, region: {region}, date: {date}, time: {time}, additional: {additional}, enemy: {enemy}, friend: {friend})')
        # load config
        self.config = GeneralFunctions(self.bot).load_config()
        if GeneralFunctions(self.bot).user_authorization(ctx, self.config['role']['bot_commander']):
            __flag = []
            # Check if "data" has the correct spelling
            try:
                __eventDayTest = datetime.strptime(date, '%d.%m.%Y')
            except ValueError:
                __flag.append('"date"')
            # Check if "time" has the correct spelling
            try:
                __eventTimeTest = datetime.strptime(time, '%H:%M')
            except ValueError:
                __flag.append('"time"')
            # Check if flag is not empty
            if __flag:
                __flag = ' '.join(__flag)
                await ctx.respond(ephemeral=True, embed=self.g_embed.error(self.commandTitel, f'{__flag} ist nicht korrekt angegeben.'))
                return
            else:
                # Special arrangement
                if type == 'Angriffskrieg' or type == 'Verteidigungskrieg':
                    if not enemy:
                        await ctx.respond(ephemeral=True, embed=self.g_embed.error(self.commandTitel, '"enemy" ist nicht angegeben.'))
                        return
                annoEmbed = self.a_embed.event(
                    ctx, type, region, date, time, additional, enemy, friend)
                __memberRollId = self.config.get('role', 'member')
                __memberRollId = GeneralFunctions(
                    self.bot).config_str_to_list(__memberRollId)
                __rollstr = ''
                for m in __memberRollId:
                    __rollstr += f'<@&{str(m)}> '
                await channel.send(f'{__rollstr}', embed=annoEmbed)
                await ctx.respond(embed=self.a_embed.delivered(ctx, channel, self.commandTitel))
                return
        else:
            # Ist nicht authorisiert
            self.log.info(
                f'{ctx.author} command /annonew terminated - is not authorized')
            await ctx.respond(ephemeral=True, embed=self.g_embed.error(self.commandTitel, f'Du bist nicht authorisiert, diesen Befehl zu nutzen.'))


def setup(bot):
    bot.add_cog(Announcement(bot))
