from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class GroupModel(BaseModel):
    gr_code: str = Field(alias="grCode")
    gr_lib: str = Field(alias="grLib")
    gr_desd: Optional[str] = Field(alias="grDesd")

    model_config = ConfigDict(validate_by_name=True)
