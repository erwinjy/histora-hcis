from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from hcis.core.db import SessionLocal
from hcis.domain.contracts import SourceImportRequest, SourceImportResult
from hcis.services.source_vault import SourceVaultService
from hcis.core.settings import settings

router=APIRouter(prefix="/sources",tags=["sources"])

def db():
    s=SessionLocal()
    try: yield s
    finally: s.close()

@router.post("/import",response_model=SourceImportResult)
def import_source(req: SourceImportRequest, session: Session=Depends(db)):
    p=Path(req.path)
    if not p.exists(): raise HTTPException(404,"source file not found")
    svc=SourceVaultService(session, settings.workspace_root/"source_vault")
    before=svc.sha256(p)
    existing=session.query(__import__("hcis.domain.models",fromlist=["SourceVersion"]).SourceVersion).filter_by(sha256=before).first()
    version=svc.ingest(p,req.local_only)
    return SourceImportResult(source_id=version.source_id,source_version_id=version.id,sha256=version.sha256,deduplicated=existing is not None)
