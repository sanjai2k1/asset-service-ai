import warnings

warnings.filterwarnings(
    "ignore",
    message="Core Pydantic V1 functionality isn't compatible with Python 3.14 or greater."
)


from fastapi import FastAPI
import webbrowser
from config.settings import settings
from api.routers import system_router ,promptvars_router,promptkeydependency_router,srcreation_router
from db.cache.prompt_cache import prompt_cache
from core.enums import PromptkeyDependency
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from config.settings import settings

app = FastAPI(
    title="Asset Systems & Info AI",
    description="Asset Sytem and Informations",
    version="1.0"
)

origins = settings.allowed_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows POST, GET, etc.
    allow_headers=["*"], # Allows Content-Type, etc.
)

# Register Routers
app.include_router(system_router.router)
app.include_router(promptvars_router.router)
app.include_router(promptkeydependency_router.router)
app.include_router(srcreation_router.router)

BASE_DIR = Path(__file__).resolve().parent
DIST_DIR = BASE_DIR / "dist"

app.mount("/", StaticFiles(directory=DIST_DIR, html=True), name="dist")# Serve index.html

@app.get("/")
def serve_react():
    return FileResponse("dist/index.html")


@app.on_event("startup")
def open_docs():
    url = f"http://{settings.app_host}:{settings.app_port}/docs"
    webbrowser.open(url, new=0)
    url = f"http://{settings.app_host}:{settings.app_port}/"
    webbrowser.open(url, new=0)
    prompt_cache.load(PromptkeyDependency.FEMS)
    prompt_cache.load(PromptkeyDependency.BEMS)
    prompt_cache.load(PromptkeyDependency.CLS)
    prompt_cache.load(PromptkeyDependency.LLS)
    prompt_cache.load(PromptkeyDependency.HWMS)


