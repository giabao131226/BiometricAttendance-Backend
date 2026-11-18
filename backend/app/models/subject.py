from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from sqlalchemy import String, Integer 


class Subject(Base):
    __tablename__ = "subject"

    subject_id: Mapped[str] = mapped_column(String(20), primary_key=True)
    subject_name: Mapped[str] = mapped_column(String(150))
    credits: Mapped[int | None] = mapped_column(Integer, nullable=True)
    
