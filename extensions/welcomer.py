# ©GO-PC Build
# This project is under a CC0-1.0 License
# (View the license here: https://github.com/GO-PC-Build/DiscordBot/blob/master/LICENSE)

from discord import Member
from discord.ext.commands import Bot
from utilsx.discord import Cog
from utilsx.discord.objects import Field


class AutoWelcome(Cog):
    def __init__(self, bot: Bot):
        super().__init__()
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member: Member):
        try:
            await self.embed(member, "Welkom in de **GO-PC Build** discord server!\n\n"
                                     "Wij geven twee workshops, in deze workshops gaan wij jullie leren hoe je je eigen "
                                     "computer kan bouwen en een OS (Operating System, bijvoorbeeld Windows) installeren!",
                             fields=[Field("🔗 Handige links",
                                           "[Website](http://gpb.go-ao.be) [Quiz](http://gpb.go-ao.be/quiz) "
                                           "[Reserveer/Reservatie](http://gpb.go-ao.be/reserveer)"),
                                     Field("Volg ons",
                                           "[Twitter](https://twitter.com/GOPCBuild) "
                                           "[Facebook](https://www.facebook.com/GOPCBuild) "
                                           "[Instagram](https://www.instagram.com/gopcbuild/)")])
        except Exception:
            pass


def setup(bot: Bot):
    bot.add_cog(AutoWelcome(bot))
