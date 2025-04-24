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
            channel.edit(slowmode_delay=duration)
        except disnake.Forbidden:
            return
        
        embed = disnake.Embed(
            title="Succes",
            description=f"Duration: {duration}\nChannel: {channel.mention}"
        )

        await inter.response.send_message(embed=embed)
    
    @commands.slash_command(description="clear")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, inter: disnake.AppCommandInter, amout: int):
        
        messages = inter.channel.history(limit=int(amout)).flatten()
        await inter.channel.purge(messages)
        
        embed = disnake.Embed(
            title="Succes",
            description=f"Amount: {amout}\nChannel: {inter.channel.mention}"
        )
        await inter.response.send_message(embed=embed)
    

    @commands.slash_command(description="ping")
    async def kick(self, inter: disnake.AppCommandInter, member: disnake.Member, reason: str = None):
        
        if reason is None:
            reason = "No reason"
            
            
        await member.kick(reason=reason)
        embed = disnake.Embed(
            title="Succes",
            description=f"Member: {member.name}\Reason: {reason}"
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