from __future__ import annotations
import httpx
from .contracts import ProviderHealth, ModelCapabilities

class OllamaProvider:
    def __init__(self, base_url="http://127.0.0.1:11434"):
        self.base_url=base_url.rstrip("/")

    async def list_models(self):
        async with httpx.AsyncClient(timeout=10) as c:
            r=await c.get(f"{self.base_url}/api/tags"); r.raise_for_status()
            return r.json().get("models",[])

    async def health_check(self):
        try:
            models=await self.list_models()
            return ProviderHealth(status="READY", detail=f"{len(models)} models")
        except Exception as e:
            return ProviderHealth(status="UNAVAILABLE", detail=str(e))

    async def complete(self, request):
        async with httpx.AsyncClient(timeout=120) as c:
            r=await c.post(f"{self.base_url}/api/chat", json=request); r.raise_for_status(); return r.json()

    async def structured_extract(self, request, json_schema):
        payload=dict(request); payload["format"]=json_schema
        return await self.complete(payload)

    async def embed(self, request):
        async with httpx.AsyncClient(timeout=120) as c:
            r=await c.post(f"{self.base_url}/api/embed",json=request); r.raise_for_status(); return r.json()

    async def capabilities(self, model_id):
        return ModelCapabilities(text=True, structured_output=True)

class OpenAICompatibleProvider:
    def __init__(self, base_url: str, api_key: str | None=None):
        self.base_url=base_url.rstrip("/")
        self.headers={"Authorization":f"Bearer {api_key}"} if api_key else {}

    async def list_models(self):
        async with httpx.AsyncClient(timeout=15,headers=self.headers) as c:
            r=await c.get(f"{self.base_url}/models"); r.raise_for_status()
            return r.json().get("data",[])

    async def health_check(self):
        try:
            m=await self.list_models()
            return ProviderHealth(status="READY",detail=f"{len(m)} models")
        except Exception as e:
            return ProviderHealth(status="UNAVAILABLE",detail=str(e))

    async def complete(self, request):
        async with httpx.AsyncClient(timeout=120,headers=self.headers) as c:
            r=await c.post(f"{self.base_url}/chat/completions",json=request); r.raise_for_status(); return r.json()

    async def structured_extract(self, request, json_schema):
        payload=dict(request)
        payload["response_format"]={"type":"json_schema","json_schema":{"name":"hcis","schema":json_schema}}
        return await self.complete(payload)

    async def embed(self, request):
        async with httpx.AsyncClient(timeout=120,headers=self.headers) as c:
            r=await c.post(f"{self.base_url}/embeddings",json=request); r.raise_for_status(); return r.json()

    async def capabilities(self, model_id):
        return ModelCapabilities(text=True, structured_output=True, json_schema=True)
