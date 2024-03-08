from pydantic import BaseModel, Field, field_validator
from pydantic_core import PydanticCustomError


class BaseBook(BaseModel):
    title: str
    author: str
    year: int


class BaseWithSeller(BaseModel):
    seller_id: int


class IncomingBook(BaseBook, BaseWithSeller):
    year: int = 2024
    count_pages: int = Field(alias="pages", default=300)

    @field_validator("year")
    @staticmethod
    def validate_year(val: int):
        if val < 1900:
            raise PydanticCustomError("Validation error", "Year is wrong!")
        return val


class ReturnedBook(BaseBook, BaseWithSeller):
    id: int
    count_pages: int

    class Config:
        from_attributes = True


class ReturnedBookForSeller(ReturnedBook):
    seller_id: int = Field(exclude=True)


class ReturnedAllBooks(BaseModel):
    books: list[ReturnedBook]
