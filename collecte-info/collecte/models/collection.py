from datetime import datetime, time, timezone
from typing import Optional, TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


from .base import BaseModel
if TYPE_CHECKING:
    from .location import LocationModel
    from .schedule import ScheduleSnapshotModel


class CollectionModel(BaseModel):
    """SQLAlchemy: Collection database model"""

    __tablename__ = "collections"

    id: Mapped[int] = mapped_column(primary_key=True)  # EFS id
    group_code: Mapped[str] = mapped_column(
        String(10), ForeignKey("groups.gr_code"), index=True
    )
    sampling_location_code: Mapped[str] = mapped_column(
        String(10), ForeignKey("locations.sampling_location_code")
    )

    # Date and timing
    date: Mapped[datetime] = mapped_column(index=True)
    morning_start_time: Mapped[Optional[time]]
    morning_end_time: Mapped[Optional[time]]
    afternoon_start_time: Mapped[Optional[time]]
    afternoon_end_time: Mapped[Optional[time]]

    # Collection details
    nature: Mapped[str]
    lp_code: Mapped[str] = mapped_column(String(10))
    is_public: Mapped[bool]
    is_publishable: Mapped[bool]
    propose_planning_rdv: Mapped[bool]

    # Capacity info
    taux_remplissage: Mapped[float]  # Fill rate
    nb_places_restantes_st: Mapped[int]  # Blood remaining slots
    nb_places_totales_st: Mapped[int]  # Blood total slots
    nb_places_reservees_st: Mapped[int]  # Blood reserved slots
    nb_places_restantes_pla: Mapped[int]  # Plasma remaining slots
    nb_places_totales_pla: Mapped[int]  # Plasma total slots
    nb_places_reservees_pla: Mapped[int]  # Plasma reserved slots
    nb_places_restantes_cpa: Mapped[int]  # Platelet remaining slots
    nb_places_totales_cpa: Mapped[int]  # Platelet total slots
    nb_places_reservees_cpa: Mapped[int]  # Platelet reserved slots

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
    location: Mapped["LocationModel"] = relationship(back_populates="collections")
    schedule_snapshots: Mapped[list["ScheduleSnapshotModel"]] = relationship(
        back_populates="collection"
    )
