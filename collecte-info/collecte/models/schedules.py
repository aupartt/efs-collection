from datetime import date, datetime, time

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from collecte.models import CollectionEventModel
from collecte.models.base import Base


class ScheduleModel(Base):
    """SQLAlchemy: Informations relative to a schedule event"""

    __tablename__ = "schedules"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    efs_id: Mapped[str] = mapped_column(index=True)

    # Details
    date: Mapped[date]
    url: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    # Data
    total_slots: Mapped[int]
    collecte_type: Mapped[str]
    timetables: Mapped[dict]
    timetable_min: Mapped[time]
    timetable_max: Mapped[time]

    # Relationships
    event_id: Mapped[int] = mapped_column(ForeignKey("collection_events.id", ondelete="CASCADE"))
    event: Mapped["CollectionEventModel"] = relationship(back_populates="snapshots")
