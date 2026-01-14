import discord
def embed_for_torrents():
    embed = discord.Embed(
        title="Torrent Management Menu",
        description="Use the buttons below to manage your torrents:",
        colour=discord.Colour.gold(),
    )
    embed.set_thumbnail(url="https://cdn.discordapp.com/app-icons/1155086366833655819/fa6f4840dc4f088f69ce7e43b3968273.png?size=512&quot")
    
    return embed