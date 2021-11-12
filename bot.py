import os
import logging

from discord.ext import commands
from utils.config import Config
from utils import amp
from utils import checks

config = Config()

desc = "Server control bot for {}".format(config.name)

bot = commands.Bot(command_prefix=config.command_prefix, description=desc, pm_help=False)

def init_console_logger():
    logger = logging.getLogger("consolelogger")
    format = logging.Formatter("%(asctime)s %(message)s")
    fileHandler = logging.FileHandler("commands.log")
    fileHandler.setFormatter(format)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(format)
    logger.setLevel(logging.INFO)
    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)
init_console_logger()

console_logger = logging.getLogger("consolelogger")

class Server():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def state(self):
        """Gets the server's current state"""
        try:
            state = amp.get_server_state()
        except KeyError:
            amp.get_session_id()
            state = amp.get_server_state()
        await self.bot.say("The server is **{}**".format(state))

    @checks.is_senior_admin()
    @commands.command()
    async def start(self):
        """Starts the server"""
        try:
            state = amp.get_server_state()
        except KeyError:
            amp.get_session_id()
            state = amp.get_server_state()
        if state == "online":
            await self.bot.say("The server is already running")
            return
        elif state == "starting":
            await self.bot.say("The server is already starting")
            return
        else:
            amp.control_power(amp.Power.START)
            await self.bot.say("Starting the server...")

    @checks.is_senior_admin()
    @commands.command()
    async def restart(self):
        """Restarts the server"""
        try:
            state = amp.get_server_state()
        except KeyError:
            amp.get_session_id()
            state = amp.get_server_state()
        if state == "starting":
            await self.bot.say("The server is already starting")
            return
        elif state == "shutting down":
            await self.bot.say("The server is already shutting down")
            return
        else:
            amp.control_power(amp.Power.RESTART)
            await self.bot.say("Restarting the server...")

    @checks.is_senior_admin()
    @commands.command()
    async def stop(self):
        """Stops the server"""
        try:
            state = amp.get_server_state()
        except KeyError:
            amp.get_session_id()
            state = amp.get_server_state()
        if state == "offline":
            await self.bot.say("The server is already stopped")
            return
        elif state == "shutting down":
            await self.bot.say("The server is already shutting down")
            return
        else:
            amp.control_power(amp.Power.STOP)
            await self.bot.say("Stopping the server...")

    @checks.is_senior_admin()
    @commands.command()
    async def kill(self):
        """Kills the server (useful if it isn't responding)"""
        try:
            state = amp.get_server_state()
        except KeyError:
            amp.get_session_id()
            state = amp.get_server_state()
        if state == "offline":
            await self.bot.say("The server is already stopped")
            return
        else:
            amp.control_power(amp.Power.KILL)
            await self.bot.say("Killing the server...")

    @commands.command()
    async def list(self):
        """Gets the list of online players"""
        try:
            state = amp.get_server_state()
        except KeyError:
            amp.get_session_id()
            state = amp.get_server_state()
        if state == "offline":
            await self.bot.say("The server is offline")
            return
        await self.bot.say(amp.get_player_list())

    @checks.is_senior_admin()
    @commands.command(pass_context=True)
    async def sendcommand(self, ctx, *, command:str):
        """Send a console command"""
        try:
            state = amp.get_server_state()
        except KeyError:
            amp.get_session_id()
            state = amp.get_server_state()
        if state == "offline":
            await self.bot.say("The server is offline")
            return
        amp.send_console_command(command)
        console_logger.info("[Console Command] {}: {}".format(ctx.message.author, ctx.message.content.replace("{}{} ".format(config.command_prefix, ctx.command), "")))
        await self.bot.say("Command sent!")

bot.add_cog(Server(bot))

@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.DisabledCommand):
        await bot.send_message(ctx.message.channel, "This command has been disabled")
        return
    if isinstance(error, checks.dev_only):
        await bot.send_message(ctx.message.channel, "This command can only be ran by the server developers")
        return
    if isinstance(error, checks.admin_only):
        await bot.send_message(ctx.message.channel, "This command can only be ran by the discord admins")
        return
    if isinstance(error, checks.senior_admin_only):
        await bot.send_message(ctx.message.channel, "This command can only be ran by the server senior admins")
        return

    # In case the bot failed to send a message to the channel, the try except pass statement is to prevent another error
    try:
        await bot.send_message(ctx.message.channel, error)
    except:
        pass
    print("An error occured while executing the command named {}: {}".format(ctx.command.qualified_name, error))

@bot.event
async def on_ready():
    print("Connected! Logged in as {}/{}".format(bot.user, bot.user.id))
    amp.get_session_id()

@checks.is_dev()
@bot.command(hidden=True, pass_context=True)
async def debug(ctx, *, shit:str):
    import asyncio
    import requests
    import random
    py = "```py\n{}```"
    """This is the part where I make 20,000 typos before I get it right"""
    # "what the fuck is with your variable naming" - EJH2
    # seth seriously what the fuck - Robin
    try:
        rebug = eval(shit)
        if asyncio.iscoroutine(rebug):
            rebug = await rebug
        await bot.say(py.format(rebug))
    except Exception as damnit:
        await bot.say(py.format("{}: {}".format(type(damnit).__name__, damnit)))

@checks.is_dev()
@bot.command(hidden=True, pass_context=True)
async def terminal(ctx, *, command:str):
    """Runs terminal commands and shows the output via a message. Oooh spoopy!"""
    xl = "```xl\n{}```"
    try:
        await bot.send_typing(ctx.message.channel)
        await bot.say(xl.format(os.popen(command).read()))
    except:
        await bot.say("Error, couldn't send command")

@checks.is_dev()
@bot.command(hidden=True)
async def shutdown():
    """Shuts down the bot"""
    await bot.say("Shutting down...")
    amp.logout()
    await bot.logout()

print("Connecting...")
bot.run(config._token)
