from __future__ import annotations
from typing import Protocol, Any
from dataclasses import dataclass

@dataclass(frozen=True)
class AdapterHealth:
    status: str
    version: str | None = None
    detail: str | None = None

class DocumentParserAdapter(Protocol):
    def parse(self, source_path: str, options: dict | None = None) -> dict: ...
    def health(self) -> AdapterHealth: ...

class OCRAdapter(Protocol):
    def recognize(self, input_ref: str, options: dict | None = None) -> dict: ...
    def health(self) -> AdapterHealth: ...

class StructuredDatasetAdapter(Protocol):
    def inspect(self, source_path: str) -> dict: ...
    def parse(self, source_path: str, mapping: dict | None = None) -> dict: ...

class EntityCandidateMatcher(Protocol):
    def candidates(self, mention: str, context: dict | None = None) -> list[dict]: ...

class PlaceResolver(Protocol):
    def candidates(self, mention: str, time_context: dict | None = None, geo_context: dict | None = None) -> list[dict]: ...

class GraphProjection(Protocol):
    def rebuild(self, scope: dict | None = None) -> dict: ...
