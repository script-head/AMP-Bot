import os
import configparser

class Defaults:
    name = "a minecraft server"
    token = None
    command_prefix = "srv!"
    dev_role_id = None
    admin_role_ids = []
    senior_admin_role_id = None
    amp_username = None
    amp_password = None
    amp_panel_url = None

class Config:
    def __init__(self):

        self.config_file = "config.ini"

        config = configparser.ConfigParser(interpolation=None)
        config.read(self.config_file, encoding="utf-8")

        sections = {"Bot", "AMP"}.difference(config.sections())
        if sections:
            print("Could not load a section in the config file, please obtain a new config file from the github repo")
            os._exit(1)
        self.name = config.get("Bot", "Name", fallback=Defaults.name)
        self._token = config.get("Bot", "Token", fallback=Defaults.token)
        self.command_prefix = config.get("Bot", "Command_Prefix", fallback=Defaults.command_prefix)
        self.dev_role_id = config.get("Bot", "Developer_Role_ID", fallback=Defaults.dev_role_id)
        self.admin_role_ids = config.get("Bot", "Admin_Role_IDs", fallback=Defaults.admin_role_ids)
        self.senior_admin_role_id = config.get("Bot", "Senior_Admin_Role_ID", fallback=Defaults.senior_admin_role_id)
        self.amp_username = config.get("AMP", "AMP_Username", fallback=Defaults.amp_username)
        self.amp_password = config.get("AMP", "AMP_Password", fallback=Defaults.amp_password)
        self.amp_panel_url = config.get("AMP", "URL", fallback=Defaults.amp_panel_url)

        self.check()

    def check(self):
        if not self._token:
            print("No token was specified in the config, please put your bot's token in the config.")
            os._exit(1)

        if len(self.admin_role_ids) is not 0:
            try:
                self.admin_role_ids = list(self.admin_role_ids.split())
            except:
                self.admin_role_ids = Defaults.admin_role_ids

        if not self.amp_username:
            print("No AMP username was specified in the config")
            os._exit(1)

        if not self.amp_password:
            print("No AMP password was specified in the config")
            os._exit(1)

        if not self.amp_panel_url:
            print("No AMP panel url was specified in the config")
            os._exit(1)
