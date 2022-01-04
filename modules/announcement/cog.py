import time as pytime
from datetime import datetime

import discord
from core.general_functions import GeneralFunctions
from core.logging_handler import UserLoggingHandler
from discord.commands import Option, slash_command
from discord.ext import commands
from messages.announcement import AnnouncementMessages
from messages.generel import GenerelMessages
from modules.announcement.preview_view import PreviewView


class Announcement(commands.Cog, name='Announcement'):
    def __init__(self, bot):
        self.bot = bot
        self.log = UserLoggingHandler('slash_command_announcement')
        self.a_embed = AnnouncementMessages(bot)  # Announcement embeds
        self.g_embed = GenerelMessages(bot)  # General embeds
        self.commandTitel = "Ankündigung"  # Command Titel for the embed

    @slash_command(name='annonew', description='Erstelle eine Ankündigung', guild_ids=[480418209099546665])
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
                                              'Ebonscale Reach (Lichtholz)',
                                              'Weaver\'s Fen (Webermoor)',
                                              'Restless Shore (Unstete Küste)',
                                              'Mourningdale (Klagental)'],
                                     required=True,
                                     default=''),
                      date: Option(str,
                                   'Wann ist das Event? (DD.MM)',
                                   required=True,
                                   default=''),
                      time: Option(str,
                                   'Um welche Uhrzeit findet es statt? (HH:MM)',
                                   required=True,
                                   default=''),
                      enemy: Option(str,
                                    'Welcher Gegner greift an?',
                                    required=False,
                                    default=''),
                      friend: Option(str,
                                     'Mit welchem Verbündeten greift wir an?',
                                     required=False,
                                     default='')):
        # logging - who uses the commands and with which augments
        self.log.info(
            f'{ctx.author} called command annonew (channel: {channel}, type: {type}, region: {region}, date: {date}, time: {time}, enemy: {enemy}, friend: {friend})')
        # load config
        self.config = GeneralFunctions(self.bot).load_config()
        if GeneralFunctions(self.bot).user_authorization(ctx, self.config['role']['bot_commander']):
            __flag = []
            # Check if "data" has the correct spelling
            try:
                __eventDayTest = datetime.strptime(date, '%d.%m')
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
                __msg = await ctx.respond(ephemeral=True, embed=self.g_embed.error(self.commandTitel, f'{__flag} ist nicht korrekt angegeben.'))
            else:
                annoEmbed = self.a_embed.war(ctx, type, region, date, time, 'test', 'test')
                __msg = await ctx.respond(embed=annoEmbed)

            # TODO am ende die msg löschen ... aber wie ? ('Interaction' object has no attribute 'delete')
            # await __msg.delete(reason='Command annosetup')
        else:
            # Ist nicht authorisiert
            pass


def setup(bot):
    bot.add_cog(Announcement(bot))
