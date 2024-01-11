import typing

from datetime import datetime
from sqlalchemy import DateTime

from sqlalchemy.orm import Mapped, mapped_column

from . import Base

class MatchModel(Base):
    __tablename__ = 'matches'

    id : Mapped[int] = mapped_column(primary_key=True)
    original_id : Mapped[int] = mapped_column(nullable=False)
    discipline_name : Mapped[str] = mapped_column(nullable=False)
    tournament_name : Mapped[str] = mapped_column(nullable=False)
    date_time : Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    participant1_name : Mapped[str] = mapped_column(nullable=False)    
    participant2_name : Mapped[str] = mapped_column(nullable=False)


    def as_dict(self) -> typing.Dict[str, typing.Union[str, int]]:
        return {
            "id" : self.id,
            "original_id" : self.original_id,
            "discipline_name" : self.discipline_name,
            "tournament_name" : self.tournament_name,
            "date" : self.date_time.strftime("%d-%m-%Y"),
            "time" : self.date_time.strftime("%H:%M:%S"),
            "participant1_name" : self.participant1_name,
            "participant2_name" : self.participant2_name
        }
    

