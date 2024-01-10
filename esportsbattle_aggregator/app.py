import os

from loguru import logger as log

from .services.aggregator.esportsbattle import CS2TournamentsAggregator, FootballTournamentsAggregator



async def start_app():
    print(os.environ['TEST'])
    print(os.environ['POSTGRES'])
    # matches = await CS2TournamentsAggregator().aggragate()
    # print(matches)    
    ...

