from datetime import datetime, timedelta

import discord
from messages.announcement import AnnouncementMessages
from messages.generel import GenerelMessages
from core.logging_handler import UserLoggingHandler
from core.general_functions import GeneralFunctions
from discord.ext import commands
from discord.ui.view import View


class Announcement(commands.Cog, name="Announcement"):
    """TODO"""

    def __init__(self, bot: commands.Bot):
        self.log = UserLoggingHandler('announcement')
        self.a_embed = AnnouncementMessages(bot)
        self.g_embed = GenerelMessages(bot)
        self.bot = bot
        self.annonewTitle = 'Ankündigung'

    class AnnonewView(View):
        """Creates a VIEW sup class with dropdown menu and buttons.
        Interactions return certain values"""

        def __init__(self, ctx: commands.Context, config, log: UserLoggingHandler):
            self.log = log
            self.ctx = ctx
            self.buttonRes = None
            self.slectRes = None
            self.config = config
            self.timeout = int(self.config.get(
                'dc_announcement_commands', 'view_timeout_value'))
            super().__init__(timeout=self.timeout)

        __areasDic = {
            'First Light': 'Erstes Licht',
            'Monarch\'s Bluffs': 'Königsfels',
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
            __areas.append(discord.SelectOption(label=__area, value=__area +
                           ' (' + __areasDic[__area] + ')', description=__areasDic[__area]))

        def disabled_all_button(self):
            """Sets all buttons with specific names to disabled"""
            for b in self.children:
                if b.custom_id == 'war_attack_button' or b.custom_id == 'war_defense_button' or b.custom_id == 'invasion_button' or b.custom_id == 'push_button':
                    b.disabled = True

        def enable_select(self):
            """Sets all dropdown menu with certain names to enabled"""
            for b in self.children:
                if b.custom_id == 'area_select':
                    b.disabled = False

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

        @discord.ui.button(label="Angriffskrieg",
                           style=discord.ButtonStyle.secondary,
                           custom_id="war_attack_button",
                           emoji='⚔')
        async def button_war_attack(self, button, interaction):
            self.buttonRes = 'war_attack'
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

        @discord.ui.button(label="PVP-Push",
                           style=discord.ButtonStyle.secondary,
                           custom_id="push_button",
                           emoji='✊')
        async def button_push(self, button, interaction):
            self.buttonRes = 'push'
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

        def __init__(self, ctx: commands.Context, config, log: UserLoggingHandler):
            self.log = log
            self.ctx = ctx
            self.slectRes = None
            self.buttonRes = None
            self.config = config
            self.timeout = int(self.config.get(
                'dc_announcement_commands', 'view_timeout_value'))
            super().__init__(timeout=self.timeout)

        time_options = []
        for i in range(16, 24):
            time_options.append(discord.SelectOption(
                label=f'{i}:00', value=f'{i}:00'))
            time_options.append(discord.SelectOption(
                label=f'{i}:30', value=f'{i}:30'))

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

        def __init__(self, ctx: commands.Context, config, log: UserLoggingHandler):
            self.log = log
            self.ctx = ctx
            self.slectRes = None
            self.buttonRes = None
            self.config = config
            self.timeout = int(self.config.get(
                'dc_announcement_commands', 'view_timeout_value'))
            super().__init__(timeout=self.timeout)

        today = datetime.now()
        time_options = []
        for i in range(5):
            timestr = today + timedelta(days=i)
            timestr = timestr.strftime("%d.%m (%a)")
            time_options.append(discord.SelectOption(
                label=timestr, value=timestr))

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

        def __init__(self, ctx: commands.Context, config, log: UserLoggingHandler):
            self.log = log
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

    @commands.command()
    async def annonew(self, ctx: commands.Context, *args: str):
        """Creates a sequence whereby an announcement 
        is sent to a target channel at the end."""
        # Load config
        self.config = GeneralFunctions(self.bot).load_config()
        # command sequence
        self.log.info(f'[{ctx.author}] called command annonew')
        if GeneralFunctions(self.bot).user_authorization(ctx, self.config['role']['bot_commander']):
            try:
                # all variable are loaded
                enemy = ''
                annoNewEmbed = self.a_embed.info_text(
                    self.annonewTitle)
                announcementChannelId = int(
                    self.config.get('dc_channels', 'announcement_id'))
                serverId = int(self.config.get('dc_server', 'id'))
                view1 = self.AnnonewView(ctx, self.config, self.log)
                view2 = self.DateView(ctx, self.config, self.log)
                view3 = self.TimeView(ctx, self.config, self.log)
                # ---------- view1 ----------
                # AnnonewView and annoNewEmbed is sent to the channel.
                # the bot waits for an interaction or a time-out.
                msg = await ctx.send(embed=annoNewEmbed, view=view1)
                await view1.wait()
                if view1.buttonRes == None or view1.slectRes == None or view1.buttonRes == 'CANCEL':
                    if view1.buttonRes == 'CANCEL':
                        await ctx.message.delete()
                    await msg.delete()
                    self.log.info(
                        f'[{ctx.author}] command annonew was terminated')
                    return
                # ---------- view1.5 ----------
                # if no argument value is given no_argument_embed
                # is sent and the command is aborted
                if view1.buttonRes == 'war_defense' or view1.buttonRes == 'war_attack' or view1.buttonRes == 'push':
                    try:
                        enemy = args[0].replace('_', ' ')
                    except:
                        noArgumentEmbed = self.g_embed.wrong_argument(
                            ctx, '', self.annonewTitle)
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
                    self.log.info(
                        f'[{ctx.author}] command annonew was terminated')
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
                    self.log.info(
                        f'[{ctx.author}] command annonew was terminated')
                    return
                # ---------- view4 ----------
                # depending on the selection anno_embed_inv or anno_embed_war is loaded
                # selection is sent to the channel.
                # the bot waits for an interaction or a time-out.
                # if the value SEND comes back from the interaction
                # the generated embed is sent to the target channel
                if enemy == '':
                    annoEmbed = self.a_embed.inv(
                        ctx, view1.slectRes, view2.slectRes, view3.slectRes)
                elif view1.buttonRes == 'war_defense' or view1.buttonRes == 'war_attack':
                    annoEmbed = self.a_embed.war(
                        ctx, view1.buttonRes, view1.slectRes, view2.slectRes, view3.slectRes, enemy)
                else:
                    annoEmbed = self.a_embed.push(
                        ctx, view1.slectRes, view2.slectRes, view3.slectRes, enemy)
                view4 = self.AnnouncementView(ctx, self.config, self.log)
                await msg.edit(embed=annoEmbed, view=view4)
                await view4.wait()
                if view4.buttonRes == None or view4.buttonRes == 'CANCEL':
                    if view4.buttonRes == 'CANCEL':
                        await ctx.message.delete()
                    await msg.delete()
                    self.log.info(
                        f'[{ctx.author}] command annonew was terminated')
                    return
                elif view4.buttonRes == 'SEND':
                    if ctx.guild.id == serverId:
                        __memberRollId = self.config.get('role', 'member')
                        __memberRollId = GeneralFunctions(
                            self.bot).config_str_to_list(__memberRollId)
                        __rollstr = ''
                        for m in __memberRollId:
                            __rollstr += f'<@&{str(m)}> '
                        await self.bot.get_channel(announcementChannelId).send(f'{__rollstr}', embed=annoEmbed)
                        del __memberRollId, __rollstr
                    deliveredEmbed = self.a_embed.delivered(
                        ctx, announcementChannelId, self.annonewTitle)
                    self.log.info(
                        f'[{ctx.author}] delivered announcement to channel {announcementChannelId}')
                    await ctx.send(embed=deliveredEmbed)
                    await msg.delete()
                del view1, view2, view3, view4, msg, annoNewEmbed, annoEmbed, deliveredEmbed
            except Exception as e:
                await ctx.send(embed=self.g_embed.error(self.annonewTitle, e))
                self.log.warning(
                    f'[{ctx.author}] Error by annonew command ({e})')
        else:
            pass

    @commands.command()
    async def annosetup(self, ctx: commands.Context, *args: str):
        """Sets up the announcement channel."""
        # command sequence
        self.log.info(f'[{ctx.author}] called command annosetup')
        if GeneralFunctions(self.bot).user_authorization(ctx, self.config['role']['bot_commander']):
            try:
                if args[0] == '-cset':
                    if len(args[1]) == 18:
                        # Update the config
                        self.config['dc_channels']['announcement_id'] = args[1]
                        # Write changes back to file
                        with open('config.ini', 'w') as conf:
                            self.config.write(conf)
                        await ctx.send(embed=self.a_embed.config_saved(ctx, args[1], self.annonewTitle))
                        self.log.info(
                            f'[{ctx.author}] announcement channel set to {args[1]}')
                    else:
                        await ctx.send(embed=self.g_embed.error(self.annonewTitle, f'invalid argument: {args[1]}'))
                else:
                    await ctx.send(embed=self.g_embed.error(self.annonewTitle, f'invalid argument: {args[0]}'))
            except IndexError as e:
                await ctx.send(embed=self.g_embed.error(self.annonewTitle, 'no argument specified'))
            except Exception as e:
                await ctx.send(embed=self.g_embed.error(self.annonewTitle, e))
                self.log.warning(
                    f'[{ctx.author}] error by annosetup command ({e})')
        else:
            pass


def setup(bot: commands.Bot):
    bot.add_cog(Announcement(bot))
