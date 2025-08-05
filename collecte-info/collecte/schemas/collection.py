from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Date,
    Time,
    Numeric,
    ForeignKey,
    Text,
    Index,
)
from sqlalchemy.orm import relationship

from collecte.schemas.base import Base


class Collection(Base):
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True)  # EFS collection ID
    group_code = Column(String(10), ForeignKey("groups.gr_code"), index=True)
    sampling_location_code = Column(
        String(20), ForeignKey("locations.sampling_location_code")
    )

    # Date and timing
    date = Column(Date, index=True)
    morning_start_time = Column(Time)
    morning_end_time = Column(Time)
    afternoon_start_time = Column(Time)
    afternoon_end_time = Column(Time)

    # Collection details
    nature = Column(String(100))
    lp_code = Column(String(10))
    is_public = Column(Boolean, default=True)
    is_publishable = Column(Boolean, default=True)
    propose_planning_rdv = Column(Boolean, default=False)

    # Capacity info
    taux_remplissage = Column(Numeric(5, 4))  # Fill rate
    nb_places_restantes_st = Column(Integer)  # Blood remaining slots
    nb_places_totales_st = Column(Integer)  # Blood total slots
    nb_places_reservees_st = Column(Integer)  # Blood reserved slots
    nb_places_restantes_pla = Column(Integer)  # Plasma remaining slots
    nb_places_totales_pla = Column(Integer)  # Plasma total slots
    nb_places_reservees_pla = Column(Integer)  # Plasma reserved slots
    nb_places_restantes_cpa = Column(Integer)  # Platelet remaining slots
    nb_places_totales_cpa = Column(Integer)  # Platelet total slots
    nb_places_reservees_cpa = Column(Integer)  # Platelet reserved slots

    # URLs for booking
    url_blood = Column(String(255))
    url_plasma = Column(String(255))
    url_platelet = Column(String(255))

    # Text descriptions
    convocation_label_long = Column(Text)
    convocation_label_sms = Column(Text)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    location = relationship("Location", back_populates="collections")
    schedule_snapshots = relationship("ScheduleSnapshot", back_populates="collection")

    # Indexes for common queries
    __table_args__ = (
        Index("ix_collections_date_group", "date", "group_code"),
        Index("ix_collections_date_location", "date", "sampling_location_code"),
    )
