import os
import discord
import dotenv
from discord.ext import commands


intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="-", intents=intents)
bot.remove_command("help")  # Custom help command


@bot.event
async def on_ready():
    for file in os.listdir("cogs"):
        if file.startswith("IGNORE_"):
            # Used to ignore non-cog python files
            # Useful for sharing content
            continue

        if file.endswith(".py"):
            await bot.load_extension(f"cogs.{file[:-3]}")
            print(f"Loaded: {file}")

    print(f"Ready. Prefix: {bot.command_prefix}")


if __name__ == "__main__":
    dotenv.load_dotenv()
    bot.run(os.environ.get("TOKEN"))
