from fastapi import Response, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.models import Seller
from src.schemas import IncomingSeller, ReturnedAllSellers, ReturnedSeller, ReturnedSellerWithBooks, UpdatedSeller
from src.utils import DBSession


class SellerService:
    @staticmethod
    async def create_seller(seller: IncomingSeller, session: DBSession) -> ReturnedSeller:
        new_seller = Seller(
            first_name=seller.first_name,
            last_name=seller.last_name,
            email=seller.email,
            password=seller.password,
        )
        session.add(new_seller)

        await session.flush()

        return ReturnedSeller.from_orm(new_seller)

    @staticmethod
    async def get_all_sellers(session: DBSession) -> ReturnedAllSellers | Response:
        query = select(Seller)
        res = await session.execute(query)
        sellers = res.scalars().all()

        if not sellers:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        sellers_response = [ReturnedSeller.from_orm(seller) for seller in sellers]
        return ReturnedAllSellers(sellers=sellers_response)

    @staticmethod
    async def get_seller(seller_id: int, session: DBSession) -> ReturnedSellerWithBooks | Response:
        res = await session.execute(select(Seller).where(Seller.id == seller_id).options(selectinload(Seller.books)))
        seller = res.scalars().first()
        if not seller:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        return ReturnedSellerWithBooks.from_orm(seller)

    @staticmethod
    async def delete_seller(seller_id: int, session: DBSession) -> Response:
        deleted_seller = await session.get(Seller, seller_id)
        if not deleted_seller:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        await session.delete(deleted_seller)
        await session.flush()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    @staticmethod
    async def update_seller(seller_id: int, new_data: UpdatedSeller, session: DBSession) -> ReturnedSeller | Response:
        updated_seller = await session.get(Seller, seller_id)
        if not updated_seller:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        for field_name, value in new_data.dict(exclude_unset=True).items():
            setattr(updated_seller, field_name, value)

        await session.flush()
        return ReturnedSeller.from_orm(updated_seller)
