from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel

if TYPE_CHECKING:
    from . import LocationModel


class GroupModel(BaseModel):
    """SQLAlchemy: Group database model"""

    __tablename__ = "groups"

    gr_code: Mapped[str] = mapped_column(String(10), primary_key=True)
    gr_lib: Mapped[str]
    gr_desd: Mapped[str] = mapped_column(nullable=True)

    # Relationships
    locations: Mapped[list["LocationModel"]] = relationship(back_populates="group")
