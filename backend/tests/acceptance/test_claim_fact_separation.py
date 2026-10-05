from hcis.domain.models import Claim, FactCandidate
def test_claim_and_fact_are_distinct_tables():
    assert Claim.__tablename__ != FactCandidate.__tablename__
    assert Claim.__tablename__=="claims"
    assert FactCandidate.__tablename__=="fact_candidates"
