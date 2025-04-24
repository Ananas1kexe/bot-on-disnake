import disnake
import io

from PIL import Image
from disnake.ext import commands


class Commands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
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