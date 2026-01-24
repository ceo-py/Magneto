import discord
from utils.add_torrent import add_torrent

class AddTorrentModal(discord.ui.Modal, title="Add torrent to download"):
    magnet_link = discord.ui.TextInput(
        label="Magnet Link",
        placeholder="Put magnet link url here",
    )

    def __init__(self):
        super().__init__()

    async def on_submit(self, interaction: discord.Interaction):
        await add_torrent(self.magnet_link.value, interaction)
