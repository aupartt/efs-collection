from datetime import datetime, time
from typing import Optional, TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


from .base import BaseModel

if TYPE_CHECKING:
    from .collection import CollectionModel


class SnapshotCollectionModel(BaseModel):
    """SQLAlchemy: Time series data for collection availability tracking"""

    __tablename__ = "collection_snapshots"

    snapshot_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id: Mapped[int]  # EFS id
    efs_id: Mapped[Optional[int]]  # ID from the url
    date: Mapped[datetime] = mapped_column(
        index=True
    )  # When the collection is happening
    lp_code: Mapped[str] = mapped_column(String(10))

    # Date and timing
    morning_start_time: Mapped[Optional[time]]
    morning_end_time: Mapped[Optional[time]]
    afternoon_start_time: Mapped[Optional[time]]
    afternoon_end_time: Mapped[Optional[time]]

    # Capacity info
    taux_remplissage: Mapped[Optional[float]]  # Fill rate
    nb_places_restantes_st: Mapped[Optional[int]]  # Blood remaining slots
    nb_places_totales_st: Mapped[Optional[int]]  # Blood total slots
    nb_places_reservees_st: Mapped[Optional[int]]  # Blood reserved slots
    nb_places_restantes_pla: Mapped[Optional[int]]  # Plasma remaining slots
    nb_places_totales_pla: Mapped[Optional[int]]  # Plasma total slots
    nb_places_reservees_pla: Mapped[Optional[int]]  # Plasma reserved slots
    nb_places_restantes_cpa: Mapped[Optional[int]]  # Platelet remaining slots
    nb_places_totales_cpa: Mapped[Optional[int]]  # Platelet total slots
    nb_places_reservees_cpa: Mapped[Optional[int]]  # Platelet reserved slots

    # Relationships
    collection_id: Mapped[int] = mapped_column(ForeignKey("collections.id"))
    collection: Mapped["CollectionModel"] = relationship(back_populates="snapshots")
    schedules: Mapped["SnapshotSchedulesModel"] = relationship(
        back_populates="snapshot", cascade="all, delete-orphan"
    )


class SnapshotSchedulesModel(BaseModel):
    """SQLAlchemy: Time series data for schedule availability tracking"""

    __tablename__ = "crawled_snapshots"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    url: Mapped[str]
    efs_id: Mapped[Optional[int]]  # ID from the url
    crawled_at: Mapped[datetime] = mapped_column(
        index=True
    )  # When this data was collected
    slots: Mapped[int]  # Number of slots available at crawl time
    schedules: Mapped[dict]  # JSON of schedules at crawl time

    # Relationships
    snapshot_id: Mapped[int] = mapped_column(
        ForeignKey("collection_snapshots.snapshot_id")
    )
    snapshot: Mapped["SnapshotCollectionModel"] = relationship(
        back_populates="schedules"
    )