import typing
import asyncio

from typing import Any
from loguru import logger as log

from . import abc

from ..api import esportsbattle
from .. import dto
from . import exc as exceptions


class ESportsBattleTournamentsAggregator(abc.IAggregator):
    _statuses = None
    _tournaments = None

    def __init__(
        self, 
        api_helper : esportsbattle.ESportsBattleApiHelper
    ):
        self.api_helper = api_helper

    # Кэш нужен для того, чтобы не отправлять миллион запросов на API, 
    # в случае, если нам где-то извне понадобится информация о статусах и матчах

    @property
    async def statuses(self):
        if self._statuses is None:
            self._statuses = await self.api_helper.get_statuses()

        return self._statuses


    @property
    async def tournaments(self):
        # TODO Переделать
        if self._tournaments is None:
            self._tournaments = await self.__aggragate_tournaments__()
        
        return self._tournaments
    

    async def __aggragate_tournaments__(self) -> typing.List[dto.TournamentInfo]:
        try:
            tournaments : typing.List[dto.TournamentInfo] = []

            tournaments_info : dto.TournamentsInfoResponse = await self.api_helper.get_tournaments_info()
            tournaments.extend(tournaments_info.tournaments)
            if tournaments_info.total_pages > 1:
                cur_page = 1
                while cur_page <= tournaments_info.total_pages:
                    info : dto.TournamentsInfoResponse = await self.api_helper.get_tournaments_info(page=cur_page)
                    tournaments.extend(info.tournaments)                    
                    cur_page += 1
            
            return tournaments
        except Exception as exc:
            log.error(f"Не удалось собрать данные по дисциплине \"{self.api_helper.discipline_name}\" в связи с исключением \"{exc.__class__.__name__}\": {str(exc)}")
            raise exceptions.AggregatorException(f"Не удалось собрать данные по дисциплине \"{self.api_helper.discipline_name}\" в связи с исключением \"{exc.__class__.__name__}\": {str(exc)}")


    async def aggragate(self) -> typing.List[dto.TournamentInfo]:

        self._tournaments = await self.__aggragate_tournaments__()
        self._statuses = await self.api_helper.get_statuses()
        
        return self._tournaments
    
    

class CS2TournamentsAggregator(ESportsBattleTournamentsAggregator):
    def __init__(self):
        super().__init__(
            api_helper=esportsbattle.CS2ESportsBattleAPIHelper()
        )
    

class FootballTournamentsAggregator(ESportsBattleTournamentsAggregator):
    def __init__(self):
        super().__init__(
            api_helper=esportsbattle.FootballESportsBattleAPIHelper()
        )

    
