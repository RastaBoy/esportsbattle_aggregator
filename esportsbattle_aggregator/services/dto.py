import dataclasses
import typing
import datetime

# ---------------------------------------------------
# Статусы
# ---------------------------------------------------

@dataclasses.dataclass
class TournamentStatus:
    draft : typing.Union[str, int]
    public : typing.Union[str, int]
    ready_to_public : typing.Union[str, int]
    started : typing.Union[str, int]
    finished : typing.Union[str, int]
    canceled : typing.Union[str, int]
    deleted : typing.Union[str, int]


@dataclasses.dataclass
class MatchStatus:
    new : typing.Union[str, int]
    active : typing.Union[str, int]
    finished : typing.Union[str, int]
    canceled : typing.Union[str, int]
    ready_to_finish : typing.Union[str, int]
    deleted : typing.Union[str, int]


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
    discipline_name : str
    status_id : str
    token_international : str
    matches : typing.List[MatchInfo] = dataclasses.field(default_factory=list)
