from pydantic import BaseModel
from typing import Any

class ResearchRunCreate(BaseModel):
    research_question_id: str | None = None
    query: str
    source_snapshot_id: str | None = None
    evidence_set_hash: str | None = None
    routing_policy_version: str | None = None

class ResearchRunDiff(BaseModel):
    added_sources: list[str]=[]
    removed_sources: list[str]=[]
    changed_claims: list[str]=[]
    changed_observations: list[str]=[]
    changed_models: list[str]=[]
    conclusion_changes: list[str]=[]
