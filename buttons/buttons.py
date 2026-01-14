import discord
from modals.add_modals import AddTorrentModal
from modals.remove_with_id_torren import RemoveWithIdTorrentModal
from utils.transmission import transmission_request

status_map = {
    0: "Queued",         # Torrent is queued for download
    1: "Downloading",    # Torrent is actively downloading
    2: "Seeding",        # Torrent has finished downloading and is uploading
    3: "Paused",         # Torrent is paused
    4: "Stalled",        # Torrent is stalled (actively downloading but no progress)
    5: "Error",          # Torrent encountered an error
    6: "Finished",       # Torrent has finished downloading
    7: "Stopping"        # Torrent is stopping (being paused or removed)
}


class TorrentButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="List",
        style=discord.ButtonStyle.primary,
        custom_id="1",
        emoji="<:list:1461116766146269254>",
    )
    async def list(self, button: discord.ui.Button, interaction: discord.Interaction):
        try:
            response = transmission_request(
                "torrent-get", {"fields": ["id", "name", "status"]})
            torrents = response.get("arguments", {}).get("torrents", [])
            if torrents:
                torrent_list = "\n".join(
                    [f"{torrent['id']}: {torrent['name']} (Status: {status_map[torrent['status']]})" for torrent in torrents])
                await button.response.send_message(torrent_list, ephemeral=True)
            else:
                await button.response.send_message("No active torrents.", ephemeral=True)
        except Exception as e:
            await button.response.send_message(f"Error: {str(e)}", ephemeral=True)

    @discord.ui.button(
        label="Add",
        style=discord.ButtonStyle.green,
        custom_id="2",
        emoji="<:add:1461116744398540863>",
    )
    async def add(self, button: discord.ui.Button, interaction: discord.Interaction):
        await button.response.send_modal(AddTorrentModal())

    @discord.ui.button(
        label="Remove with ID",
        style=discord.ButtonStyle.red,
        custom_id="3",
        emoji="<:remove_by_id:1461116729210966248>",
    )
    async def remove_with_id(self, button: discord.ui.Button, interaction: discord.Interaction):
        await button.response.send_modal(RemoveWithIdTorrentModal())

    @discord.ui.button(
        label="Remove ALL",
        style=discord.ButtonStyle.red,
        custom_id="4",
        emoji="<:remove_all:1461116701650321438>",
    )
    async def remove_all(self, button: discord.ui.Button, interaction: discord.Interaction):
        try:
            response = transmission_request("torrent-get", {"fields": ["id"]})
            torrents = response.get("arguments", {}).get("torrents", [])
            if torrents:
                torrent_ids = [torrent['id'] for torrent in torrents]
                params = {"ids": torrent_ids, "delete-local-data": True}
                response = transmission_request("torrent-remove", params)
                if response.get("result") == "success":
                    await button.response.send_message("Successfully deleted all torrents and their associated files.", ephemeral=True)
                else:
                    await button.response.send_message("Failed to delete torrents and their files.", ephemeral=True)
            else:
                await button.response.send_message("No torrents to delete.", ephemeral=True)
        except Exception as e:
            await button.response.send_message(f"Error: {str(e)}", ephemeral=True)
