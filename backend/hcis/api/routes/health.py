from fastapi import APIRouter
from hcis.api.contracts import HealthResponse
from hcis.core.settings import settings
router=APIRouter()

@router.get("/health",response_model=HealthResponse)
def health():
    return HealthResponse(status="ok",app_version=settings.app_version,schema_version=settings.schema_version)
