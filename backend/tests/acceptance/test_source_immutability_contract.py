from pathlib import Path
from hcis.services.source_vault import SourceVaultService
def test_source_vault_hash_is_sha256(tmp_path):
    p=tmp_path/"史料.txt"; p.write_text("崇祯二年",encoding="utf-8")
    digest=SourceVaultService.sha256(p)
    assert len(digest)==64
