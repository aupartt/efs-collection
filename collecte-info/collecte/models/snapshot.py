# from datetime import timezone, datetime, timedelta, time
# from typing import Optional, TYPE_CHECKING

# from sqlalchemy import String, event, func, and_, ForeignKey
# from sqlalchemy.orm import Mapped, mapped_column, relationship, Session

# from collecte.models.base import BaseModel
# from collecte.models.collection import CollectionEventModel

# class SnapshotSchedulesModel(BaseModel):
#     """SQLAlchemy: Time series data for schedule availability tracking"""

#     __tablename__ = "crawled_snapshots"
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     url: Mapped[str]
#     efs_id: Mapped[Optional[int]]  # ID from the url
#     crawled_at: Mapped[datetime] = mapped_column(
#         index=True
#     )  # When this data was collected
#     slots: Mapped[int]  # Number of slots available at crawl time
#     schedules: Mapped[dict]  # JSON of schedules at crawl time

#     # Relationships
#     snapshot_id: Mapped[int] = mapped_column(
#         ForeignKey("collection_snapshots.snapshot_id")
#     )
#     snapshot: Mapped["CollectionEventModel"] = relationship(
#         back_populates="snapshots"
#     )
