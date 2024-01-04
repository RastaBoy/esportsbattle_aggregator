import typing
from typing import Any

from . import abc

from ..api import esportsbattle
from ..api import dto as esportsbattle_dto


class MatchesAggregator(abc.IAggregator):
    _statuses = None
    _matches = None

    def __init__(self, api_helper : esportsbattle.ESportsBattleApiHelper):
        self.api_helper = api_helper


    @property
    async def statuses(self):
        if self._statuses is None:
            statuses = await self.api_helper.get_statuses()
            self._statuses = statuses

        return self._statuses


    @property
    async def matches(self):
        if self._matches is None:
            matches = await self.api_helper.get_all_matches()
            self._matches = matches
        
        return self._matches
    
    

class CS2MatchesAggregator(MatchesAggregator):
    def __init__(self):
        super().__init__(
            api_helper=esportsbattle.CS2ESportsBattleAPIHelper()
        )
    
    async def aggragate(self) -> typing.List[esportsbattle_dto.MatchInfo]:
        statuses = await self.api_helper.get_statuses()
        matches : typing.List[esportsbattle_dto.MatchInfo] = await self.api_helper.get_all_matches()

        # Обновляем временное хранилище
        self._matches = matches
        self._statuses = statuses

        # Собираем актуальные матчи
        actual_statuses = [statuses.match_statuses.new, ]
        res = []
        for match in matches:
            if match.status_id in actual_statuses:
                res.append(match)
        
        return res


class FootballMatchesAggregator(MatchesAggregator):
    def __init__(self):
        super().__init__(
            api_helper=esportsbattle.FootballESportsBattleAPIHelper()
        )

    async def aggragate(self) -> typing.List[esportsbattle_dto.MatchInfo]:
        # Копировать код нехорошо, но пока в голове нету идей, как это можно оптимизировать
        statuses = await self.api_helper.get_statuses()
        matches : typing.List[esportsbattle_dto.MatchInfo] = await self.api_helper.get_all_matches()

        # Обновляем временное хранилище
        self._matches = matches
        self._statuses = statuses

        # Собираем актуальные матчи
        actual_statuses = [statuses.match_statuses.new, ]
        res = []
        for match in matches:
            if match.status_id in actual_statuses:
                res.append(match)
        
        return res
