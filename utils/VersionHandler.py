# ©GO-PC Build
# This project is under a CC0-1.0 License
# (View the license here: https://github.com/GO-PC-Build/DiscordBot/blob/master/LICENSE)

from os import path

from git import Repo


class VersionHandler:
    def __init__(self):
        self.repo = Repo(path.curdir)
        self.remote = self.repo.remote("origin")
        self.version = f"{self.remote.fetch()[0].commit.count():,}"

    @property
    def is_latest(self) -> bool:
        return self.repo.commit() == self.remote.fetch()[0].commit

    def update_version(self) -> None:
        self.remote.pull()
