from uuid import UUID
from src.db.main import get_session
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException,status
from typing import List
from src.books.schema import Book, BookUpdateModel, BookCreateModel,BookDetails
from src.books.services import BookService
from src.auth.dependencies import AccessTokenBearer
from src.auth.dependencies import RoleChecker

from src.errors import(
    BookNotFound
)
roleChecker=Depends(RoleChecker(["admin","user"]))


access_token_bearer=AccessTokenBearer()
# from src.books.books_data import books

from fastapi import APIRouter
book_service=BookService()
book_router=APIRouter()
@book_router.get("/",response_model=List[Book],status_code=status.HTTP_200_OK,dependencies=[roleChecker])
async def get_books(session:AsyncSession=Depends(get_session),token_details:dict=Depends(access_token_bearer))->list:
    # print(token_details)
    books=await book_service.get_books(session)
    return books


@book_router.get("/user/{user_uuid}",response_model=List[Book],status_code=status.HTTP_200_OK,dependencies=[roleChecker])
async def get_user_books(user_uuid:UUID,session:AsyncSession=Depends(get_session),token_details:dict=Depends(access_token_bearer))->list:
    # print(token_details)
   
    books=await book_service.get_user_books(user_uuid,session)
    return books


@book_router.get("/{book_uid}",response_model=BookDetails,status_code=status.HTTP_200_OK,dependencies=[roleChecker])
async def get_book(book_uid:UUID,session:AsyncSession=Depends(get_session),token_details:dict=Depends(access_token_bearer))->dict:
    book=await book_service.get_book(book_uid,session)
    # print(n/0)
    if book:
        return book

    raise BookNotFound() 

# HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book not found")


@book_router.post("/",response_model=Book,status_code=status.HTTP_201_CREATED,dependencies=[roleChecker])
async def create_book(book:BookCreateModel,session:AsyncSession=Depends(get_session),token_details:dict=Depends(access_token_bearer))->dict:
    user_uuid=token_details.get("user")["uuid"]
    book_created=await book_service.create_book(book,user_uuid,session)
    return book_created


@book_router.patch("/{book_uid}",response_model=Book,status_code=status.HTTP_200_OK,dependencies=[roleChecker])
async def update_book(book_uid:UUID,book:BookUpdateModel,session:AsyncSession=Depends(get_session),token_details:dict=Depends(access_token_bearer))->dict:
    book_updated=await book_service.update_book(book_uid,book,session)
    
    if book_updated:
        return book_updated
    raise BookNotFound() 
# HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book not found")



@book_router.delete("/{book_uid}",status_code=status.HTTP_204_NO_CONTENT,dependencies=[roleChecker])
async def delete_book(book_uid:UUID,session:AsyncSession=Depends(get_session),token_details:dict=Depends(access_token_bearer)):
    delete_book=await book_service.delete_book(book_uid,session)

    if delete_book:
        return None
    raise BookNotFound() 
# HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book not found")