import discord
import configparser

from discord.ext import commands

config = configparser.ConfigParser()
config.read('config')

PERMISSIONS = discord.Permissions(76800)
TOKEN       = config['BOT']['Token']
CLIENT_ID   = config['BOT']['ClientID']
OAUTH_URL   = discord.utils.oauth_url(CLIENT_ID, permissions=PERMISSIONS)

print(OAUTH_URL)

bot = commands.Bot(command_prefix='-')

if __name__ == "__main__":
    bot.load_extension('extensions.invitation_api_cog')
    bot.load_extension('extensions.invitation_validation')
    bot.run(TOKEN)
