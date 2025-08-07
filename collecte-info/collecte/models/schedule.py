from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel
if TYPE_CHECKING:
    from .collection import CollectionModel


class ScheduleSnapshotModel(BaseModel):
    """SQLAlchemy: Time series data for schedule availability tracking"""

    __tablename__ = "schedule_snapshots"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    url: Mapped[str] = mapped_column(index=True)
    crawled_at: Mapped[datetime] = mapped_column(
        index=True
    )  # When this data was collected

    # Link to collection (derived from URL)
    collection_id: Mapped[int] = mapped_column(ForeignKey("collections.id"))

    # Relationships
    collection: Mapped["CollectionModel"] = relationship(
        back_populates="schedule_snapshots"
    )
    events: Mapped[list["ScheduleEventModel"]] = relationship(
        back_populates="snapshot", cascade="all, delete-orphan"
    )


class ScheduleEventModel(BaseModel):
    """SQLAlchemy: Individual events within a schedule snapshot"""

    __tablename__ = "schedule_events"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    snapshot_id: Mapped[int] = mapped_column(
        ForeignKey("schedule_snapshots.id"), index=True
    )

    date: Mapped[datetime] = mapped_column(index=True)
    event_type: Mapped[str] = mapped_column(String(10))  # blood, plasma, platelet
    slots: Mapped[int]

    # Store detailed time slots as JSON
    schedules: Mapped[dict]  # {"09h00": 1, "09h15": 2, ...}

    # Relationships
    snapshot: Mapped["ScheduleSnapshotModel"] = relationship(back_populates="events")
