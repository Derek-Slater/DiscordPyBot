import discord
from discord.ext import commands
import random
import eliza.eliza
import os
from memeMaker import downloadImgFromURL, addTextToImage

GenericError = "*Either something went wrong, or the command was inputted incorrectly, see below for more info, or type ?help <command> for help on other commands:*\n"
ELIZA = eliza.eliza.Eliza()
class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(aliases=['mimic'])
    async def echo(self, ctx, *, phrase):
        '''Sends the inputted message\nExample: \n?echo some text'''
        await ctx.send(phrase)
    @echo.error
    async def echo_error(self, ctx, error):
        await ctx.send(GenericError + '`Sends the inputted message\nExample: \n?echo some text`')

    @commands.command(aliases=['speak', 'send']) #ADD AN OPTIONAL CHANNEL TO SEND IN
    async def say(self, ctx, *, phrase):
        '''Lets the bot message for you\nExample: \n?say say this for me please'''
        channel = ctx.channel
        await ctx.channel.purge(limit=1)
        await ctx.send(phrase)
    @say.error
    async def say_error(self, ctx, error):
        await ctx.send(GenericError + '`Lets the bot message for you\nExample: \n?say say this for me please`')

    @commands.command(aliases=['clean', 'massdelete'])
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx, count: int):
        '''Purges an inputted number of messages.\nExample: \n?purge 5'''
        await ctx.channel.purge(limit=1)
        removed = await ctx.channel.purge(limit=count)
        timeout = 5.0
        
        if len(removed) == 0:
            await ctx.send('???')
            return
        if len(removed) == 1:
            msg = await ctx.send('Deleted 1 message', delete_after=timeout)
        else:
            if len(removed) > 50:
                msg = await ctx.send('Deleted {} messages'.format(len(removed)) + '...help?', delete_after=timeout)
            else:
                msg = await ctx.send('Deleted {} messages'.format(len(removed)), delete_after=timeout)
    @purge.error
    async def purge_error(self, ctx, error):
        await ctx.send(GenericError + '`Purges an inputted number of messages.\nExample: \n?purge 5`')

    @commands.command(aliases=['dice', 'diceroll'])
    async def roll(self, ctx, dice: str):
        """Rolls a dice in NdN format.\nExample: \n?roll 1d6"""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.send(GenericError + '`' + roll.help + '`')
            return

        numbers = list(random.randint(1, limit) for r in range(rolls))
        await ctx.send(str(numbers) + "\nTotal: " + str(sum(numbers)))

    @commands.command(description='For when you can\'t choose...', aliases=['pick'])
    async def choose(self, ctx, *choices: str):
        """Chooses between multiple choices.\nExamples: \n?choose red blue green\n?choose "Go to Sleep" "Don\'t go to sleep\""""
        await ctx.send(random.choice(choices))
    @choose.error
    async def choose_error(self, ctx, error):
        await ctx.send(GenericError + '`Chooses between multiple choices.\nExamples: \n?choose red green blue\n?choose "Go to Sleep" "Don\'t go to sleep"`')

    @commands.command(aliases=['spam'])
    async def repeat(self, ctx, times: int, *, content='Spam'):
        """Repeats a message the inputted number of times.\nExample: \n?repeat 5 spam"""
        for i in range(times):
            await ctx.send(content)
    @repeat.error
    async def repeat_error(self, ctx, error):
        await ctx.send(GenericError + '`Repeats a message the inputted number of times.\nExample: \n?repeat 5 spam`')

    @commands.command(aliases=['user', 'profile', 'member'])
    async def userinfo(self, ctx, user: discord.Member):
        '''Provides the user's id, name, and profile picture\nExample: \n?userinfo @KooshieBooshie6660'''
        embed = discord.Embed()
        embed.set_image(url=user.avatar_url)
        embed.set_author(name="{} - {}".format(user.name, user.id), icon_url=user.avatar_url)
        embed.set_footer(text="Requested by: {}".format(ctx.author.name))
        embed.add_field(name="Joined at", value=user.joined_at)
        
        await ctx.send('User found:', embed = embed)
    @userinfo.error
    async def userinfo_error(self, ctx, error):
        await ctx.send(GenericError + '`Provides the user\'s id, name, and profile picture\nExample: \n?userinfo @KooshieBooshie6660`')

    @commands.command(aliases=['joindate'])
    async def joined(self, ctx, *, member: discord.Member):
        """Gives when a member joined the server last.\nExample: ?joined @KooshieBooshie6660"""
        await ctx.send('{0.name} joined in {0.joined_at}'.format(member))
    @joined.error
    async def joined_error(self, ctx, error):
        # if isinstance(error, commands.BadArgument):
        await ctx.send(GenericError + '`Gives when a member joined the server last.\nExample: \n?joined @KooshieBooshie6660`')

    @commands.command(aliases=['talk'])
    async def chat(self, ctx, *, text):
        """Chat to the bot\nExample: ?talk How are you?"""
        await ctx.send(ELIZA.respond(text))
    @joined.error
    async def joined_error(self, ctx, error):
        # if isinstance(error, commands.BadArgument):
        await ctx.send(GenericError + '`Chat to the bot\nExample: ?talk How are you?`')

    @commands.command()
    async def makememe(self, ctx, *, text=None):
        '''Makes a meme by applying text on either a provided link or attachment\nExample: \n?makeMeme <link> Meme Text Meme Text'''
        imageURL = ""
        try: #link provided
            if text != "":
                text = text.split()
                imageURL = text[0]
        except:
            makeMeme_error()
            return
        try: #image present
            if ctx.message.attachments[0].url is not None:
                imageURL = ctx.message.attachments[0].url
        except: #if image not present, don't include link in the text that'll be added
            text = text[1:]
        
        if len(text) < 1:
            makeMeme_error()
            return
        if imageURL == "":
            makeMeme_error()
            return

        imageName = downloadImgFromURL(imageURL)
        if imageName is not None:
            meme, duration = addTextToImage(imageName, ' '.join(text))
            if meme is not None:
                if len(meme) == 1:
                    meme[0].save(imageName, lossless=True)
                else:
                    meme[0].save(imageName, save_all=True, append_images=meme[1:], loop=0, duration=duration)
            else:
                await ctx.send("Provided link or file needs to be a valid image")
                if os.path.exists(imageName):
                    os.remove(imageName)
                return
        else:
            makeMeme_error()
            if os.path.exists(imageName):
                os.remove(imageName)
            return

        f = open(imageName, "rb")
        fileToSend = discord.File(f)
        await ctx.message.delete()
        await ctx.send("Courtesy of " + ctx.message.author.mention, file=fileToSend)
        # # Afterwards, delete its local copy (whether it was actually an image or not)
        f.close()
        if os.path.exists(imageName):
            os.remove(imageName)
    # @makememe.error
    # async def makeMeme_error(self, ctx, error):
    #     await ctx.send(GenericError + '`Makes a meme by applying text on either a provided link or attachment\nExample: \n?makeMeme <link> Meme Text Meme Text`')

def setup(bot):
    bot.add_cog(General(bot))