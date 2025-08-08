from sqlalchemy import JSON
from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    type_annotation_map = {dict: JSON}
