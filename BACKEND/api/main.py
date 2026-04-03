import warnings

warnings.filterwarnings(
    "ignore",
    message="Core Pydantic V1 functionality isn't compatible with Python 3.14 or greater."
)


from fastapi import FastAPI
import webbrowser
from config.settings import settings
from api.routers import system_router ,promptvars_router,promptkeydependency_router,srcreation_router,excel_analysis
from db.cache.prompt_cache import prompt_cache
from core.enums import PromptkeyDependency
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from config.settings import settings
from llm.utils.check_pointer_util import checkpoint_util
import asyncio

app = FastAPI(
    title="Asset Systems & Info AI",
    description="Asset Sytem and Informations",
    version="1.0"
)

origins = settings.allowed_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], # Allows POST, GET, etc.
    allow_headers=["*"], # Allows Content-Type, etc.
)

# Register Routers
app.include_router(system_router.router)
app.include_router(promptvars_router.router)
app.include_router(promptkeydependency_router.router)
app.include_router(srcreation_router.router)
app.include_router(excel_analysis.router)

BASE_DIR = Path(__file__).resolve().parent
DIST_DIR = BASE_DIR / "dist"
ASSETS_DIR = DIST_DIR / "assets"

app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")

@app.get("/{full_path:path}")
async def serve_react(full_path: str):
    index_file = DIST_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"error": "index.html not found"}


async def load_prompts():
    for key in [
        PromptkeyDependency.FEMS,
        PromptkeyDependency.BEMS,
        PromptkeyDependency.CLS,
        PromptkeyDependency.LLS,
        PromptkeyDependency.HWMS,
    ]:
        await asyncio.to_thread(prompt_cache.load, key)
@app.on_event("startup")
async def open_docs():
    url = f"http://{settings.app_host}:{settings.app_port}/docs"
    asyncio.create_task(asyncio.to_thread(webbrowser.open, url, 0))
    # url = f"http://{settings.app_host}:{settings.app_port}/"
    # asyncio.create_task(asyncio.to_thread(webbrowser.open, url, 0))

    asyncio.create_task(checkpoint_util.setup())

    asyncio.create_task(load_prompts())

@app.on_event("shutdown")
async def shutdown():
    await checkpoint_util.shutdown()  # ✅ stop retry loop


