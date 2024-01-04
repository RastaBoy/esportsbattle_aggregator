import asyncio
from services.aggregator.esportsbattle import CS2MatchesAggregator, FootballMatchesAggregator

async def req():
    matches = await CS2MatchesAggregator().aggragate()
    print(matches)    
    ...

if __name__ == "__main__":
    asyncio.run(req())
