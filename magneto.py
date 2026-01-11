import discord
import requests
from discord.ext import commands
from dotenv import dotenv_values, find_dotenv

CONFIG = dotenv_values(find_dotenv())

# Set up the bot and prefix for commands
bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())

# Transmission RPC settings
TRANSMISSION_RPC_URL = CONFIG["RPC_URL"]  # URL to Transmission RPC (update if necessary)
TRANSMISSION_RPC_USER = CONFIG["RPC_USERNAME"]  # Your Transmission RPC username
TRANSMISSION_RPC_PASS = CONFIG["RPC_PASSWORD"]  # Your Transmission RPC password
TOKEN = CONFIG["TOKEN"]
NOT_DM_MESSAGE = "Sorry, I can only process commands through Direct Messages (DMs)."

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


def transmission_request(method, params=None):
    headers = {
        'X-Transmission-Session-Id': ''
    }

    data = {
        "method": method,
        "arguments": params if params else {}
    }

    with requests.Session() as session:
        response = session.post(TRANSMISSION_RPC_URL, json=data, headers=headers, auth=(TRANSMISSION_RPC_USER, TRANSMISSION_RPC_PASS))

        if response.status_code == 409:
            headers['X-Transmission-Session-Id'] = response.headers['X-Transmission-Session-Id']
            response = session.post(TRANSMISSION_RPC_URL, json=data, headers=headers, auth=(TRANSMISSION_RPC_USER, TRANSMISSION_RPC_PASS))

        return response.json()

# Command to add a magnet link
@bot.command()
async def add(ctx, magnet_url: str):
    try:
        params = {"filename": magnet_url}
        response = transmission_request("torrent-add", params)
        if response.get("result") == "success":
            await ctx.send(f"Successfully added torrent")
        else:
            await ctx.send("Failed to add torrent.")
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")


# Command to list all torrents
@bot.command()
async def list(ctx):
    try:
        response = transmission_request("torrent-get", {"fields": ["id", "name", "status"]})
        torrents = response.get("arguments", {}).get("torrents", [])
        if torrents:
            torrent_list = "\n".join([f"{torrent['id']}: {torrent['name']} (Status: {status_map[torrent['status']]})" for torrent in torrents])
            await ctx.send(f"Active torrents:\n{torrent_list}")
        else:
            await ctx.send("No active torrents.")
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")


# Command to delete a specific torrent
@bot.command()
async def delete(ctx, torrent_id: int):
    try:
        params = {"ids": [torrent_id], "delete-local-data": True} 
        response = transmission_request("torrent-remove", params)
        if response.get("result") == "success":
            await ctx.send(f"Successfully deleted torrent with ID {torrent_id} and its associated files.")
        else:
            await ctx.send("Failed to delete the torrent and its files.")
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")


# Command to delete all torrents
@bot.command()
async def delete_all(ctx):
    try:
        response = transmission_request("torrent-get", {"fields": ["id"]})
        torrents = response.get("arguments", {}).get("torrents", [])
        if torrents:
            torrent_ids = [torrent['id'] for torrent in torrents]
            params = {"ids": torrent_ids, "delete-local-data": True}  # Add delete-local-data=True
            response = transmission_request("torrent-remove", params)
            if response.get("result") == "success":
                await ctx.send("Successfully deleted all torrents and their associated files.")
            else:
                await ctx.send("Failed to delete torrents and their files.")
        else:
            await ctx.send("No torrents to delete.")
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")



# Event to ensure the bot only listens to DMs
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return 

    if isinstance(message.channel, discord.DMChannel):
        await bot.process_commands(message)
    else:
        pass


bot.run(TOKEN) 
