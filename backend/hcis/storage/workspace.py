from __future__ import annotations
import json, sqlite3, uuid, shutil
from pathlib import Path
from .contracts import WorkspacePaths

class LocalWorkspaceManager:
    def __init__(self, root: Path):
        self.root=root

    def create(self, root: str) -> WorkspacePaths:
        r=Path(root)
        paths=WorkspacePaths(
            root=str(r), database=str(r/"database"/"hcis.db"),
            source_vault=str(r/"source_vault"), derived=str(r/"derived"),
            cache=str(r/"cache"), logs=str(r/"logs"), backups=str(r/"backups"))
        for p in [Path(paths.database).parent,Path(paths.source_vault),Path(paths.derived),
                  Path(paths.cache),Path(paths.logs),Path(paths.backups)]:
            p.mkdir(parents=True,exist_ok=True)
        marker=r/"workspace.json"
        if not marker.exists():
            marker.write_text(json.dumps({"workspace_id":str(uuid.uuid4()),"schema_version":"0001"},indent=2),encoding="utf-8")
        return paths

    def locate(self, root: str) -> WorkspacePaths:
        r=Path(root)
        if not (r/"workspace.json").exists():
            raise FileNotFoundError("STORAGE_UNAVAILABLE: workspace.json missing")
        return self.create(root)

    def verify(self) -> dict:
        marker=self.root/"workspace.json"
        if not marker.exists():
            return {"status":"STORAGE_UNAVAILABLE"}
        return {"status":"READY","workspace":json.loads(marker.read_text(encoding="utf-8"))}

    def relocate_database(self, target: str) -> dict:
        src=self.root/"database"/"hcis.db"
        if not src.exists():
            raise FileNotFoundError("source database missing")
        tgt=Path(target); tgt.parent.mkdir(parents=True,exist_ok=True)
        backup=tgt.with_suffix(".pre_switch_backup.sqlite")
        shutil.copy2(src,backup)
        src_conn=sqlite3.connect(src)
        dst_conn=sqlite3.connect(tgt)
        try:
            src_conn.backup(dst_conn)
            row=dst_conn.execute("PRAGMA integrity_check").fetchone()
            if not row or row[0]!="ok":
                raise RuntimeError("target integrity_check failed")
        finally:
            src_conn.close(); dst_conn.close()
        return {"status":"READY_FOR_ATOMIC_CONFIG_SWITCH","target":str(tgt),"safety_copy":str(backup)}

    def relocate_source_vault(self, target: str) -> dict:
        raise NotImplementedError("TODO: copy+checksum+atomic switch+rollback")
