from sqlmodel import desc
from sqlmodel import select
from .schema import BookUpdateModel, BookCreateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import Book
from datetime import datetime
class BookService:
    async def get_books(self,session:AsyncSession):
        statement=select(Book).order_by(desc(Book.created_at))
        result=await session.exec(statement)
        return result.all()
    
    async def get_user_books(self,user_uuid,session:AsyncSession):
        statement=select(Book).where(Book.user_uuid==user_uuid).order_by(desc(Book.created_at))
        result=await session.exec(statement)
        return result.all()

    async def get_book(self,book_uuid:str,session:AsyncSession):
        statement=select(Book).where(Book.uuid==book_uuid)
        result=await session.exec(statement)
        return result.first()
        
    
    async def create_book(self,book_data:BookCreateModel,user_uuid,session:AsyncSession):
        book_to_create_dict=book_data.model_dump()
        new_book=Book(**book_to_create_dict) 
        new_book.published_date=datetime.strptime(book_to_create_dict["published_date"],"%Y-%m-%d")
        new_book.user_uuid=user_uuid
        session.add(new_book)
        await session.commit()
        return new_book
        

    async def update_book(self,book_uuid:str,update_data:BookUpdateModel,session:AsyncSession):
        book_to_update=await self.get_book(book_uuid,session)
        
        if book_to_update is not None:
            book_to_update_dict=update_data.model_dump()

            for k, v in book_to_update_dict.items():
                setattr(book_to_update ,k,v)
            await session.commit()

            return book_to_update
        return None

    
    async def delete_book(self,book_uuid:str,session:AsyncSession):
        book_to_delete=await self.get_book(book_uuid,session)
        
        if book_to_delete is not None:
            await session.delete(book_to_delete)
            await session.commit()
            
            return {}
        return None