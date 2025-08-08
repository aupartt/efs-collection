from typing import TYPE_CHECKING, Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel

if TYPE_CHECKING:
    from .group import GroupModel
    from .collection import CollectionModel


class LocationModel(BaseModel):
    """SQLAlchemy: Location database model"""

    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sampling_location_code: Mapped[str] = mapped_column(String(10))
    region_code: Mapped[str] = mapped_column(String(10))

    # Address info
    name: Mapped[Optional[str]]
    city: Mapped[Optional[str]]
    post_code: Mapped[str] = mapped_column(
        String(10), index=True
    )  # Used for collections lookup
    full_address: Mapped[str]
    address1: Mapped[Optional[str]]
    address2: Mapped[Optional[str]]

    # Coordinates
    latitude: Mapped[float]
    longitude: Mapped[float]

    # Services offered
    give_blood: Mapped[bool] = mapped_column(default=False)
    give_plasma: Mapped[bool] = mapped_column(default=False)
    give_platelet: Mapped[bool] = mapped_column(default=False)

    # Additional information
    horaires: Mapped[Optional[str]]
    infos: Mapped[Optional[str]]
    metro: Mapped[Optional[str]]
    bus: Mapped[Optional[str]]
    tram: Mapped[Optional[str]]
    parking: Mapped[Optional[str]]
    debut_infos: Mapped[Optional[str]]
    fin_infos: Mapped[Optional[str]]
    ville: Mapped[Optional[str]]
    phone: Mapped[Optional[str]]

    # Relationships
    group_code: Mapped[str] = mapped_column(
        String(10), ForeignKey("groups.gr_code"), index=True
    )
    group: Mapped["GroupModel"] = relationship(back_populates="locations")
    collections: Mapped[list["CollectionModel"]] = relationship(
        back_populates="location"
    )
