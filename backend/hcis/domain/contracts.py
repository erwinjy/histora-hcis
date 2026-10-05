from __future__ import annotations
from typing import Any, Optional
from pydantic import BaseModel, Field

class SourceImportRequest(BaseModel):
    path: str
    local_only: bool = False

class SourceImportResult(BaseModel):
    source_id: str
    source_version_id: str
    sha256: str
    deduplicated: bool

class ClaimCreate(BaseModel):
    source_location_id: str
    text_layer_id: str | None = None
    subject_ref: str | None = None
    predicate: str | None = None
    object: Any = None
    epistemic_status: str
    confidence: float = Field(ge=0, le=1)

class ObservationCreate(BaseModel):
    source_location_id: str
    variable: str
    original_value: Any
    observation_type: str
    unit_original: str | None = None
    definition: str | None = None
    confidence: float = Field(default=0, ge=0, le=1)

class EntityMergeRequest(BaseModel):
    source_entity_ids: list[str]
    canonical_entity_id: str
    reason: str
    evidence_refs: list[str] = []

class EntitySplitAssignment(BaseModel):
    mention_id: str
    target_entity_id: str

class EntitySplitRequest(BaseModel):
    source_entity_id: str
    new_entities: list[dict]
    assignments: list[EntitySplitAssignment]
    reason: str
