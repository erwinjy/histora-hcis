from fastapi import APIRouter
from hcis.model_control.providers import OllamaProvider
router=APIRouter(prefix="/models",tags=["models"])

@router.get("/ollama/discover")
async def ollama_discover():
    p=OllamaProvider()
    h=await p.health_check()
    if h.status!="READY":
        return {"status":h.status,"detail":h.detail,"models":[]}
    return {"status":"READY","models":await p.list_models()}
