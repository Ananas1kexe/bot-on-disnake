import disnake
import aiosqlite
from disnake.ext import commands


class datebase(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    
    @commands.Cog.listener()
    async def on_ready(self):
        async with aiosqlite.connect("main.db") as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS warnings (
                    user_id INTEGER PRIMARY KEY,
                    warn_id INTEGER,
                    reason TEXT
                )
                """)
            await db.commit()
        
        
def setup(bot: commands.Bot):
    bot.add_cog(datebase(bot))