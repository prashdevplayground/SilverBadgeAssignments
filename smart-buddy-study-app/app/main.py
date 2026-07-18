# This file creates the FastAPI application instance that powers the Smart Buddy Study service.
# It is the main entry point for the backend and wires the API routes into the application.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from app.api.routes import router as study_router
from app.core.config import settings

templates = Jinja2Templates(directory="app/templates")

# We create a FastAPI instance with metadata that helps the API documentation and deployment tools.
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="A modern RAG-powered study assistant powered by FastAPI, LangChain, and vector search.",
)

# We allow browser-based clients to call the API from different origins during local development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# We register the study routes under the /api prefix so the service stays organized.
app.include_router(study_router, prefix="/api")


@app.get("/")
def read_root() -> dict[str, str]:
    # This root endpoint keeps the API health check behavior intact while remaining simple for clients.
    return {"message": "Smart Buddy Study API is live", "version": settings.app_version}


@app.get("/ui", response_class=HTMLResponse)
async def read_ui(request: Request) -> HTMLResponse:
    # This route serves the browser-based front end so the project feels complete and usable from a browser.
    return templates.TemplateResponse(request=request, name="index.html")
