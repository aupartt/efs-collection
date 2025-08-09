from sqlalchemy import JSON
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs


class BaseModel(DeclarativeBase, AsyncAttrs):
    type_annotation_map = {dict: JSON}
