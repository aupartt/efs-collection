from typing import TYPE_CHECKING, Optional
from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from .location import LocationSchema

class GroupSchema(BaseModel):
    """Pydantic: Informations relative to a group of locations"""
    
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    gr_code: str = Field(alias="grCode")
    gr_lib: str = Field(alias="grLib")
    gr_desd: Optional[str] = Field(alias="grDesd")

    locations: Optional[list["LocationSchema"]] = None
