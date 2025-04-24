import os

import logging
import disnake
from disnake.ext import commands
from dotenv import load_dotenv



logging.basicConfig(level=logging.INFO, format=("%(asctime)s - %(levelname)s - %(message)s"), handlers=[logging.FileHandler("bot.log", encoding="utf-8"), logging.StreamHandler()])

load_dotenv()

intents = disnake.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)

bot.load_extensions("cogs")



@bot.event
async def on_ready():
    print(f"Bot has started as {bot.user}")

bot.run(os.getenv("TOKEN"))