import disnake
from disnake.ext import commands


class datebase(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
        
def setup(bot: commands.Bot):
    bot.add_cog(datebase(bot))