from fastapi import FastAPI
from app.manifest import router as manifest_router
from app.routes.model_card import router as model_card_router
from app.routes.search import router as search_router

app = FastAPI(title="Patra MCP Server")

app.include_router(manifest_router)
app.include_router(model_card_router)
app.include_router(search_router)
