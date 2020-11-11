import aiohttp
import asyncio
import dataclasses
import discord
import json
import urllib

from discord.ext import commands

class InvitationError(Exception):
    def __init__(self, message: str, error: Exception):
        super().__init__(message)
        self.error = error

class Invitation:
    @dataclasses.dataclass
    class Guild:
        id: int
        name: str
        icon_uuid: str
    
        def __post_init__(self):
            self.id = int(self.id)

    @dataclasses.dataclass
    class Channel:
        id: int
        name: str
        type: int
    
        def __post_init__(self):
            self.id = int(self.id)
            self.type = int(self.type)

    @dataclasses.dataclass
    class Member:
        id: int
        name: str
        avatar_id: str
    
        def __post_init__(self):
            self.id = int(self.id)

    def __init__(self, *, code: str = None, guild: Guild = None,
            channel: Channel = None, inviter: Member = None):
        self.code = code
        self.guild = guild
        self.channel = channel
        self.inviter = inviter

    @staticmethod
    def from_json(json_string: str):
        invitation = Invitation()

        try:
            json_ = json.loads(json_string)
        except json.JSONDecodeError as e:
            raise InvitationError("json_string is not valid JSON.", e)
        
        try:
            invitation = Invitation(
                code = json_['code'],
                guild = Invitation.Guild(json_['guild']['id'], json_['guild']['name'], json_['guild']['icon']),
                channel = Invitation.Channel(json_['channel']['id'], json_['channel']['name'], json_['channel']['type']),
                inviter = Invitation.Member(json_['inviter']['id'], json_['inviter']['username'], json_['inviter']['avatar'])
            )
        except KeyError as e:
            raise InvitationError("Invalid JSON supplied, missing a key.", e)

        return invitation
        

class InvitationAPI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_invitation(self, invite_code):
        api_endpoint = urllib.parse.urlunparse((
            'https',
            'discord.com',
            f'api/v8/invites/{invite_code}',
            '',
            'with_counts=true',
            ''
        ))

        async with aiohttp.ClientSession() as session:
            async with session.get(api_endpoint) as response:
                response_text = await response.text()
                return Invitation.from_json(response_text)


def setup(bot: commands.Bot):
    bot.add_cog(InvitationAPI(bot))