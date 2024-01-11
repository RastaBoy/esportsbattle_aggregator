import typing

from . import api_v1_blueprint, response_wrapper

from .....db import DataBaseController
from .....db.services.matches import MatchService
from .....db.models.matches import MatchModel

@api_v1_blueprint.get('/matches/get_all')
@response_wrapper
async def get_all_matches():
    async with DataBaseController.get_session() as session:
        matches : typing.List[MatchModel] = await MatchService(session).get_all()
        return [ match.as_dict() for match in matches ]        