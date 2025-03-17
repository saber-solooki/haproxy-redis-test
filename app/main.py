import asyncio
import logging
from datetime import datetime

from connections import init_redis_pool, get_sentinel, get_redis
from config import RedisSettings


async def who_is_master():
    settings = RedisSettings()

    await init_redis_pool(settings)
    sentinel_redis = get_sentinel(settings)
    result = await sentinel_redis.discover_master(settings.sentinel_service_name)
    print(result)


async def main():
    settings = RedisSettings()
    settings.redis_host = 'haproxy'
    settings.redis_port = 8080

    while True:
        redis = await get_redis(settings=settings)
        try:
            print(f'{len(redis.connection_pool._available_connections)}, {id(asyncio.current_task())}')
            await redis.set('saber', 1)
            value = await redis.get('saber')
            print(f'value from redis {value} {datetime.now()}')
            await asyncio.sleep(1)
        except Exception as e:
            print(e)


async def run_concurrently():
    tasks = []
    for _ in range(10):
        tasks.append(asyncio.create_task(main()))
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(run_concurrently())
    # asyncio.run(main())
    # asyncio.run(who_is_master())
