from buttons.buttons import TorrentButtons
from commands import load_commands
import discord
from discord.ext import commands
from dotenv import dotenv_values, find_dotenv

CONFIG = dotenv_values(find_dotenv())
TOKEN = CONFIG["TOKEN"]


class PersistentViewBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()

        super().__init__(command_prefix="!", help_command=None, intents=intents)

    async def on_ready(self):
        load_commands(self)

    async def setup_hook(self) -> None:
        self.add_view(TorrentButtons())


client = PersistentViewBot()

# Event to ensure the client only listens to DMs
@client.event
async def on_message(message):
    if message.author == client.user:
        return 

    if isinstance(message.channel, discord.DMChannel):
        await client.process_commands(message)
    else:
        pass


client.run(TOKEN) 
