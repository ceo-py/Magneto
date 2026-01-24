import discord
from discord.ui import View, Select
from view.list_torrents import DownloadFavoriteTorrent
from utils.api_eztvx import get_serials_eztvx
from utils.redis import remove_torrent_id_from_redis
from abc import ABC, abstractmethod


class FavoritesBase(View, ABC):
    def __init__(self, torrents):
        super().__init__()
        self.torrents = torrents
        self.placeholder = "Select a torrent to view latest episodes"
        select = Select(
            placeholder=self.placeholder,
            options=[discord.SelectOption(
                label=torrent_name, value=str(torrent_id)) for torrent_id, torrent_name in self.torrents.items()]
        )
        select.callback = self.select_callback
        self.add_item(select)

    @abstractmethod
    async def select_callback(self, interaction):
        pass


class ListFavorites(FavoritesBase):
    def __init__(self, torrents):
        super().__init__(torrents)

    async def select_callback(self, interaction):
        selected_torrent_id = interaction.data['values'][0]
        torrents = get_serials_eztvx(selected_torrent_id)

        if not torrents:
            await interaction.response.send_message(f"No torrents found.", ephemeral=True)
            return

        await interaction.response.send_message(view=DownloadFavoriteTorrent(torrents), ephemeral=True)


class RemoveFavorites(FavoritesBase):
    def __init__(self, torrents):
        super().__init__(torrents)

    async def select_callback(self, interaction):
        try:
            selected_torrent_id_to_remove = interaction.data['values'][0]
            remove_torrent_id_from_redis(selected_torrent_id_to_remove)
            await interaction.response.send_message(f"Successfully removed torrent from favorites.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Try again later!", ephemeral=True)