from configparser import ConfigParser
from datetime import datetime, timedelta

import discord
from discord.ext import commands
from discord.member import M
from discord.ui.view import View


class Announcement(commands.Cog, name="Announcement"):
    """TODO"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.annonewTitle = 'Neue Ankündigung'

        # Load config
        file = 'config.ini'
        self.config = ConfigParser()
        self.config.read(file)
        del file

        self.logoPath = self.config.get('bot_info', 'logo_path')
        self.botVersion = str(self.config.get('bot_info', 'version'))
    
    def error_embed(self, error_message):
        """Returns an error embed"""
        errorEmbed = discord.Embed(title=f'{self.annonewTitle} - Something went wrong!',
                                    description=f'**This command is not available here**\n||{error_message}||',
                                    color=discord.Color.red())
        return errorEmbed
    
    def anno_new_embed(self):
        """TODO"""
        annoEmbed = discord.Embed(title=f'{self.annonewTitle} - Formular',
                                    description='Wähle hintereinander bitte folgende Informationen aus\n\n- Art des Events: `Angriffskrieg, Verteidigungskrieg, Invasion`\n- In welchem Gebiet: `Everfall, Windsward, Mourningdale, ...`\n- An welchen Tag: `Tue, Wed, Thu, Fri ...`\n- Um wie viel Uhr: `17:30, 18:00, 18:30, 19:00, ...`',
                                    color=discord.Color.green())
        return annoEmbed
    
    def anno_embed_war(self, type, area, day, time, enemy):
        """TODO"""
        __meetingTime = datetime.strptime(time, '%H:%M')
        __meetingTime = __meetingTime - timedelta(minutes=15)
        __meetingTime = __meetingTime.strftime('%H:%M')
        if type == 'war_agression':
            annoEmbed = discord.Embed(title=f'⚔  Das Kriegshorn ruft - Dein Gouverneur benötigt dich!',
                                        description=f'Um **{time}** am **{day}** führen wir einen Krieg um **{area}**\n gegen **{enemy}**. Meldet euch bitte __rechtzeitig__ in {area}, am War Board (Kriegs Brett) für den Krieg an.',
                                        color=discord.Color.green())
            annoEmbed.add_field(name='ℹ  Zusammenfassung', value=f' - Wo: {area}\n - Wann (Ingame): {day} um {time}\n - Wann (Discord): {__meetingTime}\n - Gegen: {enemy}')
            annoEmbed.add_field(name='🛠  Denkt bitte an', value='- [buff food](https://www.google.com/)\n- [war builds](https://www.google.com/)')
        elif type == 'war_defense':
            annoEmbed = discord.Embed(title=f'🛡  Das Kriegshorn ruft - Wir werden angegriffen!',
                                        description=f'Am **{day}** um **{time}** müssen wir unser geliebtes **{area}**\n gegen **{enemy}** verteidigen. Meldet euch bitte __rechtzeitig__ in {area}, am War Board (Kriegs Brett) für den Krieg an.',
                                        color=discord.Color.green())
            annoEmbed.add_field(name='ℹ  Zusammenfassung', value=f' - Wo: {area}\n - Wann (Ingame): {day} um {time}\n - Wann (Discord): {__meetingTime}')
            annoEmbed.add_field(name='🛠  Denkt bitte an', value='- [buff food](https://www.google.com/)\n- [corrupted perks](https://www.google.com/)')
        annoEmbed.set_footer(text=f'The Forgotten Team - Forgotten-Hydra Discord Bot {self.botVersion}', icon_url=self.logoPath)
        return annoEmbed
    
    def anno_embed_inv(self, area, day, time):
        """TODO"""
        annoEmbed = discord.Embed(title=f'',
                                    description=f'**Area:** {area}\n**Time:** {time}\n**Day:** {day}',
                                    color=discord.Color.green())
        annoEmbed.set_footer(text=f'The Forgotten Team - Forgotten-Hydra Discord Bot {self.botVersion}', icon_url=self.logoPath)
        return annoEmbed
    
    def delivered_embed(self, ctx: commands.Context, channelId):
        """TODO"""
        deliveredEmbed = discord.Embed(title=f'{self.annonewTitle} - Ankündigung wurde veröffentlicht!',
                                    description=f'{ctx.message.author.mention} deine Ankündigung wurde im Channel <#{channelId}> gepostet!',
                                    color=discord.Color.green())
        return deliveredEmbed
    
    def no_argument_embed(self):
        """TODO"""
        noArgumentEmbed = discord.Embed(title=f'{self.annonewTitle} - Gegner Name fehlt.',
                                    description='Du hast keinen Gegner angegeben. Bitte gib den Gegner an, wenn du "Angriffskrieg" oder "Verteidigungskrieg" auswählst.',
                                    color=discord.Color.red())
        noArgumentEmbed.add_field(name='Beispiele', value='✅ Richtige schreibweiße:\n`>annonew Falling-Moon`\n\n⛔ Falsche Schreibweise:\n`>annonew Falling Moon`')                       
        return noArgumentEmbed
     
    class AnnonewView(View):
        """Creates a VIEW sup class with dropdown menu and buttons.
        Interactions return certain values"""

        def __init__(self, ctx, config):
            self.ctx = ctx
            self.buttonRes = None
            self.slectRes = None
            self.config = config 
            self.timeout = int(self.config.get('dc_announcement_commands', 'view_timeout_value'))
            super().__init__(timeout= self.timeout)

        __areasDic = {
            'First Light': 'Erstes Licht',
            'Monach\'s Bluffs': 'Königsfels',
            'Everfall': 'Immerfall',
            'Windsward': 'Windkreis',
            'Cutless Keys': 'Entermesserriff',
            'Reekwater': 'Brackwasser',
            'Ebonscale Reach': 'Lichtholz',
            'Weaver\'s Fen': 'Webermoor',
            'Restless Shore': 'Unstete Küste',
            'Mourningdale': 'Klagental',
        }

        __areas = []
        for __area in __areasDic:
            __areas.append(discord.SelectOption(label=__area, value=__area + ' (' + __areasDic[__area] + ')', description=__areasDic[__area]))

        def disabled_all_button(self):
            """Sets all buttons with specific names to disabled"""
            for b in self.children:
                if b.custom_id == 'war_agression_button' or b.custom_id == 'war_defense_button' or b.custom_id == 'invasion_button' or b.custom_id == 'cancel_button':
                    b.disabled = True
        
        def enable_select(self):
            """Sets all dropdown menu with certain names to enabled"""
            for b in self.children:
                if b.custom_id == 'area_select':
                    b.disabled = False
        
        async def on_timeout(self):
            timeoutEmbed = discord.Embed(title='Timeout!',
                                        description=f'Aus versicherungstechnische Gründe haben Sie nur {self.timeout} Sekunden Zeit mit der Nachricht zu interagieren. Führe denn Befehl erneut aus.',
                                        color=discord.Color.red())
            await self.ctx.send(embed=timeoutEmbed)
            self.stop()
        
        async def on_error(self, error: Exception, item, interaction): # TODO Not tested!
            errorEmbed = discord.Embed(title='Something went wrong!',
                                        description=f'**This command is not available here**\n||{error}||',
                                        color=discord.Color.red())
            await interaction.response.send_message(view=errorEmbed)
            self.stop()

        @discord.ui.button(label="Angriffskrieg",
                            style=discord.ButtonStyle.secondary,
                            custom_id="war_agression_button",
                            emoji='⚔')
        async def button_war_agression(self, button, interaction):
            self.buttonRes = 'war_agression'
            self.disabled_all_button()
            button.style = discord.ButtonStyle.primary
            self.enable_select()
            await interaction.response.edit_message(view=self)
        
        @discord.ui.button(label="Verteidigungskrieg",
                            style=discord.ButtonStyle.secondary,
                            custom_id="war_defense_button",
                            emoji='🛡')
        async def button_war_defense(self, button, interaction):
            self.buttonRes = 'war_defense'
            self.disabled_all_button()
            button.style = discord.ButtonStyle.primary
            self.enable_select()
            await interaction.response.edit_message(view=self)
        
        @discord.ui.button(label="Invasion",
                            style=discord.ButtonStyle.secondary,
                            custom_id="invasion_button",
                            emoji='🕷')
        async def button_invasion(self, button, interaction):
            self.buttonRes = 'invasion'
            self.disabled_all_button()
            button.style = discord.ButtonStyle.primary
            self.enable_select()
            await interaction.response.edit_message(view=self)
        
        @discord.ui.button(label="Abbrechen",
                            style=discord.ButtonStyle.red,
                            custom_id="cancel_button",
                            emoji='✖')
        async def button_cancel(self, button, interaction):
            self.buttonRes = 'CANCEL'
            self.disabled_all_button()
            await interaction.response.edit_message(view=self)
            self.stop()
        
        @discord.ui.select(placeholder='Wo?',
                            custom_id='area_select',
                            min_values=1, 
                            max_values=1,
                            options=__areas, 
                            disabled=True)
        async def select_callback(self, select, interaction: discord.Interaction):
            self.slectRes = interaction.data['values'][0]
            select.disabled = True
            select.placeholder = self.slectRes
            await interaction.response.edit_message(view=self)
            self.stop()
        
    class TimeView(View):
        """Creates a VIEW sup class with dropdown menu.
        Interactions return certain values"""

        def __init__(self, ctx, config):
            self.ctx = ctx
            self.slectRes = None
            self.buttonRes = None
            self.config = config
            self.timeout = int(self.config.get('dc_announcement_commands', 'view_timeout_value'))
            super().__init__(timeout= self.timeout)

        time_options = []
        for i in range(16, 24):
            time_options.append(discord.SelectOption(label=f'{i}:00', value=f'{i}:00'))
            time_options.append(discord.SelectOption(label=f'{i}:30', value=f'{i}:30'))
        
        async def on_timeout(self):
            timeoutEmbed = discord.Embed(title='Timeout!',
                                        description=f'Aus versicherungstechnische Gründe haben Sie nur {self.timeout} Sekunden Zeit mit der Nachricht zu interagieren. Führe denn Befehl erneut aus.',
                                        color=discord.Color.red())
            await self.ctx.send(embed=timeoutEmbed)
            self.stop()
        
        async def on_error(self, error: Exception, item, interaction): # TODO Not tested!
            errorEmbed = discord.Embed(title='Something went wrong!',
                                        description=f'**This command is not available here**\n||{error}||',
                                        color=discord.Color.red())
            await interaction.response.send_message(view=errorEmbed)
            self.stop()
        
        @discord.ui.button(label="Abbrechen",
                            style=discord.ButtonStyle.red,
                            custom_id="cancel_button",
                            emoji='✖')
        async def button_cancel(self, button, interaction):
            self.buttonRes = 'CANCEL'
            await interaction.response.edit_message(view=self)
            self.stop()

        @discord.ui.select(placeholder='Wann? (Uhrzeit)',
                            custom_id='time_select',
                            min_values=1, 
                            max_values=1,
                            options=time_options)
        async def select_callback(self, select, interaction: discord.Interaction):
            self.slectRes = interaction.data['values'][0]
            select.disabled = True
            select.placeholder = self.slectRes
            await interaction.response.edit_message(view=self)
            self.stop()

    class DateView(View):
        """Creates a VIEW sup class with dropdown menu and buttons.
        Interactions return certain values"""

        def __init__(self, ctx, config):
            self.ctx = ctx
            self.slectRes = None
            self.buttonRes = None
            self.config = config
            self.timeout = int(self.config.get('dc_announcement_commands', 'view_timeout_value'))
            super().__init__(timeout= self.timeout)

        today = datetime.now()
        time_options = []
        for i in range(5):
            timestr = today + timedelta(days=i)
            timestr = timestr.strftime("%d.%m (%a)")
            time_options.append(discord.SelectOption(label=timestr, value=timestr))
        
        async def on_timeout(self):
            timeoutEmbed = discord.Embed(title='Timeout!',
                                        description=f'Aus versicherungstechnische Gründe haben Sie nur {self.timeout} Sekunden Zeit mit der Nachricht zu interagieren. Führe denn Befehl erneut aus.',
                                        color=discord.Color.red())
            await self.ctx.send(embed=timeoutEmbed)
            self.stop()
        
        async def on_error(self, error: Exception, item, interaction): # TODO Not tested!
            errorEmbed = discord.Embed(title='Something went wrong!',
                                        description=f'**This command is not available here**\n||{error}||',
                                        color=discord.Color.red())
            await interaction.response.send_message(view=errorEmbed)
            self.stop()
        
        @discord.ui.button(label="Abbrechen",
                            style=discord.ButtonStyle.red,
                            custom_id="cancel_button",
                            emoji='✖')
        async def button_cancel(self, button, interaction):
            self.buttonRes = 'CANCEL'
            await interaction.response.edit_message(view=self)
            self.stop()

        @discord.ui.select(placeholder='Wann? (Datum)',
                            custom_id='time_select',
                            min_values=1, 
                            max_values=1,
                            options=time_options)
        async def select_callback(self, select, interaction: discord.Interaction):
            self.slectRes = interaction.data['values'][0]
            select.disabled = True
            select.placeholder = self.slectRes
            await interaction.response.edit_message(view=self)
            self.stop()
    
    class AnnouncementView(View):
        """Creates a VIEW sup class with dropdown menu and buttons.
        Interactions return certain values"""

        def __init__(self, ctx, config):
            self.ctx = ctx
            self.buttonRes = None
            self.config = config
            self.timeout = int(self.config.get('dc_announcement_commands', 'view_timeout_value'))
            super().__init__(timeout= self.timeout)

        async def on_timeout(self):
            timeoutEmbed = discord.Embed(title='Timeout!',
                                        description=f'Aus versicherungstechnische Gründe haben Sie nur {self.timeout} Sekunden Zeit mit der Nachricht zu interagieren. Führe denn Befehl erneut aus.',
                                        color=discord.Color.red())
            await self.ctx.send(embed=timeoutEmbed)
            self.stop()
        
        async def on_error(self, error: Exception, item, interaction): # TODO Not tested!
            errorEmbed = discord.Embed(title='Something went wrong!',
                                        description=f'**This command is not available here**\n||{error}||',
                                        color=discord.Color.red())
            await interaction.response.send_message(view=errorEmbed)
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

    @commands.command()
    async def annonew(self, ctx: commands.Context, *args: str):
        """Creates a sequence whereby an announcement 
        is sent to a target channel at the end."""
        # command sequence
        try:
            for i in ctx.author.roles:
                if i.id == int(self.config['role']['bot_commander']):
                    # all variable are loaded
                    enemy = ''
                    annoNewEmbed = self.anno_new_embed()
                    announcementChannelId = int(self.config.get('dc_channels', 'announcement_id'))
                    serverId = int(self.config.get('dc_server', 'id'))
                    view1 = self.AnnonewView(ctx, self.config)
                    view2 = self.DateView(ctx, self.config)
                    view3 = self.TimeView(ctx, self.config)
                    # ---------- view1 ----------
                    # AnnonewView and annoNewEmbed is sent to the channel.
                    # the bot waits for an interaction or a time-out.
                    msg = await ctx.send(embed=annoNewEmbed, view=view1)
                    await view1.wait()
                    if view1.buttonRes == None or view1.slectRes == None or view1.buttonRes == 'CANCEL':
                        if view1.buttonRes == 'CANCEL':
                            await ctx.message.delete()
                        await msg.delete()
                        return
                    # ---------- view1.5 ----------
                    # if no argument value is given no_argument_embed 
                    # is sent and the command is aborted
                    if view1.buttonRes == 'war_defense' or view1.buttonRes == 'war_agression':
                        try:
                            enemy = args[0].replace('_', ' ')
                        except:
                            noArgumentEmbed = self.no_argument_embed()
                            await ctx.send(embed=noArgumentEmbed)
                            await msg.delete()
                            return 
                    # ---------- view2 ----------
                    # DateView is sent to the channel.
                    # the bot waits for an interaction or a time-out.
                    await msg.edit(view=view2)
                    await view2.wait()
                    if view2.slectRes == None or view2.buttonRes == 'CANCEL':
                        if view2.buttonRes == 'CANCEL':
                            await ctx.message.delete()
                        await msg.delete()
                        return
                    # ---------- view3 ----------
                    # TimeView is sent to the channel.
                    # the bot waits for an interaction or a time-out.
                    await msg.edit(view=view3)
                    await view3.wait()
                    if view3.slectRes == None or view3.buttonRes == 'CANCEL':
                        if view3.buttonRes == 'CANCEL':
                            await ctx.message.delete()
                        await msg.delete()
                        return
                    # ---------- view4 ----------
                    # depending on the selection anno_embed_inv or anno_embed_war is loaded
                    # selection is sent to the channel.
                    # the bot waits for an interaction or a time-out.
                    # if the value SEND comes back from the interaction 
                    # the generated embed is sent to the target channel
                    if enemy == '':
                        annoEmbed = self.anno_embed_inv(view1.slectRes, view2.slectRes, view3.slectRes)
                    else:
                        annoEmbed = self.anno_embed_war(view1.buttonRes, view1.slectRes, view2.slectRes, view3.slectRes, enemy)
                    view4 = self.AnnouncementView(ctx, self.config)
                    await msg.edit(embed=annoEmbed , view=view4)
                    await view4.wait()
                    if view4.buttonRes == None or view4.buttonRes == 'CANCEL':
                        if view4.buttonRes == 'CANCEL':
                            await ctx.message.delete()
                        await msg.delete()
                        return
                    if view4.buttonRes == 'SEND':
                        if ctx.guild.id == serverId:
                            await self.bot.get_channel(announcementChannelId).send('@everyone', embed=annoEmbed)
                        deliveredEmbed = self.delivered_embed(ctx, announcementChannelId)
                        await ctx.send(embed=deliveredEmbed)
                        await msg.delete()
        except Exception as e:
            await ctx.send(embed=self.error_embed(e))

def setup(bot: commands.Bot):
    bot.add_cog(Announcement(bot))
