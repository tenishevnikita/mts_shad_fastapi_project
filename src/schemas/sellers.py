from typing import List, Optional

from pydantic import BaseModel, EmailStr

from .books import ReturnedBookForSeller


class BaseSeller(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class IncomingSeller(BaseSeller):
    password: str


class ReturnedSeller(BaseSeller):
    id: int

    class Config:
        from_attributes = True


class ReturnedAllSellers(BaseModel):
    sellers: List[ReturnedSeller]


class ReturnedSellerWithBooks(ReturnedSeller):
    books: Optional[List[ReturnedBookForSeller]] = []


class UpdatedSeller(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]

    class Config:
        from_attributes = True
