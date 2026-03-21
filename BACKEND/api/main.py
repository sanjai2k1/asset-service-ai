from fastapi import FastAPI
import webbrowser
from config.settings import settings
from api.routers import system_router ,promptvars_router,promptkeydependency_router,srcreation_router
from db.cache.prompt_cache import prompt_cache
from core.enums import PromptkeyDependency
app = FastAPI(
    title="Asset Systems & Info AI",
    description="Asset Sytem and Informations",
    version="1.0"
)



# Register Routers
app.include_router(system_router.router)
app.include_router(promptvars_router.router)
app.include_router(promptkeydependency_router.router)
app.include_router(srcreation_router.router)

@app.on_event("startup")
def open_docs():
    url = f"http://{settings.app_host}:{settings.app_port}/docs"
    webbrowser.open(url, new=0)

    print("🔥 Warming up cache...")
    prompt_cache.load(PromptkeyDependency.FEMS)
    prompt_cache.load(PromptkeyDependency.BEMS)
    prompt_cache.load(PromptkeyDependency.CLS)
    prompt_cache.load(PromptkeyDependency.LLS)
    prompt_cache.load(PromptkeyDependency.HWMS)
    print("✅ Cache Ready:")


