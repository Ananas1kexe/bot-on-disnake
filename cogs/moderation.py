import disnake
import aiosqlite
from datetime import datetime, timedelta
from disnake.ext import commands


class moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.slash_command(description="slowmode")
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, inter: disnake.AppCommandInter, duration: int, channel: disnake.TextChannel = None):
        if channel is None:
            channel = inter.channel
        
        try:
            await channel.edit(slowmode_delay=duration)
        except disnake.Forbidden:
            return
        
        embed = disnake.Embed(
            title="Succes",
            description=f"Duration: {duration}\nChannel: {channel.mention}",
            color=disnake.Color.green()
        )

        await inter.response.send_message(embed=embed)
    
    @commands.slash_command(description="clear")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, inter: disnake.AppCommandInter, amout: int):
        
        await inter.channel.purge(limit=amout)
        embed = disnake.Embed(
            title="Succes",
            description=f"Amount: {amout}\nChannel: {inter.channel.mention}",
            color=disnake.Color.green()
        )
        await inter.response.send_message(embed=embed)
    

    @commands.slash_command(description="kick")
    async def kick(self, inter: disnake.AppCommandInter, member: disnake.Member, reason: str = None):
        
        if reason is None:
            reason = "No reason"
            
            
        await member.kick(reason=reason)
        embed = disnake.Embed(
            title="Succes",
            description=f"Member: {member.name}\nReason: {reason}",
            color=disnake.Color.green()
        )
        await inter.response.send_message(embed=embed)

    @commands.slash_command(description="warn")
    async def warn(self, inter: disnake.AppCommandInter, member: disnake.Member, reason: str = None):
        async with aiosqlite.connect("main.db") as db:
            async with db.execute("""
                SELECT COUNT(*) FROM warnings
                WHERE user_id = ?
                """, (member.id,)) as cursor:
                warning_count = await cursor.fetchone()
                warning_count = warning_count[0] + 1
            await db.execute("""
                INSERT OR REPLACE INTO warnings (user_id, warn_id, reason)
                VALUES (?, ?, ?)
                """, (member.id, warning_count, reason))
            await db.commit()

        
        embed = disnake.Embed(
            title="Succes",
            description=f"Member: @{member.name}({member.mention})\nReason: {reason}\nWarn ID: **`{warning_count}`**",
            color=disnake.Color.green()
        )
        
        await inter.response.send_message(embed=embed)
    
    


    @commands.slash_command(description="unwarn")
    async def unwarn(self, inter: disnake.AppCommandInter, member: disnake.Member, id: int, reason: str = None):
        async with aiosqlite.connect("main.db") as db:
            cursor = await db.execute("""
                DELETE FROM warnings WHERE user_id = ? AND warn_id = ?
                """, (member.id, id))
            await db.commit()
            deleted = cursor.rowcount
            
        if deleted == 0:
            embed = disnake.Embed(
                description=f"Warn with ID {id} not found for user {member.display_name}.",
                color=disnake.Color.red()
            )
            await inter.response.send_message(embed=embed, ephemeral=True)

        else:
            embed = disnake.Embed(
                title="Succes",
                description=f"Member: {member.name}\nReason: {reason}",
                color=disnake.Color.green()
            )
            
            await inter.response.send_message(embed=embed)
    


    @commands.slash_command(description="mute")
    async def mute(self, inter: disnake.AppCommandInter, member: disnake.Member, duration: int, reason: str = None):

        until_time = timedelta(minutes=duration)
        await member.timeout(duration=until_time, reason=reason)
        
        embed = disnake.Embed(
            title="Succes",
            description=f"Member: {member.name}\nReason: {reason}\nDuration: {duration} min"
        )
        
        await inter.response.send_message(embed=embed)
    
    
    @commands.slash_command(description="unmute")
    async def unmute(self, inter: disnake.AppCommandInter, member: disnake.Member, reason: str = None):

        await member.timeout(duration=None, reason=reason)
        
        embed = disnake.Embed(
            title="Succes",
            description=f"Member: {member.name}\nReason: {reason}"
        )
        
        await inter.response.send_message(embed=embed)
        
    @commands.slash_command(description="ban")
    async def ban(self, inter: disnake.AppCommandInter, member: disnake.Member, reason: str = None):

        # clean_history_duration=100 or 0
        await member.ban(clean_history_duration=100, reason=reason)
        embed = disnake.Embed(
            title="Succes",
            description=f"Member: {member.name}\nReason: {reason}"
        )
        await inter.response.send_message(embed=embed)
        
    @commands.slash_command(description="unban")
    async def unban(self, inter: disnake.AppCommandInter, member: disnake.User, reason: str = None):

        banned_users = await inter.guild.bans().flatten()
        member_name = member.name
        
        for ban_entry in banned_users:
            user = ban_entry.user
            
            if user.name == member_name:
                await inter.guild.unban(user, reason=reason)
                embed = disnake.Embed(
                    title="Succes",
                    description=f"Member: {member.name}\nReason: {reason}"
                )
                await inter.response.send_message(embed=embed)
            else:
                pass

def setup(bot: commands.Bot):
    bot.add_cog(moderation(bot))