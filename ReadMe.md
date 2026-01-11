# Magneto Discord Torrent Bot

Magneto is a Discord bot that allows users to manage torrents via Transmission RPC directly from Discord. Users can add torrents, list active torrents, delete specific torrents, or delete all torrents through simple commands in Direct Messages (DMs).

## Features
- **Add Torrent**: Add a torrent by providing a magnet link.
- **List Torrents**: List all active torrents with their statuses.
- **Delete Torrent**: Delete a specific torrent by its ID, including the associated local data.
- **Delete All Torrents**: Delete all active torrents and their local data.
- **DM Only**: The bot can only process commands through Direct Messages (DMs) to prevent misuse in public channels.

## Requirements
- Python 3.8+
- Discord API Token
- Transmission (Docker container or local instance)
- `.env` file with necessary credentials for Transmission and the bot.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/magneto.git
cd magneto
````

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

* **`!add <magnet_link>`**: Adds a torrent from the provided magnet link.
* **`!list`**: Lists all active torrents and their statuses.
* **`!delete <torrent_id>`**: Deletes the torrent with the specified ID.
* **`!delete_all`**: Deletes all active torrents and their data.

### Example Usage

1. **Adding a torrent**:

   ```plaintext
   !add magnet:?xt=urn:btih:yourmagnetlinkhere
   ```
2. **Listing torrents**:

   ```plaintext
   !list
   ```
3. **Deleting a torrent**:

   ```plaintext
   !delete 123
   ```
4. **Deleting all torrents**:

   ```plaintext
   !delete_all
   ```

## Notes

* The bot **only works in DMs**. It will not process commands in public channels.
* Make sure your Transmission instance is configured correctly and accessible via the RPC URL.
* You can add additional functionality, such as monitoring the bot's activity or adding more commands, as needed.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```

---

### Key Sections:
1. **Project Description and Features**: Overview of the bot’s functionality.
2. **Requirements**: Prerequisites for running the bot.
3. **Setup Instructions**: Step-by-step guide to set up the bot, including creating the `.env` file, installing dependencies, and running the bot.
4. **Docker Setup**: Instructions to run both Transmission and the bot using Docker.
5. **Systemd Service**: Configuration for running the bot as a service.
6. **Commands**: The available bot commands and their usage.
7. **Example Usage**: Examples for interacting with the bot.
8. **License**: MIT License as an example, you can modify this according to your choice.

### Next Steps:
- Create the GitHub repository for this project and push the files.
- Update the repository’s URL and make sure to keep your `.env` and sensitive information out of public repositories.

Let me know if you'd like further modifications or additional features in the README!

