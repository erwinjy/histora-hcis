from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol, Any

@dataclass(frozen=True)
class ModelCapabilities:
    text: bool = True
    vision: bool = False
    structured_output: bool = False
    json_schema: bool = False
    tools: bool = False
    embeddings: bool = False
    reasoning: bool = False

@dataclass(frozen=True)
class ProviderHealth:
    status: str
    latency_ms: int | None = None
    detail: str | None = None

class ModelProvider(Protocol):
    async def list_models(self) -> list[dict]: ...
    async def health_check(self) -> ProviderHealth: ...
    async def complete(self, request: dict) -> dict: ...
    async def structured_extract(self, request: dict, json_schema: dict) -> dict: ...
    async def embed(self, request: dict) -> dict: ...
    async def capabilities(self, model_id: str) -> ModelCapabilities: ...

class SecretStore(Protocol):
    def put(self, key: str, secret: str) -> str: ...
    def get(self, secret_ref: str) -> str: ...
    def delete(self, secret_ref: str) -> None: ...
