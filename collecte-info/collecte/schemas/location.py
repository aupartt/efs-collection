from sqlalchemy import Column, Integer, String, Boolean, Numeric, JSON, ForeignKey, Text
from sqlalchemy.orm import relationship

from collecte.schemas.base import Base


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sampling_location_code = Column(String(20), unique=True, index=True)
    group_code = Column(String(10), ForeignKey("groups.gr_code"), index=True)
    region_code = Column(String(10))

    # Address info
    name = Column(String(255))
    city = Column(String(100))
    post_code = Column(String(10), index=True)  # Used for collections lookup
    full_address = Column(Text)
    address1 = Column(String(255))
    address2 = Column(String(255))

    # Coordinates
    latitude = Column(Numeric(10, 8))
    longitude = Column(Numeric(11, 8))

    # Services offered
    give_blood = Column(Boolean, default=False)
    give_plasma = Column(Boolean, default=False)
    give_platelet = Column(Boolean, default=False)

    # Additional info (JSON fields for flexibility)
    transport_info = Column(JSON)  # metro, bus, tram, parking
    schedule_info = Column(JSON)  # horaires, infos, debut/fin infos
    contact_info = Column(JSON)  # phone, ville, id
    urls = Column(JSON)  # urlBlood, urlPlasma, urlPlatelets

    # Relationships
    group = relationship("Group", back_populates="locations")
    collections = relationship("Collection", back_populates="location")
