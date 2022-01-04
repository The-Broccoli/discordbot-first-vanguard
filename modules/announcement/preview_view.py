import discord
from core.logging_handler import UserLoggingHandler
from discord.ext import commands
from discord.ui.view import View


class PreviewView(View):
    """Creates a VIEW sup class with dropdown menu and buttons.
    Interactions return certain values"""

    def __init__(self, ctx: commands.Context, config):
        self.log = UserLoggingHandler('announcement_preview_view')
        self.ctx = ctx
        self.buttonRes = None
        self.config = config
        self.timeout = int(self.config.get(
            'dc_announcement_commands', 'view_timeout_value'))
        super().__init__(timeout=self.timeout)

    async def on_timeout(self):
        timeoutEmbed = discord.Embed(title='Timeout!',
                                        description=f'Aus versicherungstechnischen Gründen haben Sie nur {self.timeout} Sekunden Zeit mit der Nachricht zu interagieren. Führe den Befehl erneut aus.',
                                        color=discord.Color.red())
        await self.ctx.send(embed=timeoutEmbed)
        self.stop()

    async def on_error(self, error: Exception, item, interaction):  # TODO Not tested!
        errorEmbed = discord.Embed(title='Something went wrong!',
                                    description=f'**This command is not available here**\n||{error}||',
                                    color=discord.Color.red())
        await interaction.response.send_message(view=errorEmbed)
        self.log.warning(
            f'[{self.ctx.author}] Error by annonew command ({error})')
        self.stop()

    @discord.ui.button(label="Absenden",
                        style=discord.ButtonStyle.green,
                        custom_id="send_button",
                        emoji='💌')
    async def button_send(self, button, interaction):
        self.buttonRes = 'SEND'
        await interaction.response.edit_message(view=self)
        self.stop()

    @discord.ui.button(label="Abbrechen",
                        style=discord.ButtonStyle.red,
                        custom_id="cancel_button",
                        emoji='✖')
    async def button_cancel(self, button, interaction):
        self.buttonRes = 'CANCEL'
        await interaction.response.edit_message(view=self)
        self.stop()
