import discord
import extensions.invitation_api_cog as inv_api_cog # pylint: disable=import-error
import re

from discord.ext import commands

DISCORD_INVITE_CODE_REGEX = re.compile(r'discord.gg/(\w*)')

bot: commands.Bot

async def on_message(message: discord.Message):
    if message.author == bot.user:
        pass

    match = DISCORD_INVITE_CODE_REGEX.search(message.content)
    if match:
        invite_code = match.group(1)
        invitation_api: inv_api_cog.InvitationAPI = bot.get_cog(inv_api_cog.InvitationAPI.__name__)

        invitation = await invitation_api.get_invitation(invite_code)
        if invitation:
            if invitation.guild.id != message.channel.guild.id:
                await message.delete()
                await message.author.send("Posting invitations that are outside this server is not allowed.")


def setup(bot_: commands.Bot):
    global bot

    bot = bot_
    bot.add_listener(on_message)