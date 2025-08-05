from functools import lru_cache

from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import RedirectResponse
from starlette.middleware.cors import CORSMiddleware

from urban_sdk_homework.core.fastapi import APIRouter
from urban_sdk_homework.core.project.metadata import metadata
from urban_sdk_homework.modules.api.settings import ApiSettings


@lru_cache()
def settings() -> ApiSettings:
    """Get the current Web API settings."""
    return ApiSettings()


#: This is the FastAPI application.
app = FastAPI(
    version=str(metadata().version),
    title=settings().title or metadata().name,
    docs_url=settings().docs_url,
    redoc_url=settings().redoc_url,
    openapi_url=settings().openapi_url,
    swagger_ui_parameters={"docExpansion": "none"},
)

# Set up CORS.
app.add_middleware(CORSMiddleware, **settings().cors.model_dump())

# Get all of the available routers and add them to the app.
for router in APIRouter.instances(condition=lambda r: r.enabled):
    app.include_router(router)


@app.get("/", include_in_schema=False)
async def root():
    """Redirect to OpenAPI documentation."""
    return RedirectResponse(url="/openapi")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage the application lifespan."""
    # Perform "startup" tasks.
    yield
    # Perform "shutdown" tasks.
