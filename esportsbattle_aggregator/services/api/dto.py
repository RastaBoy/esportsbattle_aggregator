import dataclasses
import typing
import datetime

# ---------------------------------------------------
# Статусы
# ---------------------------------------------------

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


# ---------------------------------------------------
# Матчи
# ---------------------------------------------------

@dataclasses.dataclass
class TeamInfo:
    id : int
    token : str


@dataclasses.dataclass
class ParticipantInfo:
    id : int
    team : TeamInfo
    

@dataclasses.dataclass
class MatchInfo:
    id : int
    date_time : datetime.datetime
    status_id : str
    participant1 : ParticipantInfo
    participant2 : ParticipantInfo

    
@dataclasses.dataclass
class TournamentInfo:
    id : int
    status_id : str
    token_international : str
    matches : typing.Optional[typing.List[MatchInfo]] = None
