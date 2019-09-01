import jwt

from aiohttp.web_exceptions import HTTPUnauthorized
from aiohttp.web_middlewares import middleware

from settings import JWT_SECRET_KEY


@middleware
async def jwt_auth(request, handler):
    def _get_token():
        raw_authorization = request.headers.get('Authorization', '')
        items = raw_authorization.split(' ')
        return items[1] if len(items) > 1 else None

    token = _get_token()
    if request.path != '/login':
        if token:
            try:
                request.jwt_data = jwt.decode(token, JWT_SECRET_KEY)
            except jwt.InvalidTokenError:
                raise HTTPUnauthorized(text='Token decode error')
        else:
            raise HTTPUnauthorized(text='Missing token')
    return await handler(request)
