from hcis.domain.models import Observation
def test_observation_is_first_class():
    assert Observation.__tablename__=="observations"
