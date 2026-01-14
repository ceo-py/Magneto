# Magneto Discord Torrent Bot

Magneto is a Discord bot designed to allow users to manage torrents via **Transmission RPC** directly from Discord. The bot provides an intuitive interface using buttons, allowing users to add torrents, list active torrents, and remove specific torrents or all torrents. Users can interact with the bot using **modals** for commands that require additional parameters (such as adding a magnet link or removing a torrent by ID).

## Features

* **Add Torrent**: Add a torrent by providing a magnet link via a modal.
* **List Torrents**: List all active torrents with their statuses, accessible through a button.
* **Delete Torrent**: Remove a specific torrent by its ID through a modal.
* **Delete All Torrents**: Remove all active torrents and their local data using a button.
* **DM Only**: The bot processes commands exclusively through Direct Messages (DMs) to avoid misuse in public channels.
* **Interactive Buttons & Modals**: All actions are performed using buttons, with modals used for actions requiring parameters (such as adding a torrent or removing a specific one by ID).

## Requirements

* Python 3.8+
* Discord API Token
* Transmission (Docker container or local instance)
* `.env` file with necessary credentials for Transmission and the bot.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/ceo-py/Magneto
cd magneto
```

### 2. Set up the virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file

Create a `.env` file in the root directory and add your configuration values:

```bash
RPC_URL=https://your-transmission-url:9091/transmission/rpc
RPC_USERNAME=your_rpc_username
RPC_PASSWORD=your_rpc_password
TOKEN=your_discord_token
```

### 5. Running the Bot

To start the bot, use the following command:

```bash
python3 magneto.py
```

You can also run it as a service using systemd or in a Docker container (see below).

## Docker Setup

You can run the bot alongside Transmission in Docker by using the provided `docker-compose.yml` configuration.

### 1. Docker Compose

To start both Transmission and the Magneto bot in Docker, use:

```bash
docker-compose up -d
```

This will start both the **Transmission** container and the **Magneto** bot.

### 2. Docker Configuration

The bot will connect to the Transmission service by using the settings defined in the `docker-compose.yml` file. Here’s a sample configuration:

```yaml
version: "3.8"

services:
  transmission:
    image: lscr.io/linuxserver/transmission
    container_name: transmission
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=UTC
      - TRANSMISSION_RPC_ENABLED=true
      - TRANSMISSION_RPC_BIND_ADDRESS=0.0.0.0
      - TRANSMISSION_RPC_PORT=9091
      - TRANSMISSION_RPC_USERNAME=username
      - TRANSMISSION_RPC_PASSWORD=password
    volumes:
      - /home/your_username/transmission/config:/config
      - /home/your_username/jellyfin-docker/media:/downloads
    ports:
      - "51413:51413"  # Main torrent port
      - "51413:51413/udp"
      - "9091:9091"  # Expose RPC port for API
    restart: unless-stopped
```

### 3. Systemd Service

You can also set up a systemd service to run the bot as a background service.

```ini
[Unit]
Description=Magneto Discord Torrent Bot
After=network.target

[Service]
User=user you want to run it from
WorkingDirectory=/path/to/your/script
ExecStart=/home/venv/bin/python3 /home/magneto.py 
Restart=always
RestartSec=3
Environment="PATH=/venv/bin"

[Install]
WantedBy=multi-user.target
```

Place the above configuration in `/etc/systemd/system/magneto.service`, then enable and start the service:

```bash
sudo systemctl enable magneto
sudo systemctl start magneto
```

## Commands

**All interactions now use buttons for managing torrents. Modals are used for actions that require additional parameters (e.g., adding or removing torrents by ID).**

### Button Commands:

1. **Add Torrent**

   * **Action**: Open a modal to add a torrent by providing a magnet link.
   * **Button**: "Add Torrent"
   * **Modal**: Users enter the magnet link to add a torrent.

2. **List Torrents**

   * **Action**: Lists all active torrents and their statuses in a message.
   * **Button**: "List Torrents"

3. **Delete Torrent**

   * **Action**: Open a modal to remove a specific torrent by ID.
   * **Button**: "Remove Torrent by ID"
   * **Modal**: Users provide the torrent ID to remove a specific torrent.

4. **Delete All Torrents**

   * **Action**: Delete all active torrents and their local data.
   * **Button**: "Delete All Torrents"

## Notes

* **Direct Message Only**: All bot interactions happen in **Direct Messages**. The bot does not respond to commands in public channels.
* **Transmission RPC**: Make sure your **Transmission instance** is properly configured and accessible via the RPC URL.
* **Additional Features**: You can extend the bot with more functionality, such as monitoring active torrents, adding more buttons, or integrating other torrent clients.

## License

This project is licensed under the MIT License - see the Apache-2.0 license file for details.

---

