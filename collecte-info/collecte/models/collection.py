from datetime import datetime, time, timezone
from typing import Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


from .base import BaseModel

if TYPE_CHECKING:
    from .location import LocationModel
    from .snapshot import SnapshotCollectionModel


class CollectionModel(BaseModel):
    """SQLAlchemy: Collection database model"""

    __tablename__ = "collections"

    id: Mapped[int] = mapped_column(primary_key=True)
    efs_id: Mapped[int] = mapped_column(unique=True)  # ID from the url

    # Date and timing
    date_start: Mapped[datetime] = mapped_column(index=True)
    date_end: Mapped[datetime] = mapped_column(index=True)
    morning_start_time_min: Mapped[Optional[time]]
    morning_end_time_max: Mapped[Optional[time]]
    afternoon_start_time_min: Mapped[Optional[time]]
    afternoon_end_time_max: Mapped[Optional[time]]

    # Collection details
    nature: Mapped[str]
    is_public: Mapped[bool]
    is_publishable: Mapped[bool]
    propose_planning_rdv: Mapped[bool]

    # URLs for booking
    url_blood: Mapped[str]
    url_plasma: Mapped[str]
    url_platelet: Mapped[str]

    # Text descriptions
    convocation_label_long: Mapped[str]
    convocation_label_sms: Mapped[str]

    # Metadata
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc)
    )

    # Relationships
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"))
    location: Mapped["LocationModel"] = relationship(back_populates="collections")
    snapshots: Mapped[list["SnapshotCollectionModel"]] = relationship(
        back_populates="collection"
    )
