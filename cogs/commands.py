import disnake
import io

from PIL import Image
from disnake.ext import commands
from disnake.utils import format_dt



class Commands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(description="role info")
    async def role_info(self, inter: disnake.AppCommandInter, role: disnake.Role):
        role_name = role.name
        role_id = role.id
        role_color = role.color
        
        embed = disnake.Embed(
            title=f'Role: {role.mention}',
            description=(
                f"Role name: @{role_name}\n"
                f"Role id: `{role_id}`\n"
                f"Role color: `{role_color}`\n"
            ),
            color=disnake.Color.from_rgb(255,255,255)
        )
        await inter.response.send_message(embed=embed)
        
    @commands.slash_command(description="user_info")
    async def user_info(self, inter: disnake.AppCommandInter, member: disnake.Member = None):
        if member is None:
            member = inter.author
        
        joined_at = format_dt(member.joined_at, style="F")
        created_at = format_dt(inter.guild.created_at, style='F')
        
        embed = disnake.Embed(
            title=f'About @{member.name}',
            description=(
                f"Member name: @{member.name} ({member.mention})\n"
                f"Member id: `{member.id}`\n"
                f"Created at: {created_at}\n"
                f"Joined at: {joined_at}\n"

            ),
            color=disnake.Color.from_rgb(255,255,255)
        )
        embed.set_thumbnail(url=member.display_avatar.url if member.avatar else member.default_avatar.url)
        await inter.response.send_message(embed=embed)   
        
    @commands.slash_command(description="server_info")
    async def server_info(self, inter: disnake.AppCommandInter):
        guild = inter.guild
        server_name = guild.name
        server_id = guild.id
        server_owner_name = guild.owner.name
        members_count = guild.member_count
        bots = len([member for member in guild.members if member.bot])
        human_count = members_count - bots
        server_icon = guild.icon.url if guild.icon else None 
        created_at = format_dt(guild.created_at, style='F')
        
        embed = disnake.Embed(
            title=f'About {server_name}',
            description=(
                f"Server name: {server_name}\n"
                f"Server id: `{server_id}`\n"
                f"Owner: @{server_owner_name} ({guild.owner.mention})\n"
                f"Created: {created_at}\n"
                f"Human count: `{human_count}`\n"

            ),
            color=disnake.Color.from_rgb(255,255,255)
        )
        embed.set_thumbnail(url=server_icon)
        await inter.response.send_message(embed=embed)
        
        

    @commands.slash_command(description="create suggest")
    async def suggest(self, inter: disnake.AppCommandInter, suggest: str):
        
        embed = disnake.Embed(
            title="New Suggest!",
            description=(
                f"Author: @{inter.author.name}"
                f"Suggest: {suggest}"
                ),
            color=disnake.Color.yellow()
        )
        message = await inter.response.send_message(embed=embed)
        msg = await inter.original_message()
        theard = await msg.create_thread(name=f"sugest from a {inter.author.name}")
        msg_theread = await theard.send(embed=embed)
        await msg_theread.pin()
        
        
    @commands.slash_command(description="ping")
    async def ping(self, inter: disnake.AppCommandInter):

        guild_ping = (
            round(self.bot.latency, 3)
        )

        embed = disnake.Embed(
            title=f"Pong!\n Guild ping: `{guild_ping}` s",
            color=disnake.Color.from_rgb(255,255,255)
        )
        
        await inter.response.send_message(embed=embed)
    
    
    @commands.slash_command(description="avatar")
    async def avatar(self, inter: disnake.AppCommandInter, member: disnake.Member = None):
        
        if member is None:
            member = inter.author

        embed = disnake.Embed(
            title=f"Avatar: {member}",
            color=disnake.Color.from_rgb(255,255,255)
        )
        embed.set_image(url=member.avatar.url if member.avatar else member.default_avatar.url)
        
        await inter.response.send_message(embed=embed)
        
    
    @commands.slash_command(description="say message")
    async def say(self, inter: disnake.AppCommandInter, message: str, channel: disnake.TextChannel = None, embed: bool = commands.Param(choices={"True": True, "False": False})):
        
        if channel is None:
            channel = inter.channel
        
        if embed == True:
            embed = disnake.Embed(
                description=message,
                color=disnake.Color.from_rgb(255,255,255)
            )
            await channel.send(embed=embed)
        else:
            await channel.send(message)
        await inter.response.send_message("Succes", ephemeral=True)
        
    
    @commands.slash_command(description="show color")
    async def color(self, inter: disnake.AppCommandInter, hex: str):
        
        if not hex.startswith("#"):
            hex = f"#{hex}"
        img = Image.new('RGB', (120, 40), hex)
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        
        file = disnake.File(fp=buffer, filename="color.png")

        embed = disnake.Embed(
            title=f"Color: {hex}",
            color=disnake.Color.from_rgb(255,255,255)
        )
        embed.set_image(url="attachment://color.png")
        
        await inter.response.send_message(embed=embed, file=file)
def setup(bot: commands.Bot):
    bot.add_cog(Commands(bot))