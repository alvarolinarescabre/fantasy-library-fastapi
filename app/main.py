from fastapi import FastAPI
from server.routes.library import router as LibraryRouter

app = FastAPI()
app.include_router(LibraryRouter, tags=["Library"], prefix="/library")

@app.get("/", tags=['root'])
async def read_root():
    return {"message": "Welcome to Fantasy Library"}