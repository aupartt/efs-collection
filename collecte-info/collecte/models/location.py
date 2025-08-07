from typing import TYPE_CHECKING

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
    sampling_location_code: Mapped[str] = mapped_column(String(10), unique=True, index=True)
    group_code: Mapped[str] = mapped_column(String(10), ForeignKey("groups.gr_code"), index=True)
    region_code: Mapped[str] = mapped_column(String(10))

    # Address info
    name: Mapped[str]
    city: Mapped[str]
    post_code: Mapped[str] = mapped_column(String(10), index=True)  # Used for collections lookup
    full_address: Mapped[str]
    address1: Mapped[str]
    address2: Mapped[str]

    # Coordinates
    latitude: Mapped[float]
    longitude: Mapped[float]

    # Services offered
    give_blood: Mapped[bool] = mapped_column(default=False)
    give_plasma: Mapped[bool] = mapped_column(default=False)
    give_platelet: Mapped[bool] = mapped_column(default=False)

    # URLs
    url_blood: Mapped[str]
    url_plasma: Mapped[str]
    url_platelets: Mapped[str]

    # Additional information
    horaires: Mapped[str]
    infos: Mapped[str]
    metro: Mapped[str]
    bus: Mapped[str]
    tram: Mapped[str]
    parking: Mapped[str]
    debut_infos: Mapped[str]
    fin_infos: Mapped[str]
    ville: Mapped[str]
    phone: Mapped[str]

    # Relationships
    group: Mapped["GroupModel"] = relationship(back_populates="locations")
    collections: Mapped[list["CollectionModel"]] = relationship(back_populates="location")
