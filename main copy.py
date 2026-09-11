from fastapi import Header,FastAPI
from pydantic import BaseModel
from typing import Optional


app=FastAPI()

@app.get("/")
async def get():
    return {"message":"hello"}

@app.get("/greetings-with-path-parameter/{name}")
async def greetings(name:str):
    return {"message":f"Hello {name}"}


@app.get("/greetings-with-path-parameter-and-query-parameter/{name}")
async def greetings(name:str,symbol:int):
    return {"message":f"Hello {name} and symbol is {symbol}"}


@app.get("/greetings-with-path-parameter-and-optional-query-parameter/{name}")
async def greetings(name:str,symbol:Optional[int]=0):
    return {"message":f"Hello {name} and symbol is {symbol}"}

class CreateBook(BaseModel):
    title:str
    author:str

@app.post("/create-book",status_code=201)
async def create_book(book:CreateBook)->dict:
    return {"title":book.title,"author":book.author}


@app.get("/get-headers")
async def get_headers(accept:str=Header(default=None),content_type:str=Header(None),host:str=Header(None),user_agent:str=Header(None))->dict:
    
    request_headers={}

    request_headers["Accept"]=accept
    request_headers["Host"]=host
    request_headers["User-Agent"]=user_agent

    
    request_headers["Content-Type"]=content_type


    
    return request_headers
    
    