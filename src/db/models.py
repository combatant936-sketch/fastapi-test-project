from typing import List
from sqlmodel import Relationship
from typing import Optional
from datetime import datetime,date
from sqlmodel import SQLModel,Field,Column
from uuid import UUID, uuid4

import sqlalchemy.dialects.postgresql as pg

class BookTag(SQLModel, table=True):
    book_id: UUID = Field(default=None, foreign_key="books.uuid", primary_key=True)
    tag_id: UUID = Field(default=None, foreign_key="tags.uuid", primary_key=True)


class Book(SQLModel,table=True):
        __tablename__= "books"
        uuid:UUID=Field(sa_column=Column(
            pg.UUID,
            primary_key=True,
            nullable=False,
            default=uuid4

        ))
        title:str
        author:str
        published_date: date
        user:Optional["User"]=Relationship(back_populates="books")
        user_uuid:Optional[UUID]=Field(default=False,foreign_key="users.uuid")
        reviews:List["Review"]=Relationship(back_populates="book",sa_relationship_kwargs={"lazy":"selectin"})
        tags:List["Tag"]=Relationship(link_model=BookTag,back_populates="books",sa_relationship_kwargs={"lazy":"selectin"})

        genre: str 
        price: float
        created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
        updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

        def __repr__(self):

            return f"Title is {self.title}"


class User(SQLModel,table=True):
        __tablename__= "users"
        uuid:UUID=Field(sa_column=Column(
            pg.UUID,
            primary_key=True,
            nullable=False,
            default=uuid4

        ))
        username:str
        email:str
        first_name:str
        books:List["Book"]=Relationship(back_populates="user",sa_relationship_kwargs={"lazy":"selectin"})

        reviews:List["Review"]=Relationship(back_populates="user",sa_relationship_kwargs={"lazy":"selectin"})

        last_name: str
        role:str =Field(sa_column=Column(pg.VARCHAR,nullable=False,server_default="user"))
        is_verified:bool=Field(default=False)
        password_hash:str=Field(exclude=True)
        created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
        updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

        def __repr__(self):

            return f"Title is {self.username}"


class Tag(SQLModel, table=True):
    __tablename__ = "tags"
    uuid: UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid4)
    )
    name: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    books: List["Book"] = Relationship(
        link_model=BookTag,
        back_populates="tags",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    def __repr__(self) -> str:
        return f"<Tag {self.name}>"


class Review(SQLModel,table=True):
        __tablename__= "reviews"
        uuid:UUID=Field(sa_column=Column(
            pg.UUID,
            primary_key=True,
            nullable=False,
            default=uuid4

        ))
        rating:int=Field(ge=1, le=5)
        review_text:str
        user_uuid:Optional[UUID]=Field(default=False,foreign_key="users.uuid")
        book_uuid:Optional[UUID]=Field(default=False,foreign_key="books.uuid")
        
        user:Optional[User]=Relationship(back_populates="reviews")
        book:Optional[Book]=Relationship(back_populates="reviews")



        created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
        updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

        def __repr__(self):

            return f"Review for book {self.book_uuid} by the user {self.user_uuid}"






