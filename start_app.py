
import os
import dotenv
import asyncio

from loguru import logger as log

from esportsbattle_aggregator.app import start_app

__version__ = (1,0,0,0)


# TODO Вынести LogLevel в глобальные переменные
log.add(
    os.path.join(os.getcwd(), 'logs', '{time:DD-MM-YYYY}.log'), 
    format='{time:HH:mm:ss.SSSZ} | [{level}]\t| {message}'
)
log.critical('='*15 + ' Инициализация ESportsBattle Aggregator v'+".".join(str(x) for x in __version__) + ' ' +'='*15)

# __dotenv_path__ = os.path.join(os.getcwd(), 'test', '.env')
__dotenv_path__ = os.path.join(os.getcwd(), '.env')
if os.path.exists(__dotenv_path__):
    dotenv.load_dotenv(__dotenv_path__)


if __name__ == "__main__":
    asyncio.run(start_app())
