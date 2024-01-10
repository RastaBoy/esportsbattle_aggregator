import os
import asyncio

from loguru import logger as log

from .db import DataBaseController
from .db.services.matches import MatchService

from .controllers.dbmanager import ESportsBattleDBManager
from .controllers.esportsbattle import ESportsBattleTournamentsFilter, MatchStatus, TournamentStatus

from .services.aggregator.esportsbattle import CS2TournamentsAggregator, FootballTournamentsAggregator

async def start_app():
    try:
        from . import config
    except KeyError as exc:
        log.error(f"Не удалось инициализировать файл настроек. Отсутствует значение {str(exc)}")
        return

    log.info("Инициализация базы данных...")
    try:
        await DataBaseController.create_database()
    except Exception as exc:
        log.exception(f"Не удалось инициализировать базу данных в связии с исключением \"{exc.__class__.__name__}\": {str(exc)}.", exc)
        return
    log.info("База данных инициализирована.")

    await main_loop(int(config.UPDATE_TIMEOUT))
    # matches = await CS2TournamentsAggregator().aggragate()
    # print(matches)    
    ...



async def main_loop(update_timeout : int = 60):
    tournaments_filter = ESportsBattleTournamentsFilter(
        [
            CS2TournamentsAggregator(),
            FootballTournamentsAggregator()
        ]
    )
    while True:
        try:
            filtered_tournaments = await tournaments_filter.get_filtered_data(
                tournament_statuses=[
                    TournamentStatus.PUBLIC,
                    TournamentStatus.STARTED
                ],
                match_statuses=[
                    MatchStatus.NEW,
                ]
            )
            async with DataBaseController.get_session() as session:
                await ESportsBattleDBManager(MatchService(session)).update(filtered_tournaments)
                
        except Exception as exc:
            log.exception(f"В ходе агрегации данных возникло исключение \"{exc.__class__.__name__}\": {str(exc)}", exc)
            await asyncio.sleep(15)
        finally:
            await asyncio.sleep(update_timeout)
        