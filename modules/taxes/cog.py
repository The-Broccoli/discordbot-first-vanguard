from configparser import ConfigParser
from datetime import datetime, timedelta
from pathlib import Path

import discord
from messages.texes import TexesMessages
from messages.generel import GenerelMessages
from core.logging_handler import UserLoggingHandler
from core.general_functions import GeneralFunctions
from discord.ext import commands
from discord.ui.view import View


class Taxes(commands.Cog, name="Taxes"):
    """TODO Taxes cog"""

    def __init__(self, bot: commands.Bot):
        self.log = UserLoggingHandler('taxes')
        self.t_embed = TexesMessages(bot)
        self.g_embed = GenerelMessages(bot)
        self.bot = bot
        self.taxesTitele = 'Gildensteuer'

        # Load config
        file = 'config.ini'
        self.config = ConfigParser()
        self.config.read(file)
        del file

    class TaxView(View):
        def __init__(self, ctx, config):
            self.ctx = ctx
            self.res = None
            self.config = config
            self.timeout = int(self.config.get(
                'dc_taxes_commands', 'view_timeout_value'))
            super().__init__(timeout=int(self.config.get('dc_taxes_commands', 'view_timeout_value')))

        def disabled_all_button(self):
            for b in self.children:
                b.disabled = True

        # Button "Blacklist"
        @discord.ui.button(label="Blacklist",
                           style=discord.ButtonStyle.primary,
                           custom_id="button_blacklist",
                           emoji='🔒')
        async def button_black_list(self, button, interaction):
            self.disabled_all_button()
            self.res = 'BLACKLIST'
            await interaction.response.edit_message(view=self)
            self.stop()

        # Button "Abbrechen"
        @discord.ui.button(label="Abbrechen",
                           style=discord.ButtonStyle.red,
                           custom_id="button_cancel",
                           emoji='✖')
        async def button_cancel(self, button, interaction):
            self.disabled_all_button()
            self.res = 'CANCEL'
            await interaction.response.edit_message(view=self)
            self.stop()

        async def on_timeout(self):
            self.res = None
            timeoutEmbed = discord.Embed(title='Timeout!',
                                         description=f'Aus versicherungstechnische Gründe haben Sie nur {self.timeout} Sekunden Zeit mit der Nachricht zu interagieren. Führe denn Befehl erneut aus.',
                                         color=discord.Color.red())
            await self.ctx.send(embed=timeoutEmbed)
            self.stop()

        async def on_error(self, error: Exception, item, interaction):  # TODO Not tested!
            self.res = None
            errorEmbed = discord.Embed(title='Something went wrong!',
                                       description=f'**This command is not available here**\n||{error}||',
                                       color=discord.Color.red())
            await interaction.response.send_message(view=errorEmbed)
            self.stop()

    def load_blacklist(self):
        # check if the file exists (otherwise create it)
        __file = Path('blacklist.txt')
        __file.touch(exist_ok=True)
        # load the file
        __file = open('blacklist.txt', 'r')
        blackList = __file.read().splitlines()
        __file.close()
        del __file
        return blackList

    def blacklist_time_icon(self, today: datetime, userTime: datetime):
        if userTime < today - timedelta(days=14):  # over 2 weeks
            return '🔴'
        elif userTime < today - timedelta(days=7):  # over 1 week
            return '🟠'
        elif userTime < today - timedelta(days=3):  # over 3 days
            return '🟡'
        elif userTime < today - timedelta(hours=24):  # over 24 hours
            return '🟢'
        else:
            return '⚪'  # error

    def blacklist_embed(self, blacklist):
        __today = datetime.now()
        __todayStr = __today.strftime('%H:%M - %d.%m.%y')
        __blacklistString = ''
        # String formed for embed
        for __user in blacklist:
            try:
                __user = __user.split(';')
                __icon = self.blacklist_time_icon(
                    __today, datetime.strptime(__user[1], '%d/%m/%y-%H:%M:%S'))
                __user[1] = __user[1][:-9].replace('/', '.')
                __blacklistString += f'{__icon} - <@!{__user[0]}> - {__user[1]}\n'
            except:
                __blacklistString += f'⚪ - Error {__user}\n'
        # create and fill embed for user
        blacklistEmbed = discord.Embed(title='Gildensteuer Benachrichtigung - Blacklist',
                                       description=f'In der folgenden Liste sind alle Mitglieder aufgeführt, die angegeben haben die "Gildensteuer Benachrichtigung" nicht mehr zu erhalten.\nStand: {__todayStr}',
                                       color=discord.Color.green())
        blacklistEmbed.add_field(name=f'Blacklist', value=__blacklistString)
        blacklistEmbed.add_field(
            name='Legende', value='Wie lange der Eintrag besteht:\n🔴 - 2 Wochen\n🟠 - 1 Wochen\n🟡 - 3 Tage\n🟢 - 24 Stunden\n ⚪ - Error')
        del __today, __todayStr, __blacklistString, __icon, __user
        return blacklistEmbed

    @commands.command()
    async def taxes(self, ctx: commands.Context):
        """TODO Taxes command"""
        # blacklist information determine
        blacklist = self.load_blacklist()

        # determine database information
        intervalValue = int(self.config.get(
            'dc_taxes_commands', 'interval_value'))
        unpaidTaxes = 45  # TODO DEMO VALUE
        paidTaxes = 23  # TODO DEMO VALUE

        # presenceTime list = 1. Presence Time in Minutes 2. Presence Time as Date
        presenceTime = [datetime.today() + (timedelta(hours=0, minutes=(unpaidTaxes * intervalValue)) - timedelta(hours=0, minutes=(len(blacklist) * intervalValue))),
                        (unpaidTaxes * intervalValue) - (len(blacklist) * intervalValue)]
        presenceTime[0] = presenceTime[0].strftime(
            '%H:%M - (%m/%d/%Y)')  # datetime to string

        # command sequence
        self.log.info(f'[{ctx.author}] called command taxes')
        if GeneralFunctions(self.bot).user_authorization(ctx, self.config['role']['bot_commander']):
            """With this command you can start the tax notification"""
            infoEmbed = self.t_embed.info(
                ctx, intervalValue, unpaidTaxes, paidTaxes, blacklist, presenceTime, self.taxesTitele)
            view = self.TaxView(ctx, self.config)  # create view
            # send embed and view and save message class in msg
            msg = await ctx.send(embed=infoEmbed, view=view)
            await view.wait()  # waiting for button click
            if view.res == None:
                await msg.delete()
                return
            elif view.res == 'CANCEL':
                await msg.delete()
                await ctx.message.delete()  # delete the message of the orderer
                return
            elif view.res == 'BLACKLIST':
                await msg.edit(embed=self.blacklist_embed(blacklist))
                return
            elif view.res == 'SEND':
                return
        else:
            await ctx.send(embed=self.g_embed.error(self.taxesTitele, 'Du hast keine Berechtigung für diesen Befehl!'))

    @commands.command()
    async def blacklist(self, ctx: commands.Context):
        # command sequence
        self.log.info(f'[{ctx.author}] called command blacklist')
        if GeneralFunctions(self.bot).user_authorization(ctx, self.config['role']['bot_commander']):
            __blacklist = self.load_blacklist()
            await ctx.send(embed=self.blacklist_embed(__blacklist))
        else:
            await ctx.send(embed=self.g_embed.error(self.taxesTitele, 'Du hast keine Berechtigung für diesen Befehl!'))


def setup(bot: commands.Bot):
    bot.add_cog(Taxes(bot))
