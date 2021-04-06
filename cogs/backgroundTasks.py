from discord.ext import tasks
import discord

class Tasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None