from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True)
class RightsDecision:
    rights_status: str
    license: str | None
    download_allowed: bool
    analysis_allowed: bool | None
    redistribution_allowed: bool | None
    attribution_required: bool | None
    policy_source: str | None
    reason: str

class SourceAcquisitionConnector(Protocol):
    async def provider_info(self) -> dict: ...
    async def health_check(self) -> dict: ...
    async def search(self, query: dict) -> list[dict]: ...
    async def get_item(self, external_id: str) -> dict: ...
    async def get_rights(self, candidate: dict) -> RightsDecision: ...
    async def download(self, candidate: dict, target_path: str) -> dict: ...
