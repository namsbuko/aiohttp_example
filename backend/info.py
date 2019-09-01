import asyncio

from aiohttp import ClientSession

from settings import API_URL


class InfoGetter:
    api_url = API_URL
    session = ClientSession()

    @staticmethod
    async def close(_):
        await InfoGetter.session.close()

    async def _request(self, url, headers=None):
        request_url = self.api_url + url
        headers = headers or {'content-type': 'json/application'}
        async with self.session.get(request_url, headers=headers) as resp:
            return await resp.json()

    async def get(self, client_id, tariff_id):
        client_info_task = \
            asyncio.ensure_future(self._request('clients/' + str(client_id)))
        tariff_info_task = \
            asyncio.ensure_future(self._request('tariffs/' + str(tariff_id)))

        await asyncio.gather(client_info_task, tariff_info_task)
        client_info = client_info_task.result()
        tariff_info = tariff_info_task.result()

        # здесь нужны сериалайзеры
        return {
            'id': client_info.get('id', 0),  # из описания не ясно,
                                             # что должен значить этот параметр
            'success': True,
            'status': 'TRIAL',
            'client': {
                'id': client_info.get('id', 0),
                'name': client_info.get('name', ''),
                'username': client_info.get('username', ''),
                'email': client_info.get('email', ''),
            },
            'tariff': {
                'id': tariff_info.get('id', 0),
                'name': tariff_info.get('name', ''),
                'size': tariff_info.get('size', 0),
                'websites': tariff_info.get('websites', 0),
                'databases': tariff_info.get('databases', 0),
            },
        }
