import pickle

import aioredis
from aiohttp.web_middlewares import middleware
from aiohttp.web_response import Response


# just for json/application content-type
class RedisCache:
    def __init__(self, redis_pool):
        self.redis_pool = redis_pool

    @staticmethod
    async def init(app):
        app.middlewares.append(cache_middleware)
        redis_pool = await aioredis.create_redis_pool(
            (app['redis_host'], app['redis_port']))
        app['cache'] = RedisCache(redis_pool)

    @staticmethod
    async def close(app):
        app['cache'].redis_pool.close()
        await app['cache'].redis_pool.wait_closed()

    async def _make_key(self, request):
        return '{method}{host}{path}{post_data}'.format(
            method=request.method,
            host=request.url.host,
            path=request.rel_url.path_qs,
            post_data=''.join(await request.post()),
        )

    async def get(self, request):
        key = await self._make_key(request)
        value = await self.redis_pool.get(key)
        return pickle.loads(value) if value else value

    async def set(self, request, response, expire):
        key = await self._make_key(request)
        data = {
            'status': response.status,
            'headers': dict(response.headers),
            'body': response.body,
        }

        await self.redis_pool.set(key, pickle.dumps(data), expire=expire)


class cache:
    def __init__(self, expire=60):
        self.expire = expire

    def __call__(self, f):
        f.cached = True
        f.expire = self.expire

        return f


@middleware
async def cache_middleware(request, handler):
    if not getattr(handler, 'cached', None):
        return await handler(request)

    redis = request.app['cache']

    cached_resp = await redis.get(request)
    if cached_resp:
        return Response(**cached_resp)

    response = await handler(request)
    expire = getattr(handler, 'expire', 60)
    await redis.set(request, response, expire)

    return response
