import aiohttp

from aiohttp import ClientResponseError

from typing import Dict, Optional, Any


class ApiService():
    def __init__(
        self,
        url : str
    ) -> None:
        self.url=url.rstrip('/')

    
    async def __send_request__(
            self,
            method : str,
            endpoint : str,
            query : Optional[Dict[str, str]] = None,
            headers : Optional[Dict[str, str]] = None,
            data : Any = None,
            json : Any = None
    ) -> Any:
        # TODO Надо бы доработать обработку ошибок и не факт, что оно всегда json возвращает
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method, 
                self.url + endpoint,
                params=query,
                headers=headers,
                data=data,
                json=json,
            ) as response:
                response.raise_for_status()
                return await response.json()
