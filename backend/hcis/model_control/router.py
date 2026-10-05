from __future__ import annotations
from dataclasses import dataclass
from hcis.core.enums import PrivacyClass

@dataclass
class RouteCandidate:
    model_profile_id: str
    locality: str
    capabilities: dict
    healthy: bool
    benchmark_score: float = 0.0
    estimated_cost: float = 0.0

class ModelRouter:
    """
    CONTRACT LOCKED.
    Privacy and capability are hard constraints.
    """
    def route(self, *, source_privacy: str, required_capabilities: set[str],
              candidates: list[RouteCandidate]) -> RouteCandidate:
        eligible=[]
        for c in candidates:
            if not c.healthy:
                continue
            if source_privacy == PrivacyClass.LOCAL_ONLY and c.locality != "LOCAL":
                continue
            if any(not c.capabilities.get(cap, False) for cap in required_capabilities):
                continue
            eligible.append(c)
        if not eligible:
            if source_privacy == PrivacyClass.LOCAL_ONLY:
                raise PermissionError("BLOCKED_PRIVACY_POLICY")
            raise RuntimeError("NO_ELIGIBLE_MODEL")
        return sorted(eligible, key=lambda x:(-x.benchmark_score, x.estimated_cost))[0]
