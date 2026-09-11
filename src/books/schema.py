from src.reviews.schema import ReviewModel
from src.tags.schemas import TagModel

from typing import List
from typing import Optional
from pydantic import BaseModel
from uuid import UUID, uuid4
from datetime import datetime, date
class Book(BaseModel):
        uuid: UUID
        title: str
        author: str
        published_date: date
        genre: str
        price: float
        user_uuid: Optional[UUID] = None
        created_at: datetime
        updated_at: datetime


class BookDetails(Book):
        reviews:List[ReviewModel]
        tags:List[TagModel]
        



class BookCreateModel(BaseModel):
        title:str
        author:str
        published_date: str
        genre: str 
        price: float


class BookUpdateModel(BaseModel):
        title:str
        author:str
        genre: str 
        price: float