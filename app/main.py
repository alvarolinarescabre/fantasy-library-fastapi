from fastapi import FastAPI
from app.server.routes.routes import router as library_route
from app.server.database import init_db
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)


app = FastAPI(docs_url=None, redoc_url=None, title="Fantasy Library")
app.include_router(library_route, tags=["Fantasy Library"], prefix="/v1")

@app.on_event("startup")
async def start_db():
    await init_db()

@app.get("/", tags=['root'])
async def read_root():
    return {"message": "Welcome to Fantasy Library", "version": "1.0"}

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()

