import dataclasses
import typing


@dataclasses.dataclass
class TournamentStatus:
    public : typing.Union[str, int]


@dataclasses.dataclass
class MatchStatus:
    new : typing.Union[str, int]


@dataclasses.dataclass
class ESportsBattleStatuses:
    tournament_statuses : TournamentStatus
    match_statuses : MatchStatus