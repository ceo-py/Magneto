import redis
from dotenv import dotenv_values, find_dotenv


CONFIG = dotenv_values(find_dotenv())
REDIS_HOST = str(CONFIG.get("REDIS_HOST"))
REDIS_PORT = int(CONFIG.get("REDIS_PORT"))

redis_client = redis.StrictRedis(
    host=REDIS_HOST, port=REDIS_PORT, db=1, decode_responses=True)


def save_torrent_id_to_redis(torrent_name: str, torrent_id: str) -> None:
    """Save the torrent ID to Redis with a value based on the torrent name."""
    redis_client.set(torrent_id, torrent_name)


def remove_torrent_id_from_redis(torrent_id: str) -> str:
    """Retrieve the torrent ID from Redis for the given torrent."""
    torrent_value = redis_client.get(str(torrent_id))
    if torrent_value:
        redis_client.delete(torrent_id)


def list_all_torrents_from_redis():
    """Retrieve all torrents from Redis."""

    keys = list(redis_client.scan_iter("*"))
    if not keys:
        return {}

    pipe = redis_client.pipeline()
    for key in keys:
        pipe.get(key)
    values = pipe.execute()

    return dict(zip(keys, values))