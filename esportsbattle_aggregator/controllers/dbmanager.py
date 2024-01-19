import typing

from loguru import logger as log
from sqlalchemy.sql import text

from ..services import dto

from ..db.services.matches import MatchService
from ..db.models.matches import MatchModel




class ESportsBattleDBManager:
    def __init__(
        self,
        match_service : MatchService
    ):
        self.match_service=match_service

    async def remove_unactual_matches(
        self,
        current_match_list : typing.List[MatchModel],
        actual_ids_list : typing.List[int]
    ) -> None:
        '''Удаление лишних записей из базы данных'''
        if current_match_list:
            for db_match in current_match_list:
                if not db_match.original_id in actual_ids_list:
                    await self.match_service.delete(db_match, True)                


    async def update(
        self,
        tournaments : typing.List[dto.TournamentInfo]
    ) -> None:
        try:
            log.info('Обновление информации в базе данных...')
            actual_matches : typing.List[dto.MatchInfo] = []
            for arr in [el.matches for el in tournaments]:
                actual_matches.extend(arr)
            
            # Начало процесса удаления неактуальной информации в Б/д
            # ------------------------------------------------------
            actual_ids = [el.id for el in actual_matches]
            actual_ids = [1, ]

            db_matches = await self.match_service.get_all()

            await self.remove_unactual_matches(db_matches, actual_ids)
            # ------------------------------------------------------
            # TODO Уверен, можно оптимизировать
            # ------------------------------------------------------
            db_matches_original_ids = [el.original_id for el in (await self.match_service.get_all())]
            for tournament in tournaments:
                for match in tournament.matches:
                    if not match.id in db_matches_original_ids:
                        await self.match_service.update(
                            MatchModel(
                                original_id=match.id,
                                discipline_name=tournament.discipline_name,
                                tournament_name=tournament.token_international,
                                date_time=match.date_time,
                                participant1_name=match.participant1.team.token,
                                participant2_name=match.participant2.team.token
                            )
                        )

            await self.match_service.commit()
            # ------------------------------------------------------

            log.info("Обновление завершено.")
        except Exception as exc:
            log.exception(f"В ходе обновления информации в базе данных возникло исключение \"{exc.__class__.__name__}\": {str(exc)}")
