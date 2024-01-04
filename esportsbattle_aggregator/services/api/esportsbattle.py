import typing
import datetime
import asyncio

from . import abc
from . import dto

"""
Основная проблема в текущей задаче в том, 
что endpoint'ы и подходы для получения информации по турнирам/матчам 
в дисциплинах CS2 и Футбол отличаются друг от друга
"""

class ESportsBattleApiHelper(abc.ApiService):
    async def get_statuses(self) -> dto.ESportsBattleStatuses:
        '''
        В рамках задачи нас интересует вполне один конкретный статус, по которым мы и будем выборку делать,
        но технически можно описать все статусы и это будет работать, если в рамках API они имеют одинаковые названия
        '''
        response : dict = await self.__send_request__(
            'GET',
            '/statuses'
        )

        # Магия Васянства
        # TODO Переписать на что-то более читаемое
        # ------------------------------------
        match_statuses, tournament_statuses = None, None
        if response.get('match') is not None:
            match_statuses = dto.MatchStatus(
                **dict(
                    [(status['code'], status['id']) for status in filter(
                        lambda el: el['code'] in dto.MatchStatus.__dataclass_fields__, 
                        response['match']
                    )]
                )
            )
        
        if response.get('tournament') is not None:
            tournament_statuses = dto.TournamentStatus(
                **dict(
                    [(status['code'], status['id']) for status in filter(
                        lambda el: el['code'] in dto.TournamentStatus.__dataclass_fields__, 
                        response['tournament']
                    )]
                )
            )
        # ------------------------------------

        return dto.ESportsBattleStatuses(
            tournament_statuses=tournament_statuses,
            match_statuses=match_statuses
        )
    

    async def get_all_matches(self) -> typing.List[typing.Any]:
        raise Exception(f"В данном классе не реализован метод получения информации о ближайших матчах")




class CS2ESportsBattleAPIHelper(ESportsBattleApiHelper):
    def __init__(self):
        super().__init__(
            url='https://cs2.esportsbattle.com/api/'    
        )

    async def get_tournaments(self) -> typing.List[dto.TournamentInfo]:
        response : dict = await self.__send_request__(
            'GET',
            '/tournaments',
            query={
                'page' : 1,
                'dateFrom' : datetime.datetime(2024, 1, 2, 17, 0, 0).isoformat(),
                'dateTo' : datetime.datetime(2025, 1, 2, 17, 0, 0).isoformat()
            }
        )

        result = []
        if response.get('tournaments') is not None:
            for el in response.get('tournaments'):
                result.append(
                    dto.TournamentInfo(
                        id=int(el.get('id')),
                        status_id=el.get('status_id'),
                        token_international=el.get('token_international')
                    )
                )
        
        return result


    async def get_tournament_matches(self, tournament_id : str) -> typing.List[dto.MatchInfo]:
        response : list = await self.__send_request__(
            'GET',
            f'/tournaments/{tournament_id}/matches'
        )

        result = []
        for el in response:
            result.append(
                dto.MatchInfo(
                    id=int(el.get('id')),
                    date_time=datetime.datetime.fromisoformat(el.get('date')),
                    status_id=el.get('status_id'),
                    participant1=dto.ParticipantInfo(
                        id=int(el['participant1']['id']),
                        team=dto.TeamInfo(
                            id=int(el['participant1']['team']['id']),
                            token=el['participant1']['team']['token_international']
                        )
                    ),
                    participant2=dto.ParticipantInfo(
                        id=int(el['participant2']['id']),
                        team=dto.TeamInfo(
                            id=int(el['participant2']['team']['id']),
                            token=el['participant2']['team']['token_international']
                        )
                    )
                )
            )
        
        return result


    async def get_all_matches(self) -> typing.List[dto.MatchInfo]:
        tournaments = await self.get_tournaments()
        matches = []
        # TODO Оптимизировать эту часть
        # Можно сделать через таски, чтобы выполнялось синхронно
        tasks = []
        for tournament in tournaments:
            tasks.append(asyncio.create_task(self.get_tournament_matches(tournament.id)))

        results = await asyncio.gather(*tasks)

        for result in results:
            matches.extend(result)

        return matches


class FootballESportsBattleAPIHelper(ESportsBattleApiHelper):
    def __init__(self):
        super().__init__(
            url='https://football.esportsbattle.com/api/'
        )

    
    async def get_all_matches(self) -> typing.List[dto.MatchInfo]:
        response : list = await self.__send_request__(
            'GET',
            '/tournaments/nearest-matches'
        )

        result = []
        for el in response:
            result.append(
                dto.MatchInfo(
                    id=int(el.get('id')),
                    date_time=datetime.datetime.fromisoformat(el.get('date')),
                    status_id=el.get('status_id'),
                    participant1=dto.ParticipantInfo(
                        id=int(el['participant1']['id']),
                        team=dto.TeamInfo(
                            id=int(el['participant1']['team']['id']),
                            token=el['participant1']['team']['token_international']
                        )
                    ),
                    participant2=dto.ParticipantInfo(
                        id=int(el['participant2']['id']),
                        team=dto.TeamInfo(
                            id=int(el['participant2']['team']['id']),
                            token=el['participant2']['team']['token_international']
                        )
                    )
                )
            )
            
        return result