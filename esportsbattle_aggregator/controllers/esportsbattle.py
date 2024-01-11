import typing
import enum
import aiohttp

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


    async def get_filtered_data(
        self,
        tournament_statuses : typing.List[TournamentStatus],
        match_statuses : typing.List[MatchStatus]
    ):
        data = []
        for aggregator in self.aggregators:
            # TODO Не факапить всё, если не получилось по одной дисциплине собрать статусы или данные
            try:
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
                data.extend(
                    self.filter(
                        tournaments,
                        actual_torunament_statuses,
                        actual_match_statuses
                    )
                )
            except aiohttp.ClientResponseError as exc:
                log.error(f"Не удалось собрать данные по агрегатору \"{aggregator.__class__.__name__}\" по причине \"{exc.__class__.__name__}\": {str(exc)}")
                continue        
        return data
