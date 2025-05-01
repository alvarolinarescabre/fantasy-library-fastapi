import secrets
import beanie.exceptions
from typing import Annotated, List

import pymongo
from beanie import PydanticObjectId
from fastapi import HTTPException, status
from fastapi.params import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from fastapi import APIRouter, Body

from ..models.model import (
    error_response_model,
    response_model,
    BookModel,
    UpdateBookModel,
)

security = HTTPBasic()
router = APIRouter()

def get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"chamo"
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"chamo"
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@router.post("/")
async def added_book(book: BookModel = Body(...), username: str = Depends(get_current_username)):
    try:
        await book.create()
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(409, "Book exists")

    return {"message": "Book added successfully."}

@router.get("/", response_description="Books records retrieved")
async def get_books(username: str = Depends(get_current_username)):
    books = await BookModel.find_all().to_list()

    if not books:
        raise HTTPException(
            status_code=404,
            detail="Books records not found!"
        )

    return books
@router.get("/{id}", response_description="Book record retrieved")
async def get_book(id: PydanticObjectId, username: str = Depends(get_current_username))  -> BookModel:
    book = await BookModel.get(id)

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book record not found!"
        )

    return book
@router.put("/{id}", response_description="Book record updated")
async def updated_book(id: PydanticObjectId, req: UpdateBookModel, username: str = Depends(get_current_username)) -> BookModel:
    req = {k: v for k, v in req.model_dump().items() if v is not None}

    update_query = {"$set": {
        field: value for field, value in req.items()
    }}

    book = await BookModel.get(id)

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book record not found!"
        )

    await book.update(update_query)

    return book
@router.delete("/{id}", response_description="Book record deleted from the database")
async def deleted_book(id: PydanticObjectId, username: str = Depends(get_current_username))  -> dict:
    book = await BookModel.get(id)

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Review record not found!"
        )

    await book.delete()

    return {
        "message": "Book deleted successfully"
    }
