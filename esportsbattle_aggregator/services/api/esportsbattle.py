import typing
import datetime
import asyncio

from loguru import logger as log

from . import abc
from .. import dto


class ESportsBattleApiHelper(abc.ApiService):
    def __init__(
            self, 
            url : str,
            discipline_name : str
        ) -> None:
        self.discipline_name=discipline_name
        super().__init__(url)

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
    

    async def get_tournaments_info(self, page=1) -> dto.TournamentsInfoResponse:
        # TODO Изменить возвращаемое значение у метода,
        # Теперь он будет возвращать dto.TournamentsInfoResponse,
        # Где будет информация по числу страниц

        # Турниры располагаются на множестве страниц, 
        # Поле totalPages - относительно него нужно скакать
        response : dict = await self.__send_request__(
            'GET',
            '/tournaments',
            query={
                'page' : page,
                'dateFrom' : datetime.datetime.now().strftime('%Y/%m/%d'),
                'dateTo' : (datetime.datetime.now() + datetime.timedelta(days=365)).strftime('%Y/%m/%d')
            }
        )

        tournaments = []
        total_pages = response.get('totalPages')
        if response.get('tournaments') is not None:
            if response.get('tournaments'):
                for el in response.get('tournaments'):
                    tournaments.append(
                        dto.TournamentInfo(
                            id=int(el.get('id')),
                            discipline_name=self.discipline_name,
                            status_id=el.get('status_id'),
                            token_international=el.get('token_international')
                        )
                    )
        tasks = []
        for tournament in tournaments:
            tasks.append(asyncio.create_task(self.fill_tournament_matches(tournament)))
        
        await asyncio.gather(*tasks)

        # На этом этапе есть список чемпионатов с заполненными матчами
        # if page < total_pages:
        #     tournaments.extend(await self.get_tournaments(page=page+1))
            

        return dto.TournamentsInfoResponse(
            total_pages=total_pages,
            tournaments=tournaments
        )


    async def fill_tournament_matches(self, tournament : dto.TournamentInfo):
        matches = await self.get_tournament_matches(tournament.id)
        tournament.matches.extend(matches)


    async def get_tournament_matches(self, tournament_id : str) -> typing.List[dto.MatchInfo]:
        try:
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
        except Exception:
            return []
        

class CS2ESportsBattleAPIHelper(ESportsBattleApiHelper):
    def __init__(self):
        super().__init__(
            url='https://cs2.esportsbattle.com/api/',
            discipline_name='CS2'    
        )



class FootballESportsBattleAPIHelper(ESportsBattleApiHelper):
    def __init__(self):
        super().__init__(
            url='https://football.esportsbattle.com/api/',
            discipline_name='FootBall'
        )
