from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column

from . import Base

class MatchModel(Base):
    __tablename__ = 'matches'

    id : Mapped[int] = mapped_column(primary_key=True)
    discipline_name : Mapped[str] = mapped_column(nullable=False)
    tournament_name : Mapped[str] = mapped_column(nullable=False)
    date_time : Mapped[datetime] = mapped_column(nullable=False)
    participant1_name : str = mapped_column(nullable=False)    
    participant2_name : str = mapped_column(nullable=False)    

