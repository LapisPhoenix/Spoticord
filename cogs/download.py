import os
import re
import subprocess
import discord
import asyncio
from discord.ext import commands

class Download(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.user_locks = {}

    def get_user_lock(self, user_id):
        if user_id not in self.user_locks:
            self.user_locks[user_id] = asyncio.Lock()
        return self.user_locks[user_id]

    def dwn(self, url, cwd):
        command = ["spotdl", "download", url, "--lyrics", "genius"]
        process = subprocess.run(command, stdout=subprocess.PIPE, cwd=cwd)
        return process.stdout

    def find_file(self, song_name, artist_name, directory):
        files = os.listdir(directory)
        for file in files:
            if song_name.lower() in file.lower() and artist_name.lower() in file.lower():
                return file
        return None

    @commands.command()
    async def download(self, ctx, url):
        if "album" in url:
            await ctx.send("Sorry, downloading albums is not allowed.")
            return

        await ctx.send("Downloading, please be patient...")

        cwd = "./songs"
        user_id = ctx.author.id

        async with self.get_user_lock(user_id):
            await self._download_and_upload(ctx, url, cwd)

    async def _download_and_upload(self, ctx, url, cwd):
        output = self.dwn(url, cwd)
        output = str(output, 'utf-8')
        pattern = r'"(.*?)"'
        match = re.findall(pattern, output)

        song = match[0].split('-')
        song_name = song[1].strip()
        artist_name = song[0].strip()

        found_file = self.find_file(song_name, artist_name, cwd)

        if found_file:
            print(f"Serving {found_file} for {ctx.author.name}")
            song_path = os.path.join(cwd, found_file)
            with open(song_path, 'rb') as f:
                fl = discord.File(fp=f, filename=f"{song_name}.mp3")
                await ctx.send(f"{ctx.author.mention} Downloaded {song_name}!", file=fl)

            os.remove(song_path)
        else:
            print(f"File not found for {song_name} by {artist_name}")
            await ctx.send("An Unknown Error Occurred!")

async def setup(bot):
    await bot.add_cog(Download(bot))