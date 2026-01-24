from utils.transmission import transmission_request

async def remove_torrent_by_id(torrent_id, interaction):
    try:
        params = {"ids": [torrent_id], "delete-local-data": True}
        response = transmission_request("torrent-remove", params)
        if response.get("result") == "success":
            await interaction.response.send_message(f"Successfully deleted torrent with ID {torrent_id} and its associated files.", ephemeral=True)
        else:
            await interaction.response.send_message("Failed to delete the torrent and its files.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"Error: {str(e)}", ephemeral=True)
