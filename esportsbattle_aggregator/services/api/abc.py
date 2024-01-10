import aiohttp

from aiohttp import ClientResponseError
from typing import Dict, Optional, Any
from loguru import logger as log


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
        # TODO Надо бы доработать обработку ошибок
        async with aiohttp.ClientSession() as session:
            log.debug(f"Отправка {method} запроса на URL \"{self.url + endpoint}\"...")
            try:
                async with session.request(
                    method, 
                    self.url + endpoint,
                    params=query,
                    headers=headers,
                    data=data,
                    json=json,
                ) as response:
                    response.raise_for_status()
                    result = await response.json()
                    log.debug(f"Получен ответ на {method} запрос на URL \"{self.url + endpoint}\": {result}")
                    return result
            except Exception as exc:
                log.exception(f"В ходе отправки запроса на URL \"{self.url + endpoint}\" возникло исключение \"{exc.__class__.__name__}\": {str(exc)}", exc)
                raise
