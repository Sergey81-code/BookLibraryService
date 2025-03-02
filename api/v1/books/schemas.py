from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, field_validator, model_validator

from api.core.exceptions import AppExceptions

class TundeModel(BaseModel):
    class ConfigDict:
        from_attributes = True

class Author(BaseModel):
    id: UUID

class ShowBook(TundeModel):
    id: UUID
    name: str
    desc: Optional[str] = None
    url: Optional[str] = None
    year: int
    totalAmount: int
    borrowedAmount: int
    authors: list[Author]


class BookCreate(BaseModel):
    name: str
    desc: Optional[str] = None
    url: Optional[str] = None
    year: int
    totalAmount: int = Field(gt=0, description="Total amount must be greater than 0")
    borrowedAmount: int = Field(ge=0, description="Borrowed amount must be non-negative")
    authors: list[Author] = []

    @model_validator(mode="before")
    def capitalize_name(cls, values):
        if "name" in values:
            values['name'] = values['name'].capitalize()
        return values
        

    @field_validator("borrowedAmount")
    def validate_borrowed_amount(cls, value, info):
        total_amount = info.data.get('totalAmount')
        if total_amount is not None and value > total_amount:
            AppExceptions.bad_request_exception("borrowedAmount cannot be greater than totalAmount")
        return value


class BookUpdate(BaseModel):
    name: Optional[str] = None
    desc: Optional[str] = None
    url: Optional[str] = None
    year: Optional[int] = None
    totalAmount: Optional[int] = Field(None, gt=0, description="Total amount must be greater than 0")
    borrowedAmount: Optional[int] = Field(None, ge=0, description="Borrowed amount must be non-negative")
    authors: Optional[list[Author]] = []

    @model_validator(mode="before")
    def capitalize_name(cls, values):
        if "name" in values:
            values['name'] = values['name'].capitalize()
        return values
        


    @field_validator("borrowedAmount")
    def validate_borrowed_amount(cls, value, values):
        total_amount = values.data.get('totalAmount')
        if total_amount is not None and value > total_amount:
            AppExceptions.bad_request_exception("borrowedAmount cannot be greater than totalAmount")
        return value