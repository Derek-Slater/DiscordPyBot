import discord
from discord.ext import commands
LOG_CHANNEL = 828120665135251462
OWNER_ID = 395782336626556928

class eventChecks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        on_message_edit = False
        debug_on_message_edit = True
        edit_channel = before.channel
        log = before.channel
        person = before.author
        if debug_on_message_edit == False or before.author.id == OWNER_ID:
            return
        if before.content == after.content:
            return
        else:
            if on_message_edit == True: #for sending it in the same channel as the sent message
                await log.send('%s has dun messed up:' % str(before.author.mention))
                await log.send("**Before correction: **" + before.content)
                await log.send("**After correction: **" + after.content)
            else:
                log = self.bot.get_channel(LOG_CHANNEL) #bot-logs channel
                await log.send('**%s has dun messed up in %s:**\nBefore correction: %s\nAfter correction: %s' % ( str(before.author), str(edit_channel.mention), str(before.content), str(after.content) ) )

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        person = message.author
        if person.bot or person.id == OWNER_ID:
            return
        log = self.bot.get_channel(LOG_CHANNEL) #bot-logs channel
        if len(message.attachments) > 0:
            await log.send('**%s has deleted their message in %s:**\nMessage: %s\nAttachment: %s' % ( str(message.author), str(message.channel.mention), str(message.content), str(message.attachments[0].url) ) )
        else:
            await log.send('**%s has deleted their message in %s:**\nMessage: %s' % ( str(message.author), str(message.channel.mention), str(message.content) ) )

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        if payload.cached_message == None:
            chnl = await self.bot.fetch_channel(payload.channel_id)
            log = self.bot.get_channel(LOG_CHANNEL)
            await log.send("Older message deleted in: %s" %(chnl.mention))

def setup(bot):
    bot.add_cog(eventChecks(bot))