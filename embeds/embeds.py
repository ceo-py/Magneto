import discord


def embed_for_torrents():
    embed = discord.Embed(
        title="🛰️ Torrent Management Station",
        description=(
            "Use the buttons below to manage your downloads and favorite shows.\n\n"
            "**General Operations**\n"
            "• `List`: View all active/completed downloads.\n"
            "• `Add Magnet`: Paste a link to start a new download.\n\n"
            "**Favorite Shows (Redis Sync)**\n"
            "• `View Favorites`: Check your top 25 shows for new episodes.\n"
            "• `Add Favorite`: Save a show with its Name and IMDB ID.\n"
            "• `Remove Favorite`: Delete a show from your quick-access list.\n\n"
            "**Maintenance**\n"
            "• `Remove with ID`: Delete one specific torrent.\n"
            "• `Remove ALL`: Clear the entire download queue and local data."
        ),
        colour=discord.Colour.gold(),
    )
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/app-icons/1155086366833655819/fa6f4840dc4f088f69ce7e43b3968273.png?size=512&quot")

    return embed
