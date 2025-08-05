from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Date,
    JSON,
    ForeignKey,
    Index,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from collecte.schemas.base import Base


class ScheduleSnapshot(Base):
    """Time series data for schedule availability tracking"""

    __tablename__ = "schedule_snapshots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(255), index=True)
    crawled_at = Column(DateTime, index=True)  # When this data was collected

    # Link to collection (derived from URL)
    collection_id = Column(Integer, ForeignKey("collections.id"), nullable=True)

    # Relationships
    collection = relationship("Collection", back_populates="schedule_snapshots")
    events = relationship(
        "ScheduleEvent", back_populates="snapshot", cascade="all, delete-orphan"
    )

    # Unique constraint to prevent duplicate snapshots
    __table_args__ = (Index("ix_schedule_snapshots_url_time", "url", "crawled_at"),)


class ScheduleEvent(Base):
    """Individual events within a schedule snapshot"""

    __tablename__ = "schedule_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    snapshot_id = Column(Integer, ForeignKey("schedule_snapshots.id"), index=True)

    date = Column(Date, index=True)
    event_type = Column(String(20))  # blood, plasma, platelet
    total_slots = Column(Integer)

    # Store detailed time slots as JSON
    schedules = Column(JSON)  # {"09h00": 1, "09h15": 2, ...}

    # Computed fields for easy querying
    available_slots = Column(Integer)  # Sum of all schedules values

    # Relationships
    snapshot = relationship("ScheduleSnapshot", back_populates="events")

    # Indexes
    __table_args__ = (
        Index("ix_schedule_events_date_type", "date", "event_type"),
        UniqueConstraint(
            "snapshot_id", "date", "event_type", name="unique_event_per_snapshot"
        ),
    )
