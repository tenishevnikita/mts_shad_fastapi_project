from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.configurations import get_async_session
from src.schemas import IncomingBook, ReturnedAllBooks, ReturnedBook
from src.service import BookService

books_router = APIRouter(tags=["books"], prefix="/books")


DBSession = Annotated[AsyncSession, Depends(get_async_session)]


@books_router.post("/", response_model=ReturnedBook, status_code=status.HTTP_201_CREATED)
async def create_book(book: IncomingBook, session: DBSession):
    return await BookService.create_book(session=session, book=book)


@books_router.get("/", response_model=ReturnedAllBooks)
async def get_all_books(session: DBSession):
    return await BookService.get_all_books(session=session)


@books_router.get("/{book_id}", response_model=ReturnedBook)
async def get_book(book_id: int, session: DBSession):
    return await BookService.get_book(book_id=book_id, session=session)


@books_router.delete("/{book_id}")
async def delete_book(book_id: int, session: DBSession):
    return await BookService.delete_book(book_id=book_id, session=session)


@books_router.put("/{book_id}")
async def update_book(book_id: int, new_data: IncomingBook, session: DBSession):
    return await BookService.update_book(book_id=book_id, new_data=new_data, session=session)
