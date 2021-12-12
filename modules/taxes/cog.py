from configparser import ConfigParser
from datetime import datetime, timedelta

import discord
from discord.ext import commands
from discord.ui.view import View


class Taxes(commands.Cog, name="Taxes"):
    """TODO Taxes cog"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

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
            self.timeout = int(self.config.get('dc_taxes_commands', 'view_timeout_value'))
            super().__init__(timeout=int(self.config.get('dc_taxes_commands', 'view_timeout_value')))

        def disabled_all_button(self):
            for b in self.children:
                b.disabled = True

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
        
        async def on_error(self, error: Exception, item, interaction): # TODO Not tested!
            self.res = None
            errorEmbed = discord.Embed(title='Something went wrong!',
                                        description=f'**This command is not available here**\n||{error}||',
                                        color=discord.Color.red())
            await interaction.response.send_message(view=errorEmbed)
            self.stop()

    @commands.command()
    async def taxes(self, ctx: commands.Context):
        """TODO Taxes command"""
        intervalValue = int(self.config.get('dc_taxes_commands', 'interval_value'))
        unpaidTaxes = 45 # TODO DEMO VALUE
        paidTaxes = 23 # TODO DEMO VALUE
        blacklisted = 5 # TODO DEMO VALUE
        presenceTime = [datetime.today() + (timedelta(hours=0, minutes=(unpaidTaxes * intervalValue)) - timedelta(hours=0, minutes=(blacklisted * intervalValue))),
                        (unpaidTaxes * intervalValue) - (blacklisted * intervalValue)]
        presenceTime[0] = presenceTime[0].strftime('%H:%M - (%m/%d/%Y)') # datetime zu string
        try:
            for i in ctx.author.roles: # # passing through the roles of the author
                if i.id == int(self.config['role']['bot_commander']): # is there the role id that matches bot_commander id ?
                    """With this command you can start the tax notification"""
                    infoEmbed = discord.Embed(title='Gildensteuer Benachrichtigung',
                                            description=f'Hallo {ctx.message.author.mention}, mit diesem Befehl kannst du eine Private Notification **an alle Mitglieder** automatisiert versenden, die noch keine Steuern in dieser KW gezahlt haben (aufgenommen Mitglieder, die diesen Dienst verweigert haben).',
                                            color=discord.Colour.green())
                    infoEmbed.add_field(name="Ablauf",
                                        value=f'Sobald du auf "Absenden" klickst, werde die Nachrichten in einem Intervall von {intervalValue} Minuten versendet. Zwischen dem Versenden der Nachrichten ist so genügen Zeit, um die Beiträge einzutragen.\n`({unpaidTaxes} (Unbezahlt) - 5 (Blacklist)) * {intervalValue} Minuten = {presenceTime[1]}`\n Anwesenheit gewähren bis **{presenceTime[0]}**',
                                        inline=True)
                    infoEmbed.add_field(name='Tax status',
                                        value=f'Offen: **{unpaidTaxes}**\tBezahlt: **{paidTaxes}**',
                                        inline=True)
                    view = self.TaxView(ctx, self.config) # create view
                    msg = await ctx.send(embed=infoEmbed ,view=view) # send embed and view and save message class in msg
                    await view.wait() # waiting for button click
                    if view.res == None or 'CANCEL': # if timeout or error
                        await msg.delete() # delete message with infoEmbed
                        if view.res == 'CANCEL':
                            await ctx.message.delete() # delete the message of the orderer
                    elif view.res == 'SEND':
                        pass
                    elif view.res == 'BLACKLIST':
                        pass
            # await ctx.message.delete() # Delete message, does this make sense ?
        except Exception as e:
            errorEmbed = discord.Embed(title='Something went wrong!',
                                        description=f'**This command is not available here**\n||{e}||',
                                        color=discord.Color.red())
            await ctx.send(embed=errorEmbed)

def setup(bot: commands.Bot):
    bot.add_cog(Taxes(bot))
