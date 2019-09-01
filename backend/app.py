from aiohttp import web

from cache import RedisCache
from info import InfoGetter
from middlewares import jwt_auth
from settings import REDIS_HOST, REDIS_PORT
from views import InfoHandler, JwtLogin


async def server():
    app = web.Application(middlewares=[jwt_auth, ])

    app['redis_port'] = REDIS_PORT
    app['redis_host'] = REDIS_HOST

    app.on_startup.append(RedisCache.init)

    app.router.add_get(
        r'/{client_id:\d+}/{tariff_id:\d+}', InfoHandler(InfoGetter()).get_info)
    app.router.add_get('/login', JwtLogin().login)

    app.on_cleanup.append(InfoGetter.close)
    app.on_cleanup.append(RedisCache.close)

    return app
