from __future__ import annotations
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, Float, Integer, Boolean, DateTime, ForeignKey, JSON, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Workspace(Base, TimestampMixin):
    __tablename__ = "workspaces"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    schema_version: Mapped[str] = mapped_column(String, nullable=False)
    root_path: Mapped[str] = mapped_column(Text, nullable=False)

class Source(Base, TimestampMixin):
    __tablename__ = "sources"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    canonical_title: Mapped[Optional[str]] = mapped_column(Text)
    source_type: Mapped[Optional[str]] = mapped_column(String)
    language: Mapped[Optional[str]] = mapped_column(String)

class SourceVersion(Base, TimestampMixin):
    __tablename__ = "source_versions"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    source_id: Mapped[str] = mapped_column(ForeignKey("sources.id"), index=True)
    sha256: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    filename: Mapped[str] = mapped_column(Text, nullable=False)
    immutable_path: Mapped[str] = mapped_column(Text, nullable=False)
    edition: Mapped[Optional[str]] = mapped_column(Text)
    mime_type: Mapped[Optional[str]] = mapped_column(String)
    license: Mapped[Optional[str]] = mapped_column(Text)
    privacy_class: Mapped[str] = mapped_column(String, default="LOCAL_PREFERRED")
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)

class SourceLocation(Base, TimestampMixin):
    __tablename__ = "source_locations"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    source_version_id: Mapped[str] = mapped_column(ForeignKey("source_versions.id"), index=True)
    page: Mapped[Optional[int]] = mapped_column(Integer)
    block_id: Mapped[Optional[str]] = mapped_column(String)
    paragraph_id: Mapped[Optional[str]] = mapped_column(String)
    char_start: Mapped[Optional[int]] = mapped_column(Integer)
    char_end: Mapped[Optional[int]] = mapped_column(Integer)
    sheet: Mapped[Optional[str]] = mapped_column(String)
    row: Mapped[Optional[int]] = mapped_column(Integer)
    column: Mapped[Optional[int]] = mapped_column(Integer)
    cell: Mapped[Optional[str]] = mapped_column(String)
    quote_hash: Mapped[Optional[str]] = mapped_column(String(64))
    locator_json: Mapped[dict] = mapped_column(JSON, default=dict)

class SourceRelation(Base, TimestampMixin):
    __tablename__ = "source_relations"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    from_source_version_id: Mapped[str] = mapped_column(ForeignKey("source_versions.id"), index=True)
    to_source_version_id: Mapped[str] = mapped_column(ForeignKey("source_versions.id"), index=True)
    relation_type: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, default="UNKNOWN")
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    evidence_json: Mapped[list] = mapped_column(JSON, default=list)

class SourceCriticismProfile(Base, TimestampMixin):
    __tablename__ = "source_criticism_profiles"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    source_version_id: Mapped[str] = mapped_column(ForeignKey("source_versions.id"), unique=True)
    authenticity_status: Mapped[str] = mapped_column(String, default="UNKNOWN")
    independence_status: Mapped[str] = mapped_column(String, default="UNKNOWN")
    contemporaneity: Mapped[Optional[str]] = mapped_column(Text)
    directness: Mapped[Optional[str]] = mapped_column(Text)
    known_biases: Mapped[list] = mapped_column(JSON, default=list)
    transmission_notes: Mapped[Optional[str]] = mapped_column(Text)
    survival_bias_notes: Mapped[Optional[str]] = mapped_column(Text)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)

class TextualVariant(Base, TimestampMixin):
    __tablename__ = "textual_variants"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    variant_group_id: Mapped[str] = mapped_column(String, index=True)
    source_location_id: Mapped[str] = mapped_column(ForeignKey("source_locations.id"))
    variant_text: Mapped[str] = mapped_column(Text)
    variant_type: Mapped[str] = mapped_column(String)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)

class TextLayer(Base, TimestampMixin):
    __tablename__ = "text_layers"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    source_location_id: Mapped[str] = mapped_column(ForeignKey("source_locations.id"), index=True)
    parent_layer_id: Mapped[Optional[str]] = mapped_column(ForeignKey("text_layers.id"))
    layer_type: Mapped[str] = mapped_column(String)
    language: Mapped[str] = mapped_column(String)
    script: Mapped[Optional[str]] = mapped_column(String)
    content: Mapped[Optional[str]] = mapped_column(Text)
    generated_by: Mapped[Optional[str]] = mapped_column(String)
    model_version: Mapped[Optional[str]] = mapped_column(String)
    confidence: Mapped[Optional[float]] = mapped_column(Float)

class Segment(Base, TimestampMixin):
    __tablename__ = "segments"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    source_location_id: Mapped[str] = mapped_column(ForeignKey("source_locations.id"), index=True)
    text_layer_id: Mapped[Optional[str]] = mapped_column(ForeignKey("text_layers.id"))
    segment_type: Mapped[str] = mapped_column(String, default="BODY")
    content: Mapped[str] = mapped_column(Text)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)

class Entity(Base, TimestampMixin):
    __tablename__ = "entities"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    entity_type: Mapped[str] = mapped_column(String, index=True)
    canonical_label: Mapped[str] = mapped_column(Text)
    valid_time_start: Mapped[Optional[str]] = mapped_column(String)
    valid_time_end: Mapped[Optional[str]] = mapped_column(String)
    valid_place_ref: Mapped[Optional[str]] = mapped_column(String)
    status: Mapped[str] = mapped_column(String, default="UNKNOWN")
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    canonical_entity_id: Mapped[Optional[str]] = mapped_column(ForeignKey("entities.id"))

class EntityMention(Base, TimestampMixin):
    __tablename__ = "entity_mentions"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    entity_id: Mapped[Optional[str]] = mapped_column(ForeignKey("entities.id"), index=True)
    source_location_id: Mapped[str] = mapped_column(ForeignKey("source_locations.id"), index=True)
    surface: Mapped[str] = mapped_column(Text)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)

class Alias(Base, TimestampMixin):
    __tablename__ = "aliases"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    entity_id: Mapped[str] = mapped_column(ForeignKey("entities.id"), index=True)
    label: Mapped[str] = mapped_column(Text)
    alias_type: Mapped[Optional[str]] = mapped_column(String)

class EventCandidate(Base, TimestampMixin):
    __tablename__ = "event_candidates"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    event_type: Mapped[Optional[str]] = mapped_column(String)
    time_start: Mapped[Optional[str]] = mapped_column(String)
    time_end: Mapped[Optional[str]] = mapped_column(String)
    location_refs: Mapped[list] = mapped_column(JSON, default=list)
    participant_refs: Mapped[list] = mapped_column(JSON, default=list)
    status: Mapped[str] = mapped_column(String, default="UNKNOWN")
    confidence: Mapped[float] = mapped_column(Float, default=0.0)

class Claim(Base, TimestampMixin):
    __tablename__ = "claims"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    source_location_id: Mapped[str] = mapped_column(ForeignKey("source_locations.id"), index=True)
    text_layer_id: Mapped[Optional[str]] = mapped_column(ForeignKey("text_layers.id"))
    subject_ref: Mapped[Optional[str]] = mapped_column(String)
    predicate: Mapped[Optional[str]] = mapped_column(String)
    object_json: Mapped[dict] = mapped_column(JSON, default=dict)
    epistemic_status: Mapped[str] = mapped_column(String, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    extraction_run_id: Mapped[Optional[str]] = mapped_column(String)

class Observation(Base, TimestampMixin):
    __tablename__ = "observations"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    source_location_id: Mapped[str] = mapped_column(ForeignKey("source_locations.id"), index=True)
    variable: Mapped[str] = mapped_column(String, index=True)
    original_value_json: Mapped[dict] = mapped_column(JSON, default=dict)
    parsed_value_json: Mapped[dict] = mapped_column(JSON, default=dict)
    unit_original: Mapped[Optional[str]] = mapped_column(String)
    unit_normalized: Mapped[Optional[str]] = mapped_column(String)
    definition: Mapped[Optional[str]] = mapped_column(Text)
    time_start: Mapped[Optional[str]] = mapped_column(String)
    time_end: Mapped[Optional[str]] = mapped_column(String)
    place_ref: Mapped[Optional[str]] = mapped_column(String)
    group_ref: Mapped[Optional[str]] = mapped_column(String)
    observation_type: Mapped[str] = mapped_column(String)
    coverage: Mapped[Optional[str]] = mapped_column(Text)
    uncertainty_json: Mapped[dict] = mapped_column(JSON, default=dict)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)

class FactCandidate(Base, TimestampMixin):
    __tablename__ = "fact_candidates"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    subject_ref: Mapped[Optional[str]] = mapped_column(String)
    predicate: Mapped[Optional[str]] = mapped_column(String)
    object_json: Mapped[dict] = mapped_column(JSON, default=dict)
    status: Mapped[str] = mapped_column(String, default="UNKNOWN")
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    method_version: Mapped[Optional[str]] = mapped_column(String)

class Evidence(Base, TimestampMixin):
    __tablename__ = "evidence"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    evidence_type: Mapped[str] = mapped_column(String)
    claim_id: Mapped[Optional[str]] = mapped_column(ForeignKey("claims.id"), index=True)
    observation_id: Mapped[Optional[str]] = mapped_column(ForeignKey("observations.id"), index=True)
    fact_candidate_id: Mapped[Optional[str]] = mapped_column(ForeignKey("fact_candidates.id"), index=True)
    source_relation_id: Mapped[Optional[str]] = mapped_column(ForeignKey("source_relations.id"))
    confidence: Mapped[float] = mapped_column(Float, default=0.0)

class ConflictGroup(Base, TimestampMixin):
    __tablename__ = "conflict_groups"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    topic_key: Mapped[str] = mapped_column(String, index=True)
    member_refs: Mapped[list] = mapped_column(JSON, default=list)
    status: Mapped[str] = mapped_column(String, default="DISPUTED")

class HistoricalDate(Base, TimestampMixin):
    __tablename__ = "historical_dates"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    source_location_id: Mapped[Optional[str]] = mapped_column(ForeignKey("source_locations.id"))
    original_expression: Mapped[str] = mapped_column(Text)
    calendar_system: Mapped[Optional[str]] = mapped_column(String)
    reign_title: Mapped[Optional[str]] = mapped_column(String)
    reign_year: Mapped[Optional[int]] = mapped_column(Integer)
    normalized_start: Mapped[Optional[str]] = mapped_column(String)
    normalized_end: Mapped[Optional[str]] = mapped_column(String)
    conversion_rule_id: Mapped[Optional[str]] = mapped_column(String)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)

class HistoricalQuantity(Base, TimestampMixin):
    __tablename__ = "historical_quantities"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    source_location_id: Mapped[Optional[str]] = mapped_column(ForeignKey("source_locations.id"))
    original_value_json: Mapped[dict] = mapped_column(JSON)
    original_unit: Mapped[str] = mapped_column(String)
    quantity_type: Mapped[Optional[str]] = mapped_column(String)
    normalized_range_json: Mapped[dict] = mapped_column(JSON, default=dict)
    normalized_unit: Mapped[Optional[str]] = mapped_column(String)
    conversion_rule_id: Mapped[Optional[str]] = mapped_column(String)

class ResearchQuestion(Base, TimestampMixin):
    __tablename__ = "research_questions"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    question: Mapped[str] = mapped_column(Text)
    scope_json: Mapped[dict] = mapped_column(JSON, default=dict)
    status: Mapped[str] = mapped_column(String, default="OPEN")

class Hypothesis(Base, TimestampMixin):
    __tablename__ = "hypotheses"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    research_question_id: Mapped[str] = mapped_column(ForeignKey("research_questions.id"), index=True)
    statement: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String, default="OPEN")
    evidence_json: Mapped[dict] = mapped_column(JSON, default=dict)
    falsification_conditions: Mapped[list] = mapped_column(JSON, default=list)

class CoverageCell(Base, TimestampMixin):
    __tablename__ = "coverage_cells"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    dimensions_json: Mapped[dict] = mapped_column(JSON, default=dict)
    source_count_raw: Mapped[int] = mapped_column(Integer, default=0)
    source_count_independent: Mapped[int] = mapped_column(Integer, default=0)
    claim_count: Mapped[int] = mapped_column(Integer, default=0)
    observation_count: Mapped[int] = mapped_column(Integer, default=0)
    coverage_level: Mapped[str] = mapped_column(String, default="UNKNOWN")

class GoldenCase(Base, TimestampMixin):
    __tablename__ = "golden_cases"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    task_class: Mapped[str] = mapped_column(String, index=True)
    input_json: Mapped[dict] = mapped_column(JSON, default=dict)
    expected_json: Mapped[dict] = mapped_column(JSON, default=dict)
    version: Mapped[str] = mapped_column(String, default="1")

class ResearchRun(Base, TimestampMixin):
    __tablename__ = "research_runs"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    research_question_id: Mapped[Optional[str]] = mapped_column(ForeignKey("research_questions.id"))
    query: Mapped[str] = mapped_column(Text)
    source_snapshot_id: Mapped[Optional[str]] = mapped_column(String)
    evidence_set_hash: Mapped[Optional[str]] = mapped_column(String(64))
    routing_policy_version: Mapped[Optional[str]] = mapped_column(String)
    result_json: Mapped[dict] = mapped_column(JSON, default=dict)

class ProviderProfile(Base, TimestampMixin):
    __tablename__ = "provider_profiles"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    provider_type: Mapped[str] = mapped_column(String)
    base_url: Mapped[Optional[str]] = mapped_column(Text)
    secret_ref: Mapped[Optional[str]] = mapped_column(Text)
    locality: Mapped[str] = mapped_column(String)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)

class ModelProfile(Base, TimestampMixin):
    __tablename__ = "model_profiles"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    provider_id: Mapped[str] = mapped_column(ForeignKey("provider_profiles.id"), index=True)
    model_id: Mapped[str] = mapped_column(String)
    capabilities_json: Mapped[dict] = mapped_column(JSON, default=dict)
    status: Mapped[str] = mapped_column(String, default="UNAVAILABLE")

class TaskRoutingPolicy(Base, TimestampMixin):
    __tablename__ = "task_routing_policies"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    task_class: Mapped[str] = mapped_column(String, unique=True)
    mode: Mapped[str] = mapped_column(String)
    primary_model_profile_id: Mapped[Optional[str]] = mapped_column(ForeignKey("model_profiles.id"))
    fallback_model_profile_ids: Mapped[list] = mapped_column(JSON, default=list)
    privacy_requirement: Mapped[str] = mapped_column(String, default="SOURCE_POLICY")

class ModelCall(Base, TimestampMixin):
    __tablename__ = "model_calls"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    task_class: Mapped[str] = mapped_column(String)
    provider_id: Mapped[str] = mapped_column(String)
    model_profile_id: Mapped[str] = mapped_column(String)
    input_tokens: Mapped[Optional[int]] = mapped_column(Integer)
    output_tokens: Mapped[Optional[int]] = mapped_column(Integer)
    latency_ms: Mapped[Optional[int]] = mapped_column(Integer)
    estimated_cost: Mapped[Optional[float]] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)

class SourceProvider(Base, TimestampMixin):
    __tablename__ = "source_providers"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    connector_type: Mapped[str] = mapped_column(String)
    endpoints_json: Mapped[dict] = mapped_column(JSON, default=dict)
    rights_policy_url: Mapped[Optional[str]] = mapped_column(Text)
    default_acquisition_mode: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String)

class AcquisitionCandidate(Base, TimestampMixin):
    __tablename__ = "acquisition_candidates"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    provider_id: Mapped[str] = mapped_column(ForeignKey("source_providers.id"), index=True)
    external_id: Mapped[str] = mapped_column(String)
    persistent_identifier: Mapped[Optional[str]] = mapped_column(String)
    title: Mapped[str] = mapped_column(Text)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)
    rights_json: Mapped[dict] = mapped_column(JSON, default=dict)
    acquisition_mode: Mapped[str] = mapped_column(String)
    relevance: Mapped[Optional[float]] = mapped_column(Float)

class Job(Base, TimestampMixin):
    __tablename__ = "jobs"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    job_type: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String, default="QUEUED")
    payload_json: Mapped[dict] = mapped_column(JSON, default=dict)
    error_json: Mapped[dict] = mapped_column(JSON, default=dict)

class AuditEvent(Base, TimestampMixin):
    __tablename__ = "audit_events"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    event_type: Mapped[str] = mapped_column(String)
    actor: Mapped[str] = mapped_column(String, default="SYSTEM")
    object_ref: Mapped[Optional[str]] = mapped_column(String)
    details_json: Mapped[dict] = mapped_column(JSON, default=dict)

class DependencyEdge(Base, TimestampMixin):
    __tablename__ = "dependency_edges"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    derived_ref: Mapped[str] = mapped_column(String, index=True)
    upstream_ref: Mapped[str] = mapped_column(String, index=True)
    relation: Mapped[str] = mapped_column(String, default="DEPENDS_ON")
