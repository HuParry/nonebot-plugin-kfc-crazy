from pydantic import BaseModel, Field


class Config(BaseModel):
    kfc_crazy_group_ids: set[int] = Field(default_factory=set)
