from sqlalchemy.orm import Session
from sqlalchemy import select
from hcis.domain import models

class SqlAlchemySourceRepository:
    def __init__(self, db: Session): self.db=db
    def create_source(self, **data):
        obj=models.Source(**data); self.db.add(obj); self.db.flush(); return obj
    def create_version(self, **data):
        obj=models.SourceVersion(**data); self.db.add(obj); self.db.flush(); return obj
    def get_version_by_hash(self, sha256: str):
        return self.db.scalar(select(models.SourceVersion).where(models.SourceVersion.sha256==sha256))

class SqlAlchemyClaimRepository:
    def __init__(self, db: Session): self.db=db
    def create(self, **data):
        obj=models.Claim(**data); self.db.add(obj); self.db.flush(); return obj
    def get(self, claim_id: str):
        return self.db.get(models.Claim, claim_id)
    def list_by_source_version(self, source_version_id: str):
        q=(select(models.Claim)
           .join(models.SourceLocation, models.Claim.source_location_id==models.SourceLocation.id)
           .where(models.SourceLocation.source_version_id==source_version_id))
        return list(self.db.scalars(q))
