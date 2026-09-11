import logging
from fastapi import status
from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import Review
from src.auth.services import UserService
from src.books.services import BookService
from .schema import ReviewCreateModel

user_service=UserService()
book_service=BookService()

class ReviewService:
    async def add_review_to_book(self,user_email:str,book_uuid:str,review_data:ReviewCreateModel,session:AsyncSession):
        try:
            user=await user_service.get_user_by_email(user_email,session)
            book=await book_service.get_book(book_uuid,session)

            if user is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail={"errors":"No user is found..."}
            )

            if book is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail={"errors":"No book is found..."}
            )


            new_review_dump=review_data.model_dump()

            new_review=Review(**new_review_dump)

            new_review.user=user
            new_review.book=book

            session.add(new_review)
            await session.commit()
            return new_review


        except Exception as e:
            logging.exception(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail={"errors":"Opps..."}
            )

       