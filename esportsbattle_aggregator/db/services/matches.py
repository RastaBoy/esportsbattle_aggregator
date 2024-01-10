from .abc import IDBService
from ..models.matches import MatchModel


class MatchService(IDBService[MatchModel]):
    ...