import json

from app.core.redis_client import (
    redis_client,
)


def get_cache(key: str):

    data = redis_client.get(key)

    if data:

        print(f"REDIS HIT: {key}")

        return json.loads(data)

    print(f"REDIS MISS: {key}")

    return None


def set_cache(
    key: str,
    value,
    ttl: int = 30,
):

    print(f"REDIS SET: {key}")

    redis_client.setex(
        key,
        ttl,
        json.dumps(value),
    )


def delete_cache(key: str):

    print(f"REDIS DELETE: {key}")

    redis_client.delete(key)
