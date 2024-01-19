import typing
import enum
import aiohttp
import asyncio
import dataclasses

from loguru import logger as log

from ..services import dto
from ..services.aggregator.esportsbattle import ESportsBattleTournamentsAggregator


class TournamentStatus(enum.Enum):
    DRAFT = "draft" 
    PUBLIC = "public" 
    READY_TO_PUBLIC = "ready_to_public" 
    STARTED = "started" 
    FINISHED = "finished" 
    CANCELED = "canceled" 
    DELETED = "deleted" 


class MatchStatus(enum.Enum):
    NEW = "new"
    ACTIVE = "active"
    FINISHED = "finished"
    CANCELED = "canceled"
    READY_TO_FINISH = "ready_to_finish"
    DELETED = "deleted"


# TODO Нейминг. 
class ESportsBattleTournamentsFilter:
    '''
    Класс, который фильтрует собранные агрегаторами чемпионаты/матчи
    '''
    def __init__(
        self, 
        aggregators : typing.List[ESportsBattleTournamentsAggregator]
    ):
        self.aggregators = aggregators

    
    def __get_status_codes__(
        self, 
        statuses_info : typing.Union[dto.MatchStatus, dto.TournamentStatus], 
        intested_statuses : typing.List[typing.Union[TournamentStatus, MatchStatus]]
    ) -> typing.List[typing.Union[str, int]]:
        result = []
        for status in intested_statuses:
            if hasattr(statuses_info, status.value):
                result.append(getattr(statuses_info, status.value))
        
        return result


    def filter(
        self, 
        tournaments : typing.List[dto.TournamentInfo], 
        tournament_statuses : typing.List[typing.Union[str, int]],
        match_statuses : typing.List[typing.Union[str, int]]
    ) -> typing.List[dto.TournamentInfo]:
        result = []
        # Будем создавать копии объектов, чтобы случайно не удалить информацию из объектов в памяти
        for tournament in tournaments:
            if tournament.status_id in tournament_statuses:
                matches = []
                for match in tournament.matches:
                    if match.status_id in match_statuses:
                        matches.append(
                            dto.MatchInfo(
                                id=match.id,
                                date_time=match.date_time,
                                status_id=match.status_id,
                                participant1=dto.ParticipantInfo(
                                    id=match.participant1.id,
                                    team=dto.TeamInfo(
                                        id=match.participant1.team.id,
                                        token=match.participant1.team.token
                                    )
                                ),
                                participant2=dto.ParticipantInfo(
                                    id=match.participant2.id,
                                    team=dto.TeamInfo(
                                        id=match.participant2.team.id,
                                        token=match.participant2.team.token
                                    )
                                )
                            )
                        )
                result.append(
                    dto.TournamentInfo(
                        id=tournament.id,
                        discipline_name=tournament.discipline_name,
                        status_id=tournament.status_id,
                        token_international=tournament.token_international,
                        matches=matches
                    )
                )

        return result
    
    def __count_matches__(self, tournaments : typing.List[dto.TournamentInfo]) -> int:
        count = 0
        for t in tournaments:
            count += len(t.matches)
        return count


    async def __get_aggregator_filtered_tournaments__(
        self, 
        aggregator : ESportsBattleTournamentsAggregator,
        tournament_statuses : typing.List[TournamentStatus],
        match_statuses : typing.List[MatchStatus]
    ) -> typing.List[dto.TournamentInfo]:
        
        filtered_tournaments : typing.List[dto.TournamentInfo] = []

        tournaments = await aggregator.aggragate()
        statuses_info = await aggregator.statuses


        actual_torunament_statuses = self.__get_status_codes__(
            statuses_info=statuses_info.tournament_statuses, 
            intested_statuses=tournament_statuses
        )
        actual_match_statuses = self.__get_status_codes__(
            statuses_info=statuses_info.match_statuses,
            intested_statuses=match_statuses
        )
        
        # ------------------------------------------------------------
        # Отладка
        # ------------------------------------------------------------
        log.debug(f"Сбор данных от агрегатора \"{aggregator.__class__.__name__}\"")
        log.debug(f"Входное число чемпионатов: {len(tournaments)}")
        log.debug(f"Входное число матчей: {self.__count_matches__(tournaments)}")
        log.debug(f"Перечень статусов для чемпионатов:\n{"\n".join([f"{ids}.{kv[0]} - {kv[1]}" for ids, kv in enumerate(dataclasses.asdict(statuses_info.tournament_statuses).items(), 1)])}")
        log.debug(f"Перечень статусов для матчей:\n{"\n".join([f"{ids}.{kv[0]} - {kv[1]}" for ids, kv in enumerate(dataclasses.asdict(statuses_info.match_statuses).items(), 1)])}")

        log.debug(f"Список актуальных статусов чемпионатов: {actual_torunament_statuses}")
        log.debug(f"Список актуальных статусов матчей: {actual_match_statuses}")
        # ------------------------------------------------------------

        filtered_tournaments.extend(
            self.filter(
                tournaments,
                actual_torunament_statuses,
                actual_match_statuses
            )
        )
        # ------------------------------------------------------------
        # Отладка
        # ------------------------------------------------------------
        log.debug(f"Число чемпионатов после фильтрации: {len(filtered_tournaments)}")
        log.debug(f"Число матчей после фильтрации: {self.__count_matches__(filtered_tournaments)}")
        # ------------------------------------------------------------
        return filtered_tournaments


    async def get_filtered_data(
        self,
        tournament_statuses : typing.List[TournamentStatus],
        match_statuses : typing.List[MatchStatus]
    ) -> typing.List[dto.TournamentInfo]:
        
        filtered_tournaments : typing.List[dto.TournamentInfo] = []

        tasks = []
        for aggregator in self.aggregators:
            tasks.append(
                asyncio.create_task(
                    self.__get_aggregator_filtered_tournaments__(
                        aggregator,
                        tournament_statuses,
                        match_statuses
                    )
                )
            )

        results = await asyncio.gather(*tasks)
        for result in results:
            filtered_tournaments.extend(result)

        return filtered_tournaments
