import pytest
from fastapi import status
from sqlalchemy import select

from src.models import Book, Seller


@pytest.mark.asyncio
async def test_create_book(db_session, async_client):
    seller_1 = Seller(first_name="Nikita", last_name="Tenishev", email="nik.tenishev@gmail.com", password="12345")
    db_session.add(seller_1)
    await db_session.flush()

    book = {"title": "Капитанская дочка", "author": "А.С. Пушкин", "pages": 500, "year": 2024, "seller_id": seller_1.id}

    response = await async_client.post("/api/v1/books/", json=book)

    assert response.status_code == status.HTTP_201_CREATED

    result_data = response.json()

    assert result_data["id"] == 1
    assert result_data["title"] == book["title"]
    assert result_data["author"] == book["author"]
    assert result_data["count_pages"] == book["pages"]
    assert result_data["year"] == book["year"]
    assert result_data["seller_id"] == seller_1.id


@pytest.mark.asyncio
async def test_get_books(db_session, async_client):
    seller_1 = Seller(first_name="Nikita", last_name="Tenishev", email="nik.tenishev@gmail.com", password="12345")
    db_session.add(seller_1)
    await db_session.flush()

    book1 = Book(author="А.С. Пушкин", title="Евгений Онегин", year=2000, count_pages=350, seller_id=seller_1.id)
    book2 = Book(author="Л.Н. Толстой", title="Война и мир", year=1990, count_pages=1000, seller_id=seller_1.id)

    db_session.add_all([book1, book2])
    await db_session.flush()

    response = await async_client.get("/api/v1/books/")

    assert response.status_code == status.HTTP_200_OK

    assert len(response.json()["books"]) == 2

    assert response.json() == {
        "books": [
            {
                "title": book1.title,
                "author": book1.author,
                "year": book1.year,
                "id": book1.id,
                "count_pages": book1.count_pages,
                "seller_id": seller_1.id,
            },
            {
                "title": book2.title,
                "author": book2.author,
                "year": book2.year,
                "id": book2.id,
                "count_pages": book2.count_pages,
                "seller_id": seller_1.id,
            },
        ]
    }


@pytest.mark.asyncio
async def test_get_single_book(db_session, async_client):
    seller_1 = Seller(first_name="Nikita", last_name="Tenishev", email="nik.tenishev@gmail.com", password="12345")
    db_session.add(seller_1)
    await db_session.flush()

    book1 = Book(author="А.С. Пушкин", title="Евгений Онегин", year=2000, count_pages=350, seller_id=seller_1.id)
    book2 = Book(author="Л.Н. Толстой", title="Война и мир", year=1990, count_pages=1000, seller_id=seller_1.id)

    db_session.add_all([book1, book2])
    await db_session.flush()

    response = await async_client.get(f"/api/v1/books/{book1.id}")

    assert response.status_code == status.HTTP_200_OK

    assert response.json() == {
        "title": book1.title,
        "author": book1.author,
        "year": book1.year,
        "id": book1.id,
        "count_pages": book1.count_pages,
        "seller_id": seller_1.id,
    }


@pytest.mark.asyncio
async def test_delete_book(db_session, async_client):
    seller_1 = Seller(first_name="Nikita", last_name="Tenishev", email="nik.tenishev@gmail.com", password="12345")
    db_session.add(seller_1)
    await db_session.flush()

    book = Book(author="А.С. Пушкин", title="Евгений Онегин", year=2000, count_pages=350, seller_id=seller_1.id)
    db_session.add(book)
    await db_session.flush()

    response = await async_client.delete(f"/api/v1/books/{book.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    await db_session.flush()

    all_books = await db_session.execute(select(Book))
    res = all_books.scalars().all()
    assert len(res) == 0


@pytest.mark.asyncio
async def test_update_book(db_session, async_client):
    seller_1 = Seller(first_name="Nikita", last_name="Tenishev", email="nik.tenishev@gmail.com", password="12345")
    db_session.add(seller_1)
    await db_session.flush()

    book = Book(author="А.С. Пушкин", title="Евгений Онегин", year=2000, count_pages=350, seller_id=seller_1.id)
    db_session.add(book)
    await db_session.flush()

    new_book = {
        "author": "Л.Н. Толстой",
        "title": "Война и мир",
        "pages": 1000,
        "year": 1990,
        "id": book.id,
        "seller_id": seller_1.id,
    }

    response = await async_client.put(f"/api/v1/books/{book.id}", json=new_book)

    assert response.status_code == status.HTTP_200_OK
    await db_session.flush()

    res = await db_session.get(Book, book.id)
    assert res.title == new_book["title"]
    assert res.author == new_book["author"]
    assert res.count_pages == new_book["pages"]
    assert res.year == new_book["year"]
    assert res.id == new_book["id"]
    assert res.seller_id == new_book["seller_id"]
