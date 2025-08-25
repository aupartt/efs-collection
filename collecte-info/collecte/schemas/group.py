from pydantic import BaseModel, ConfigDict, Field

from collecte.schemas.location import LocationSchema


class GroupSchema(BaseModel):
    """Pydantic: Informations relative to a group of locations"""

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    gr_code: str = Field(alias="grCode")
    gr_lib: str = Field(alias="grLib")
    gr_desd: str | None = Field(alias="grDesd")

    locations: list["LocationSchema"] | None = []

    def info(self) -> dict:
        return self.model_dump(include=["gr_code", "gr_lib", "gr_desd"])
