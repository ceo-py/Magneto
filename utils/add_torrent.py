from utils.transmission import transmission_request


async def add_torrent(magnet_link: str, interaction) -> dict:
        try:
            params = {"filename": magnet_link}
            response = transmission_request("torrent-add", params)

            if response.get("result") == "success":
                await interaction.response.send_message("Successfully added torrent", ephemeral=True)
            else:
                await interaction.response.send_message("Failed to add torrent.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Error: {str(e)}", ephemeral=True)
