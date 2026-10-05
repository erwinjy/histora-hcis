from hcis.core.enums import ClaimEpistemicStatus, FactStatus

def claim_can_auto_verify(epistemic_status: str) -> bool:
    # HARD RULE: source assertions never become VERIFIED facts directly.
    return False

def minimum_fact_status_for_claim(epistemic_status: str) -> str:
    if epistemic_status in {ClaimEpistemicStatus.RUMORED, ClaimEpistemicStatus.UNCERTAIN}:
        return FactStatus.UNKNOWN
    return FactStatus.POSSIBLE
