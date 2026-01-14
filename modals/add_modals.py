import discord
from utils.transmission import transmission_request

class AddTorrentModal(discord.ui.Modal, title="Add torrent to download"):
    magnet_link = discord.ui.TextInput(
        label="Magnet Link",
        placeholder="Put magnet link url here",
    )

    def __init__(self):
        super().__init__()

    async def on_submit(self, interaction: discord.Interaction):
        try:
            magnet_link = self.magnet_link.value.strip()
            params = {"filename": magnet_link}
            response = transmission_request("torrent-add", params)

            if response.get("result") == "success":
                await interaction.response.send_message("Successfully added torrent", ephemeral=True)
            else:
                await interaction.response.send_message("Failed to add torrent.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Error: {str(e)}", ephemeral=True)
