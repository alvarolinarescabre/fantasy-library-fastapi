from beanie import Document
from pydantic import BaseModel
from typing import Optional

class BookModel(Document):
    title: str
    author: str
    genre: str
    publish_date: str
    isbn: int

    class Settings:
        name = "fantasy_library_collection"

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "lotr": {
                "title": "The Lord of the Ring",
                "author": "J.R.R Tolkien",
                "genre": "Fantasy",
                "publish_date": "29/07/1954",
                "isbn": 9780395647387
            }
        }

class UpdateBookModel(BaseModel):
    title: Optional[str]
    author: Optional[str]
    genre: Optional[str]
    publish_date: Optional[str]
    isbn: Optional[int]

    class Config:
        json_schema_extra = {
            "lotr": {
                "title": "The Hobbit",
                "author": "J.R.R Tolkien",
                "genre": "Fantasy",
                "publish_date": "21/09/1937",
                "isbn": 9780007525508
            }
        }

def response_model(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }

def error_response_model(error, code, message):
    return {"error": error, "code": code, "message": message}