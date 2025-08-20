from datetime import UTC, datetime, time
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from collecte.models.base import Base

if TYPE_CHECKING:
    from .location import LocationModel
    from .schedules import ScheduleModel


class CollectionGroupModel(Base):
    """SQLAlchemy: Global data for a group of events"""

    def __init__(self, **kw):
        mapper = self.__mapper__
        for key in mapper.relationships.keys():
            if key in kw:
                # Check if the value is a list of dictionaries
                if isinstance(kw[key], list):
                    # Create a list of instances for the relationship
                    kw[key] = [
                        mapper.relationships[key].entity.class_(**item)
                        if isinstance(item, dict)
                        else item
                        for item in kw[key]
                    ]
                elif isinstance(kw[key], dict):
                    # Create a single instance for the relationship
                    kw[key] = mapper.relationships[key].entity.class_(**kw[key])
        super().__init__(**kw)

    __tablename__ = "collection_groups"
    __table_args__ = (
        UniqueConstraint("efs_id", "nature", name="unique_collection_group"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    efs_id: Mapped[str | None] = mapped_column(unique=True, nullable=True, index=True)

    # Date
    start_date: Mapped[datetime]
    end_date: Mapped[datetime]

    # Details
    nature: Mapped[str | None]
    is_public: Mapped[bool]
    is_publishable: Mapped[bool]
    propose_planning_rdv: Mapped[bool]

    # URLs
    url_blood: Mapped[str | None]
    url_plasma: Mapped[str | None]
    url_platelet: Mapped[str | None]

    # Text descriptions
    convocation_label_long: Mapped[str | None]
    convocation_label_sms: Mapped[str | None]

    # Metadata
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    # Relationships
    group_code: Mapped[str] = mapped_column(ForeignKey("groups.gr_code", ondelete="CASCADE"))
    events: Mapped[list["CollectionEventModel"]] = relationship(
        back_populates="collection_group", cascade="all, delete-orphan"
    )
    snapshots: Mapped[list["CollectionGroupSnapshotModel"]] = relationship(
        back_populates="collection_group", cascade="all, delete-orphan"
    )
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id", ondelete="CASCADE"))
    location: Mapped["LocationModel"] = relationship(back_populates="collections")


class CollectionEventModel(Base):
    """SQLAlchemy: Single event information"""

    __tablename__ = "collection_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    lp_code: Mapped[str] = mapped_column(String(10))

    date: Mapped[datetime]

    morning_start_time: Mapped[time | None] = None
    morning_end_time: Mapped[time | None] = None
    afternoon_start_time: Mapped[time | None] = None
    afternoon_end_time: Mapped[time | None] = None

    # Metadata
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    # Relationships
    collection_group_id: Mapped[int] = mapped_column(ForeignKey("collection_groups.id", ondelete="CASCADE"))
    collection_group: Mapped["CollectionGroupModel"] = relationship(
        back_populates="events"
    )
    snapshots: Mapped[list["ScheduleModel"]] = relationship(
        back_populates="event", cascade="all, delete-orphan"
    )


class CollectionGroupSnapshotModel(Base):
    """SQLAlchemy: Snapshot of stats for an collection group"""

    __tablename__ = "collection_group_snapshots"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    taux_remplissage: Mapped[float | None]

    # Blood slots
    nb_places_restantes_st: Mapped[int | None]
    nb_places_totales_st: Mapped[int | None]
    nb_places_reservees_st: Mapped[int | None]

    # Plasma slots
    nb_places_restantes_pla: Mapped[int | None]
    nb_places_totales_pla: Mapped[int | None]
    nb_places_reservees_pla: Mapped[int | None]

    # Platelet slots
    nb_places_restantes_cpa: Mapped[int | None]
    nb_places_totales_cpa: Mapped[int | None]
    nb_places_reservees_cpa: Mapped[int | None]

    # Metadata
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), index=True
    )

    # Relationships
    collection_group_id: Mapped[int] = mapped_column(ForeignKey("collection_groups.id", ondelete="CASCADE"))
    collection_group: Mapped["CollectionGroupModel"] = relationship(
        back_populates="snapshots"
    )
