

from buttons.buttons import TorrentButtons
from embeds.embeds import embed_for_torrents
from discord.ext import commands


@commands.command()
async def menu(ctx):
    embed = embed_for_torrents()
    await ctx.send(embed=embed, view=TorrentButtons())

def setup(bot):
    bot.add_command(menu)