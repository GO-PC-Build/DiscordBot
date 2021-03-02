# ©GO-PC Build
# This project is under a CC0-1.0 License
# (View the license here: https://github.com/GO-PC-Build/DiscordBot/blob/master/LICENSE)

from glob import glob
from os import name, execv, system, environ
from sys import argv, executable, stdout, exit
from distutils.util import strtobool

try:
    from utilsx.console import Prettier, Colors
    from utilsx.discord import BotX
except ImportError:
    print("UtilsX library is missing, attempting to install it...")
    system(("py -3" if name == "nt" else "python3") + " -m pip install -r requirements.txt")
    print("Please reboot this application")
    exit(0)
    raise  # Fixes IDE error


from utils import VersionHandler, PrintHandler
from configparser import ConfigParser
from discord import Intents


# Check if the operating system is linux or windows. (nt = windows)
# If its windows, change the console clear command and the filepath delimiter.
clear, back_slash = "clear", "/"
if name == "nt":
    clear, back_slash = "cls", "\\"

# Read our configuration
cfg = ConfigParser()
cfg.read("config.cfg")


class Bot(BotX):
    """
    The main bot object, this contains our handlers and loads our extensions
    """
    def __init__(self):
        super().__init__(Intents.all())
        system(clear)
        stdout.flush()
        self.prettier = Prettier(colors_enabled=strtobool(cfg["CONSOLE"].get("colors", "true")), auto_strip_message=True)
        self.ph = PrintHandler(self.prettier)
        self.ph.printf("Initializing client...")
        self.prefix = cfg["BOT"].get("prefix", "!")

        self.vm = VersionHandler()
        if strtobool(cfg["UPDATER"].get("enabled", "true")):
            self.check_for_updates()
            self.ph.printf("No updates found, starting bot...")

        self.ph.printf("Started loading extensions.")
        extensions = list(map(lambda extension: extension.replace(back_slash, ".")[:-3], glob("extensions/*.py")))

        for index, _ in enumerate(self.load_extensions(extensions)):
            self.ph.printf(f"Successfully loaded "
                           f"{Colors.light_blue.value + extensions[index].replace('extensions.', '')}")

    @staticmethod
    def restart():
        system(clear)
        stdout.flush()
        execv(executable, ['python'] + argv)

    def check_for_updates(self):
        self.ph.printf("Checking for updates...")
        if not self.vm.is_latest:
            self.ph.printf("Update found! Started updating bot to the latest version...")
            self.vm.update_version()
            self.ph.printf("Successfully updated to the latest version. Rebooting bot.")
            self.restart()

    # def console_handler(self):
    #     data = input("").strip()
    #     if data == "help":
    #         self.prettier.print(f"Interactive Console Help Menu v{self.vm.version}\n"
    #                             "update - Checks if it can update, if it can it will.\n"
    #                             "stop - Kills the bot instance\n"
    #                             "help - This menu")
    #     elif data == "update":
    #         self.check_for_updates()
    #         self.ph.printf("No updates found!")
    #     elif data == "stop":
    #         self.ph.printf("Stopping bot!")
    #         exit(0)
    #     else:
    #         self.ph.printf(f"Couldn't find a command called '{data}'")
    #     self.console_handler()

    async def on_ready(self):
        self.ph.printf(f"Currently running on v{self.vm.version}!")

        # self.ph.printf("Console input ready, type `help` to see all commands.")

        # Thread(target=self.console_handler).start()
        # await self.logout()


if __name__ == "__main__":
    location = cfg["BOT"].get("token_env", "GO_PC_BOT_TOKEN")
    try:
        Bot().run(environ[location])
    except KeyError:
        print(f"{Colors.red.value}ERROR:\n"
              f"No valid bot token was provided on env `{Colors.magenta.value + location + Colors.red.value}`"
              f"{Colors.default.value}\n"
              f"Please create an env variable with name `{Colors.magenta.value + location + Colors.default.value}` "
              f"and place your bot token in it.\n"
              f"Then rerun this script.\n\n"
              f"Or check out this tutorial:\n"
              f"{Colors.light_blue.value}https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html"
              f"{Colors.default.value}")
