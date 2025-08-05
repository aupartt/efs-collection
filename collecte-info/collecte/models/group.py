from typing import Optional
from pydantic import BaseModel, Field


class GroupModel(BaseModel):
    gr_code: str = Field(alias="grCode")
    gr_lib: str = Field(alias="grLib")
    gr_desd: Optional[str] = Field(alias="grDesd")

    class Config:
        allow_population_by_field_name = True
