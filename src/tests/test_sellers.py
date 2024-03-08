import pytest
from fastapi import status
from sqlalchemy import select

from src.models import Book, Seller


@pytest.mark.asyncio
async def test_create_seller(async_client, db_session):
    seller_data = {
        "first_name": "Nikita",
        "last_name": "Tenishev",
        "email": "nik.tenishev@gmail.com",
        "password": "12345",
    }

    response = await async_client.post("/api/v1/seller/", json=seller_data)

    assert response.status_code == status.HTTP_201_CREATED

    result_data = response.json()

    assert result_data["first_name"] == seller_data["first_name"]
    assert result_data["last_name"] == seller_data["last_name"]
    assert result_data["email"] == seller_data["email"]


@pytest.mark.asyncio
async def test_get_sellers(db_session, async_client):
    seller_1 = Seller(first_name="Nikita", last_name="Tenishev", email="nik.tenishev@gmail.com", password="12345")
    seller_2 = Seller(first_name="Ivan", last_name="Ivanov", email="ivanov.ivan@gmail.com", password="54321")
    db_session.add_all([seller_1, seller_2])
    await db_session.flush()

    response = await async_client.get("/api/v1/seller/")

    assert response.status_code == status.HTTP_200_OK

    assert len(response.json()["sellers"]) == 2

    assert response.json() == {
        "sellers": [
            {
                "first_name": seller_1.first_name,
                "last_name": seller_1.last_name,
                "email": seller_1.email,
                "id": seller_1.id,
            },
            {
                "first_name": seller_2.first_name,
                "last_name": seller_2.last_name,
                "email": seller_2.email,
                "id": seller_2.id,
            },
        ]
    }


@pytest.mark.asyncio
async def test_get_single_seller(db_session, async_client):
    seller_1 = Seller(first_name="Nikita", last_name="Tenishev", email="nik.tenishev@gmail.com", password="12345")
    seller_2 = Seller(first_name="Ivan", last_name="Ivanov", email="ivanov.ivan@gmail.com", password="54321")
    db_session.add_all([seller_1, seller_2])
    await db_session.flush()

    book = Book(author="А.С. Пушкин", title="Евгений Онегин", year=2000, count_pages=350, seller_id=seller_1.id)
    db_session.add_all([book])
    await db_session.flush()

    response = await async_client.get(f"/api/v1/seller/{seller_1.id}")

    assert response.status_code == status.HTTP_200_OK

    assert response.json() == {
        "id": seller_1.id,
        "first_name": seller_1.first_name,
        "last_name": seller_1.last_name,
        "email": seller_1.email,
        "books": [
            {
                "title": book.title,
                "author": book.author,
                "year": book.year,
                "id": book.id,
                "count_pages": book.count_pages,
            }
        ],
    }


@pytest.mark.asyncio
async def test_delete_seller(db_session, async_client):
    seller_1 = Seller(first_name="Nikita", last_name="Tenishev", email="nik.tenishev@gmail.com", password="12345")
    db_session.add(seller_1)
    await db_session.flush()

    response = await async_client.delete(f"/api/v1/seller/{seller_1.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    await db_session.flush()

    all_books = await db_session.execute(select(Book))
    res = all_books.scalars().all()
    assert len(res) == 0


@pytest.mark.asyncio
async def test_update_seller(db_session, async_client):
    seller_1_data = {
        "first_name": "Nikita",
        "last_name": "Tenishev",
        "email": "nik.tenishev@gmail.com",
        "password": "12345",
    }
    seller_1 = Seller(**seller_1_data)
    db_session.add(seller_1)
    await db_session.flush()

    seller_1_new_data = {"first_name": "Ivan", "last_name": "Ivanov", "email": "ivanov.ivan@gmail.com"}

    response = await async_client.put(f"/api/v1/seller/{seller_1.id}", json=seller_1_new_data)

    assert response.status_code == status.HTTP_200_OK
    await db_session.flush()

    res = await db_session.get(Seller, seller_1.id)
    assert res.first_name == seller_1_new_data["first_name"]
    assert res.last_name == seller_1_new_data["last_name"]
    assert res.email == seller_1_new_data["email"]
    assert res.id == seller_1.id
