from __future__ import annotations

from typing import (
    List,
    Optional,
)

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
)


class InvalidProperties(BaseModel):
    additionalProp1: List[str] = Field(None, description='Key-value pairs of invalid request properties')
    additionalProp2: List[str] = Field(None, description='Key-value pairs of invalid request properties')
    additionalProp3: List[str] = Field(None, description='Key-value pairs of invalid request properties')


class BadRequestError(BaseModel):
    model_config = ConfigDict(extra="forbid")
    message: Optional[str] = None
    invalidProperties: Optional[invalidProperties] = None
