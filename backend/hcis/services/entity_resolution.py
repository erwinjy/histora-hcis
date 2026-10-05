class EntityResolutionService:
    """
    CONTRACT LOCKED.
    Implement candidate generation / scoring / adjudication without changing public method names.
    """
    def candidates(self, mention: str, context: dict | None = None) -> list[dict]:
        raise NotImplementedError("TODO: integrate exact/normalized/DeezyMatch/RapidFuzz/external candidates")

    def merge(self, canonical_entity_id: str, source_entity_ids: list[str], reason: str) -> None:
        raise NotImplementedError("TODO: transactional MERGE + RELINK + RECALCULATE + AuditEvent")

    def split(self, source_entity_id: str, assignments: dict[str, str], reason: str) -> None:
        raise NotImplementedError("TODO: transactional SPLIT; never copy all old relations blindly")
