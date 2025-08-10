from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from collecte.models.base import Base

from collecte.models import CollectionEventModel


class ScheduleModel(Base):
    """SQLAlchemy: Informations relative to a schedule event"""

    __tablename__ = "schedules"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    efs_id: Mapped[str] = mapped_column(index=True)

    # Details
    date: Mapped[datetime]
    url: Mapped[str]
    created_at: Mapped[str]

    # Data
    total_slots: Mapped[int]
    collecte_type: Mapped[str]
    schedules: Mapped[dict]

    # Relationships
    event_id: Mapped[int] = mapped_column(ForeignKey("collection_events.id"))
    event: Mapped["CollectionEventModel"] = relationship(back_populates="snapshots")
