import os
import motor.motor_asyncio
from bson.objectid import ObjectId


client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["DB_URL"])

database = client.fantasy_library

fantasy_library_collection = database.get_collection("fantasy_library_collection")

def fantasy_library_helper(fantasy_library) -> dict:
    return {
        "id": str(fantasy_library["_id"]),
        "title": (fantasy_library["title"]),
        "author": (fantasy_library["author"]),
        "genre": (fantasy_library["genre"]),
        "publish_date": fantasy_library["publish_date"],
        "isbn": fantasy_library["isbn"]
    }

# Buscar todos los libros de la base de datos
async def retrieve_books():
    books = []
    async for book in fantasy_library_collection.find():
        books.append(fantasy_library_helper(book))
    return books

# Agregar un book a la base de datos
async def add_book(book_data: dict) -> dict:
    book = await fantasy_library_collection.insert_one(book_data)
    new_book = await fantasy_library_collection.find_one({"_id": book.inserted_id})
    return fantasy_library_helper(new_book)

# Buscar un book a partir de un ID
async def retrieve_book(id: str) -> dict:
    book = await fantasy_library_collection.find_one({"_id": ObjectId(id)})
    if book:
        return fantasy_library_helper(book)

# Actulizar un book a partir de un ID
async def update_book(id: str, data: dict):
    # Devuelve falso si el cuerpo del request está vacio
    if len(data) < 1:
        return False
    book = await fantasy_library_collection.find_one({"_id": ObjectId(id)})
    if book:
        updated_book = await fantasy_library_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_book:
            return True
        return False

# Borrar un libro de la base de datos
async def delete_book(id: str):
    book = await fantasy_library_collection.find_one({"_id": ObjectId(id)})
    if book:
        await fantasy_library_collection.delete_one({"_id": ObjectId(id)})
        return True
