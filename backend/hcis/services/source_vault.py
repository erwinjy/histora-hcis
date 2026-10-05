from __future__ import annotations
import hashlib, shutil, uuid
from pathlib import Path
from sqlalchemy.orm import Session
from hcis.domain.models import Source, SourceVersion, AuditEvent

class SourceVaultService:
    def __init__(self, db: Session, vault_root: Path):
        self.db=db
        self.vault_root=vault_root

    @staticmethod
    def sha256(path: Path) -> str:
        h=hashlib.sha256()
        with path.open("rb") as f:
            for chunk in iter(lambda:f.read(1024*1024), b""):
                h.update(chunk)
        return h.hexdigest()

    def ingest(self, path: Path, local_only: bool=False) -> SourceVersion:
        digest=self.sha256(path)
        existing=self.db.query(SourceVersion).filter_by(sha256=digest).first()
        if existing:
            return existing
        source=Source(id=str(uuid.uuid4()), canonical_title=path.stem)
        target_dir=self.vault_root/digest
        target_dir.mkdir(parents=True, exist_ok=True)
        target=target_dir/path.name
        shutil.copy2(path,target)
        if self.sha256(target)!=digest:
            raise RuntimeError("source vault copy checksum mismatch")
        version=SourceVersion(
            id=str(uuid.uuid4()), source_id=source.id, sha256=digest,
            filename=path.name, immutable_path=str(target),
            privacy_class="LOCAL_ONLY" if local_only else "LOCAL_PREFERRED",
        )
        self.db.add_all([source,version,AuditEvent(
            id=str(uuid.uuid4()), event_type="SOURCE_IMPORT", actor="SYSTEM",
            object_ref=version.id, details_json={"sha256":digest}
        )])
        self.db.commit()
        return version
