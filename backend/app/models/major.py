from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from sqlalchemy import String, ForeignKey, Numeric
from decimal import Decimal

class Major(Base):
    __tablename__ = "major"

    major_id: Mapped[str] = mapped_column(String(20), primary_key=True)
    major_name: Mapped[str] = mapped_column(String(150))
    faculty_id: Mapped[str] = mapped_column(ForeignKey("faculty.faculty_id"))
    duration_years: Mapped[Decimal | None] = mapped_column(Numeric(3,1), nullable=True)
    
