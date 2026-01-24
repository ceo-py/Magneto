import discord
from utils.redis import save_torrent_id_to_redis


class AddFavoriteModal(discord.ui.Modal, title="Add Series to Favorites"):
    Serial_Name = discord.ui.TextInput(
        label="Name",
        placeholder="Put name here",
    )
    imdb_id = discord.ui.TextInput(
        label="IMDB ID",
        placeholder="Put IMDB ID here",
    )

    def __init__(self):
        super().__init__()

    async def on_submit(self, interaction: discord.Interaction):
        try:
            save_torrent_id_to_redis(
                self.Serial_Name.value.strip(), self.imdb_id.value.strip())
            await interaction.response.send_message("Successfully added torrent to favorites.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Try again later!", ephemeral=True)
