import discord
from utils.remove_torrent_by_id import remove_torrent_by_id

class RemoveWithIdTorrentModal(discord.ui.Modal, title="Remove torrent by ID"):
    torrent_id = discord.ui.TextInput(
        label="Torrent ID",
        placeholder="Put Torrent ID here",
    )

    def __init__(self):
        super().__init__()

    async def on_submit(self, interaction: discord.Interaction):
        torrent_id = self.torrent_id.value.strip()
        await remove_torrent_by_id(torrent_id, interaction)
