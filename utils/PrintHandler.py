# ©GO-PC Build
# This project is under a CC0-1.0 License
# (View the license here: https://github.com/GO-PC-Build/DiscordBot/blob/master/LICENSE)

from datetime import datetime

from utilsx.console import Prettier


class PrintHandler:
    def __init__(self, prettier: Prettier):
        self.prettier = prettier

    def printf(self, message: str) -> None:
        self.prettier.print(message, datetime.now())
