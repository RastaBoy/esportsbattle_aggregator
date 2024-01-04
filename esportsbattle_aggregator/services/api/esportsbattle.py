import typing

from . import abc
from . import dto
"""
Основная проблема в текущей задаче в том, 
что endpoint'ы и подходы для получения информации по турнирам/матчам 
в дисциплинах CS2 и Футбол отличаются друг от друга
"""

class ESportsBattleApiHelper(abc.ApiService):
    async def __get_statuses__(self) -> dto.ESportsBattleStatuses:
        # TODO размаппить в структуру какую-нибудь
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
