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
    

