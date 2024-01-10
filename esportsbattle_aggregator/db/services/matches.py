from .abc import IDBService
from ..models.models import MatchModel


class MatchService(IDBService[MatchModel]):
    ...