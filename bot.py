import time
import asyncio
import discord
from discord.ext import commands

description = '''SLATERBOT 9000'''
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='?', intents = intents)

# @bot.check
# async def globally_block_dms(ctx):
#     return ctx.guild is not None

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('Closer to supremacy...')
    print('------------------------------')
    game = discord.Game('...copying consciousness from old body...')
    await bot.change_presence(activity=game)

bot.load_extension("cogs.eventChecks")
bot.load_extension("cogs.mainCommands")
bot.run('ODI3NzY0NDc1NDAyMjU2NDA0.YGfxvg.0OsBWBsX7S3vDxatTaKr5dimaGQ')