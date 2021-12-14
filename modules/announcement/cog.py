from configparser import ConfigParser

import discord
from discord.ext import commands
from discord.ui.view import View


class Announcement(commands.Cog, name="Announcement"):
    """TODO"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        # Load config
        file = 'config.ini'
        self.config = ConfigParser()
        self.config.read(file)
        del file
    
    def error_embed(self, error_message):
        """Returns an error embed"""
        errorEmbed = discord.Embed(title='Something went wrong!',
                                    description=f'**This command is not available here**\n||{error_message}||',
                                    color=discord.Color.red())
        return errorEmbed
    
    def anno_new_embed(self):
        """TODO"""
        annoEmbed = discord.Embed(title='New announcement!',
                                    description='announcement announcement announcement announcement announcement',
                                    color=discord.Color.green())
        return annoEmbed
    
    def anno_embed(self, area, type, time, enemy):
        """TODO"""
        annoEmbed = discord.Embed(title='Announcement',
                                    description=f'**Area:** {area}\n**Type:** {type}\n**Time:** {time}\n**Enemy:** {enemy}',
                                    color=discord.Color.green())
        return annoEmbed
    
    def delivered_embed(self, ctx):
        """TODO"""
        deliveredEmbed = discord.Embed(title='Announcement delivered!',
                                    description=f'{ctx.message.author.mention}?! Announcement delivered!!!!!',
                                    color=discord.Color.green())
        return deliveredEmbed
    
    def no_argument_embed(self):
        """TODO"""
        noArgumentEmbed = discord.Embed(title='No Argument!',
                                    description='Bitte gib den Gegner an\nbuttons "Angriffskrieg" and "Verteidigungskrieg"',
                                    color=discord.Color.red())
        return noArgumentEmbed
     
    class AnnonewView(View):
        """TODO"""

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
            __areas.append(discord.SelectOption(label=__area, value=__area, description=__areasDic[__area]))

        def disabled_all_button(self):
            for b in self.children:
                if b.custom_id == 'war_agression_button' or b.custom_id == 'war_defense_button' or b.custom_id == 'invasion_button' or b.custom_id == 'cancel_button':
                    b.disabled = True
        
        def enable_select(self):
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
        """TODO"""

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

        @discord.ui.select(placeholder='Wann?',
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
        """TODO"""

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
                            style=discord.ButtonStyle.primary,
                            custom_id="send_button",
                            emoji='✔')
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
        """TODO"""
        try:
            for i in ctx.author.roles:
                if i.id == int(self.config['role']['bot_commander']):
                    """TODO"""
                    enemy = ''
                    annoNewEmbed = self.anno_new_embed()
                    announcementChannelId = int(self.config.get('dc_channels', 'announcement_id'))
                    serverId = int(self.config.get('dc_server', 'id'))
                    view1 = self.AnnonewView(ctx, self.config)
                    view2 = self.TimeView(ctx, self.config)
                    # ---------- view1 ----------
                    msg = await ctx.send(embed=annoNewEmbed, view=view1)
                    await view1.wait()
                    if view1.buttonRes == None or view1.slectRes == None or view1.buttonRes == 'CANCEL':
                        if view1.buttonRes == 'CANCEL':
                            await ctx.message.delete()
                        await msg.delete()
                        return
                    # ---------- view1.5 ----------
                    if view1.buttonRes == 'war_defense' or view1.buttonRes == 'war_agression':
                        try:
                            enemy = args[0].split('_')
                        except:
                            noArgumentEmbed = self.no_argument_embed()
                            await msg.delete()
                            await ctx.send(embed=noArgumentEmbed)
                            return
                        
                    # ---------- view2 ----------
                    await msg.edit(view=view2)
                    await view2.wait()
                    if view2.slectRes == None or view2.buttonRes == 'CANCEL':
                        if view2.buttonRes == 'CANCEL':
                            await ctx.message.delete()
                        await msg.delete()
                        return
                    # ---------- view3 ----------
                    annoEmbed = self.anno_embed(view1.slectRes, view1.buttonRes, view2.slectRes, enemy)
                    view3 = self.AnnouncementView(ctx, self.config)
                    await msg.edit(embed=annoEmbed , view=view3)
                    await view3.wait()
                    if view3.buttonRes == None or view3.buttonRes == 'CANCEL':
                        if view3.buttonRes == 'CANCEL':
                            await ctx.message.delete()
                        await msg.delete()
                        return
                    if view3.buttonRes == 'SEND':
                        if ctx.guild.id == serverId:
                            await self.bot.get_channel(announcementChannelId).send(embed=annoEmbed)
                        deliveredEmbed = self.delivered_embed(ctx)
                        await ctx.send(embed=deliveredEmbed)
                        await msg.delete()
        except Exception as e:
            await ctx.send(embed=self.error_embed(e))

def setup(bot: commands.Bot):
    bot.add_cog(Announcement(bot))
