import pytest
from hcis.model_control.router import ModelRouter,RouteCandidate
def test_local_only_never_routes_cloud():
    router=ModelRouter()
    c=[RouteCandidate("cloud","CLOUD",{"text":True},True,100,0)]
    with pytest.raises(PermissionError,match="BLOCKED_PRIVACY_POLICY"):
        router.route(source_privacy="LOCAL_ONLY",required_capabilities={"text"},candidates=c)
