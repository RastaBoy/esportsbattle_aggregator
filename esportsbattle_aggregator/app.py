import asyncio
from services.aggregator.esportsbattle import CS2MatchesAggregator, FootballMatchesAggregator

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
    matches = await CS2MatchesAggregator().aggragate()
    print(matches)    
    ...

if __name__ == "__main__":
    asyncio.run(req())
