from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from collecte.schemas.base import Base


class Group(Base):
    __tablename__ = "groups"

    gr_code = Column(String(10), primary_key=True)
    gr_lib = Column(String(255))
    gr_desd = Column(Text, nullable=True)

    # Relationships
    locations = relationship("Location", back_populates="group")
