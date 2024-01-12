import typing
from typing import Any

from . import abc

from ..api import esportsbattle
from .. import dto as esportsbattle_dto


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
        if self._tournaments is None:
            self._tournaments = await self.api_helper.get_tournaments()
        
        return self._tournaments
    

    async def aggragate(self) -> typing.List[esportsbattle_dto.TournamentInfo]:
        statuses = await self.api_helper.get_statuses()
        tournaments : typing.List[esportsbattle_dto.TournamentInfo] = await self.api_helper.get_tournaments()

        # Обновляем временное хранилище
        self._tournaments = tournaments
        self._statuses = statuses
        
        return tournaments
    
    

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

    
