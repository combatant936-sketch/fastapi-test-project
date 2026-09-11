

from datetime import datetime
from typing import Optional
from pydantic import Field
from uuid import UUID
from pydantic import BaseModel
class ReviewModel(BaseModel):
        uuid:UUID
        rating:int=Field(ge=1, le=5)
        review_text:str
        user_uuid:Optional[UUID]
        book_uuid:Optional[UUID]
        created_at: datetime
        updated_at: datetime

class ReviewCreateModel(BaseModel):
        rating:int=Field(ge=1, le=5)
        review_text:str