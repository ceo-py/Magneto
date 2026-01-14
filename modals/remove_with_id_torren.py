import discord
from utils.transmission import transmission_request

class RemoveWithIdTorrentModal(discord.ui.Modal, title="Remove torrent by ID"):
    torrent_id = discord.ui.TextInput(
        label="Torrent ID",
        placeholder="Put Torrent ID here",
    )

    def __init__(self):
        super().__init__()

    async def on_submit(self, interaction: discord.Interaction):
        torrent_id = self.torrent_id.value.strip()

        try:
            params = {"ids": [torrent_id], "delete-local-data": True} 
            response = transmission_request("torrent-remove", params)
            if response.get("result") == "success":
                await interaction.response.send_message(f"Successfully deleted torrent with ID {torrent_id} and its associated files.", ephemeral=True)
            else:
                await interaction.response.send_message("Failed to delete the torrent and its files.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Error: {str(e)}", ephemeral=True)
