from datetime import datetime, time, timezone
from typing import Optional, TYPE_CHECKING
from sqlalchemy import DateTime, ForeignKey, UniqueConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from collecte.models.base import BaseModel

if TYPE_CHECKING:
    from .location import LocationModel


class CollectionGroupModel(BaseModel):
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
    efs_id: Mapped[Optional[str]] = mapped_column(
        unique=True, nullable=True, index=True
    )

    # Date
    start_date: Mapped[datetime]
    end_date: Mapped[datetime]

    # Details
    nature: Mapped[Optional[str]]
    is_public: Mapped[bool]
    is_publishable: Mapped[bool]
    propose_planning_rdv: Mapped[bool]

    # URLs
    url_blood: Mapped[Optional[str]]
    url_plasma: Mapped[Optional[str]]
    url_platelet: Mapped[Optional[str]]

    # Text descriptions
    convocation_label_long: Mapped[Optional[str]]
    convocation_label_sms: Mapped[Optional[str]]

    # Metadata
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    events: Mapped[list["CollectionEventModel"]] = relationship(
        back_populates="collection_group", cascade="all, delete-orphan"
    )
    snapshots: Mapped[list["CollectionGroupSnapshotModel"]] = relationship(
        back_populates="collection_group", cascade="all, delete-orphan"
    )
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"))
    location: Mapped["LocationModel"] = relationship(back_populates="collections")


class CollectionEventModel(BaseModel):
    """SQLAlchemy: Single event information"""

    __tablename__ = "collection_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    lp_code: Mapped[str] = mapped_column(String(10))

    date: Mapped[datetime]

    morning_start_time: Mapped[Optional[time]] = None
    morning_end_time: Mapped[Optional[time]] = None
    afternoon_start_time: Mapped[Optional[time]] = None
    afternoon_end_time: Mapped[Optional[time]] = None

    # Metadata
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    collection_group_id: Mapped[int] = mapped_column(ForeignKey("collection_groups.id"))
    collection_group: Mapped["CollectionGroupModel"] = relationship(
        back_populates="events"
    )


class CollectionGroupSnapshotModel(BaseModel):
    """SQLAlchemy: Snapshot of stats for an collection group"""

    __tablename__ = "collection_group_snapshots"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    taux_remplissage: Mapped[Optional[float]]

    # Blood slots
    nb_places_restantes_st: Mapped[Optional[int]]
    nb_places_totales_st: Mapped[Optional[int]]
    nb_places_reservees_st: Mapped[Optional[int]]

    # Plasma slots
    nb_places_restantes_pla: Mapped[Optional[int]]
    nb_places_totales_pla: Mapped[Optional[int]]
    nb_places_reservees_pla: Mapped[Optional[int]]

    # Platelet slots
    nb_places_restantes_cpa: Mapped[Optional[int]]
    nb_places_totales_cpa: Mapped[Optional[int]]
    nb_places_reservees_cpa: Mapped[Optional[int]]

    # Metadata
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True
    )

    # Relationships
    collection_group_id: Mapped[int] = mapped_column(ForeignKey("collection_groups.id"))
    collection_group: Mapped["CollectionGroupModel"] = relationship(
        back_populates="snapshots"
    )
