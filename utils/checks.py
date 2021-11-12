from discord.ext import commands
from utils.config import Config
config = Config()

class admin_only(commands.CommandError):
    pass

class senior_admin_only(commands.CommandError):
    pass

class dev_only(commands.CommandError):
    pass

def is_dev():
    def predicate(ctx):
        for role in ctx.message.author.roles:
            if role.id == config.dev_role_id:
                return True
        else:
            raise dev_only
    return commands.check(predicate)

def is_admin():
    def predicate(ctx):
        for role in ctx.message.author.roles:
            if role.id in config.admin_role_ids or role.id == config.dev_role_id:
                return True
        raise admin_only
    return commands.check(predicate)

def is_senior_admin():
    def predicate(ctx):
        for role in ctx.message.author.roles:
            if role.id == config.senior_admin_role_id or role.id in config.admin_role_ids or role.id == config.dev_role_id:
                return True
        raise senior_admin_only
    return commands.check(predicate)