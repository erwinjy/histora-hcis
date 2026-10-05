from hcis.domain.models import SourceRelation
def test_source_relation_is_first_class():
    assert SourceRelation.__tablename__=="source_relations"
