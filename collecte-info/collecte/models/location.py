from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from collecte.models.base import Base

from .collection import CollectionGroupModel

if TYPE_CHECKING:
    from .group import GroupModel


class LocationModel(Base):
    """SQLAlchemy: Location database model"""

    __tablename__ = "locations"
    __table_args__ = (
        UniqueConstraint(
            "name",
            "full_address",
            "latitude",
            "longitude",
            "sampling_location_code",
            name="unique_location",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sampling_location_code: Mapped[str] = mapped_column(String(10))
    region_code: Mapped[str | None] = mapped_column(String(10))

    # Address info
    name: Mapped[str | None]
    city: Mapped[str | None]
    post_code: Mapped[str] = mapped_column(
        String(10), index=True
    )  # Used for collections lookup
    full_address: Mapped[str]
    address1: Mapped[str | None]
    address2: Mapped[str | None]

    # Coordinates
    latitude: Mapped[float]
    longitude: Mapped[float]

    # Services offered
    give_blood: Mapped[bool] = mapped_column(default=False)
    give_plasma: Mapped[bool] = mapped_column(default=False)
    give_platelet: Mapped[bool] = mapped_column(default=False)

    # Additional information
    horaires: Mapped[str | None]
    infos: Mapped[str | None]
    metro: Mapped[str | None]
    bus: Mapped[str | None]
    tram: Mapped[str | None]
    parking: Mapped[str | None]
    debut_infos: Mapped[str | None]
    fin_infos: Mapped[str | None]
    ville: Mapped[str | None]
    phone: Mapped[str | None]

    # Relationships
    group_code: Mapped[str] = mapped_column(
        String(10), ForeignKey("groups.gr_code"), index=True
    )
    group: Mapped["GroupModel"] = relationship(back_populates="locations")
    collections: Mapped[list["CollectionGroupModel"]] = relationship(
        back_populates="location", cascade="all, delete-orphan"
    )
