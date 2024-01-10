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


    async def update(
        self,
        tournaments : typing.List[dto.TournamentInfo]
    ) -> None:
        try:
            log.info('Обновление информации в базе данных...')
            actual_matches : typing.List[dto.MatchInfo] = []
            for arr in [el.matches for el in tournaments]:
                actual_matches.extend(arr)
            
            actual_ids = [el.id for el in actual_matches]

            db_matches = await self.match_service.get_all()
            
            if db_matches:
                matches_to_remove = []
                for db_match in db_matches:
                    if not db_match.original_id in actual_ids:
                        matches_to_remove.append(db_match.id)

                matches_to_remove = [1, ]
                if matches_to_remove:
                    await self.match_service.session.execute(text(f"DELETE FROM matches WHERE id IN ({",".join([str(el) for el in matches_to_remove])})"))
                    # await self.match_service.commit()
            
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
            log.info("Обновление завершено.")
        except Exception as exc:
            log.exception(f"В ходе обновления информации в базе данных возникло исключение \"{exc.__class__.__name__}\": {str(exc)}")
