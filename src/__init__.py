from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import status
from src.db.main import init_db
from src.books.routes import book_router
from src.auth.routes import auth_routes
from src.reviews.routes import review_router
from src.tags.routes import tags_router
from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.errors import register_custom_errors
from src.middlewares import register_middlewares


@asynccontextmanager
async def life_span_bro(app:FastAPI):
    print("server is running")
    await init_db()
    yield
    print("server is shutting down")


version = "v1"

app = FastAPI(
    title="Bookly",
    description="A REST API for book review web service",
    version=version,
    docs_url=f"/api/{version}/docs",
    contact={
        "email":"combatant936@gmail.com"
    },
    redoc_url=f"/api/{version}/redoc",
    openapi_url=f"/api/{version}/openapi.json",
    lifespan=life_span_bro
)

register_custom_errors(app)
register_middlewares(app)





app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"])
app.include_router(auth_routes, prefix=f"/api/{version}/auth", tags=["auth"])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=["review"])
app.include_router(tags_router, prefix=f"/api/{version}/tags", tags=["tags"])




