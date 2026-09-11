from src.reviews.schema import ReviewModel
from src.db.models import Book
from typing import List
from pydantic import Field
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
class UserCreate(BaseModel):
    username: str = Field(min_length=3)
    email: str = Field(min_length=5)
    first_name: str
    last_name: str
    password: str = Field(min_length=6, max_length=40)


class UserModel(BaseModel):
        uuid: UUID
        username: str
        email: str
        first_name: str
        last_name: str
        is_verified: bool
        password_hash: str = Field(exclude=True)
        created_at: datetime
        updated_at: datetime
class UserBookModel(UserModel):
        books:List[Book]
        reviews:List[ReviewModel]
        


class UserLogin(BaseModel):
    email:str
    password:str

class EmailAddresses(BaseModel):
        addresses:List[str]

class PasswordResetRequest(BaseModel):
        email:str

class PasswordResetConfirm(BaseModel):
        new_password:str
        confirm_new_password:str

