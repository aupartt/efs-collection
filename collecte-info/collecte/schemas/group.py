from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class GroupSchema(BaseModel):
    """Pydantic: Informations relative to a group of locations"""
    gr_code: str = Field(alias="grCode")
    gr_lib: str = Field(alias="grLib")
    gr_desd: Optional[str] = Field(alias="grDesd")

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)
