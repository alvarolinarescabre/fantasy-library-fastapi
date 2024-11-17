from typing import Optional
from pydantic import BaseModel, Field, constr, conint, create_model


class SchemaBook(BaseModel):
    title: constr(strict=True) = Field(...)
    author: constr(strict=True) = Field(...)
    genre: constr(strict=True) = Field(...)
    publish_date: constr(strict=True) = Field(...)
    isbn: conint(strict=True) = Field(...)

    class Config:
        json_schema_extra = {
            "lotr": {
                "title": "The Lord of the Ring",
                "author": "J.R.R Tolkien",
                "genre": "Fantasy",
                "publish_date": "29/07/1954",
                "isbn": 9780395647387
            }
        }

    @classmethod
    def as_optional(cls):
        annotations = cls.model_fields
        fields = {
            attribute: (Optional[data_type.type_], None)
            for attribute, data_type in annotations.items()
        }
        OptionalModel = create_model(f"Optional{cls.__name__}", **fields)
        return OptionalModel

class UpdateBookModel(BaseModel):
    title: constr(strict=True)
    author: constr(strict=True)
    genre: constr(strict=True)
    publish_date: constr(strict=True)
    isbn: conint(strict=True)

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

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }

def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}