from fastapi import FastAPI
import uvicorn
from hcis.core.db import init_db
from hcis.api.routes.health import router as health_router
from hcis.api.routes.sources import router as sources_router
from hcis.api.routes.models import router as models_router
from hcis.api.routes.research import router as research_router

app=FastAPI(title="HCIS",version="0.2.0")
app.include_router(health_router)
app.include_router(sources_router)
app.include_router(models_router)
app.include_router(research_router)

@app.on_event("startup")
def startup():
    init_db()

if __name__=="__main__":
    uvicorn.run("hcis.main:app",host="127.0.0.1",port=8765,reload=False)
