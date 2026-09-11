from uuid import UUID
from .schema import ReviewModel,ReviewCreateModel
from fastapi import status
from src.db.models import User
from src.db.main import get_session
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import APIRouter
from .services import ReviewService
from src.auth.dependencies import current_user
reviewService=ReviewService()
review_router=APIRouter()

@review_router.post("/books/{book_uuid}", response_model=ReviewModel, status_code=status.HTTP_200_OK)
async def add_review_to_book(
    book_uuid: UUID,
    review_data: ReviewCreateModel,
    current_user: User = Depends(current_user),
    session: AsyncSession = Depends(get_session),
):
    new_review = await reviewService.add_review_to_book(
        user_email=current_user.email,
        review_data=review_data,
        book_uuid=book_uuid,
        session=session,
    )
    return new_review


