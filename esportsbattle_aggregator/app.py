import os

from loguru import logger as log


from .services.aggregator.esportsbattle import CS2TournamentsAggregator, FootballTournamentsAggregator

async def start_app():
    try:
        from . import config
    except KeyError as exc:
        log.error(f"Не удалось инициализировать файл настроек. Отсутствует значение {str(exc)}")
        return

    

    print(config.POSTGRES_USERNAME)
    # matches = await CS2TournamentsAggregator().aggragate()
    # print(matches)    
    ...

