import asyncio
import aiohttp
import json
import enum

import datetime 

from services.api import abc
from services.api import esportsbattle

from datetime import datetime



async def req():
    # url = 'https://cs2.esportsbattle.com/api/tournaments?page=1&dateFrom=2024-01-02T17%3A00%3A00.000Z&dateTo=2025-01-03T16%3A59%3A59.000Z'
    # async with aiohttp.ClientSession() as session:
    #     async with session.get(url) as response:
    #         print(await response.json(encoding='utf-8'))
    
    # Список чемпионатов

    # response : dict = await ApiService(
    #     'https://cs2.esportsbattle.com/api/'
    # ).__send_request__(
    #     'GET',
    #     '/tournaments',
    #     query={
    #         'page' : 1,
    #         'dateFrom' : datetime(2024, 1, 2, 17, 0, 0).isoformat(),
    #         'dateTo' : datetime(2025, 1, 2, 17, 0, 0).isoformat()
    #     }
    # )

    # tournaments : list = response.get('tournaments')
    # for tournament in tournaments:
    #     try:
    #         print(f"Чемпионат \"{tournament.get('token_international')}\", Статус чемпионата: {TorunamentStatus(tournament.get('status_id')).name}")
    #     except ValueError:
    #         pass

    # Получение статусов
    
    # response = await esportsbattle.ESportsBattleApiHelper(
    #     'https://cs2.esportsbattle.com/api/'
    # ).get_statuses()
    # print(response)

    # time = '2024-01-04T06:00:00Z'
    # result = datetime.fromisoformat(time)
    # print(result)
    
    # result = await esportsbattle.CS2ESportsBattleAPIHelper().get_all_matches()
    # print(result)

    result = await esportsbattle.FootballESportsBattleAPIHelper().get_all_matches()
    print(result)


if __name__ == "__main__":
    asyncio.run(req())
