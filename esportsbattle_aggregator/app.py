import asyncio
import os

from loguru import logger as log

from services.aggregator.esportsbattle import CS2TournamentsAggregator, FootballTournamentsAggregator


__version__ = (1,0,0,0)

log.add(
    os.path.join(os.getcwd(), 'logs', '{time:DD-MM-YYYY}.log'), 
    format='{time:HH:mm:ss.SSSZ} | [{level}]\t| {message}'
)
log.critical('='*15 + ' Инициализация ESportsBattle Aggregator v'+".".join(str(x) for x in __version__) + ' ' +'='*15)


async def start_app():
    matches = await CS2TournamentsAggregator().aggragate()
    print(matches)    
    ...

if __name__ == "__main__":
    asyncio.run(start_app())
