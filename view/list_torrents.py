import discord
from discord.ui import View, Select
from utils.add_torrent import add_torrent
from abc import ABC, abstractmethod


class ListTorrentsBase(View, ABC):
    def __init__(self, torrents):
        super().__init__()
        self.torrents = torrents[:25]
        self.placeholder = "Select a torrent to download"
        select = Select(
            placeholder=self.placeholder,
            options=[discord.SelectOption(
                label=f'S[{torrent["seeds"]}] {torrent["title"]}'[:100], value=str(pos)) for pos, torrent in enumerate(self.torrents)]
        )
        select.callback = self.select_callback
        self.add_item(select)

    @abstractmethod
    async def select_callback(self, interaction):
        pass


class DownloadFavoriteTorrent(ListTorrentsBase):
    def __init__(self, torrents):
        super().__init__(torrents)

    async def select_callback(self, interaction):
        selected_option = interaction.data['values'][0]
        magnet_url = self.torrents[int(selected_option)]["magnet_url"]
        await add_torrent(magnet_url, interaction)

