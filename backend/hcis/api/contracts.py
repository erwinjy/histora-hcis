from pydantic import BaseModel

class HealthResponse(BaseModel):
    status: str
    app_version: str
    schema_version: str

class ErrorResponse(BaseModel):
    code: str
    message: str
    details: dict | None = None
