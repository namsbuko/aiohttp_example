import jwt

from aiohttp import web

from cache import cache
from settings import JWT_SECRET_KEY


class InfoHandler:
    def __init__(self, info_getter):
        self.info_getter = info_getter

    @cache(expire=60)
    async def get_info(self, request):
        client_id = request.match_info['client_id']
        tariff_id = request.match_info['tariff_id']
        data = await self.info_getter.get(client_id, tariff_id)
        return web.json_response(data)


class JwtLogin:
    jwt_secret_key = JWT_SECRET_KEY

    async def login(self, _):
        token = jwt.encode(
            {'some_data': 'some_data'}, self.jwt_secret_key, algorithm='HS256')
        return web.json_response({'token': token.decode()})
