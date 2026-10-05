from pathlib import Path
import json,hashlib,sys
ROOT=Path(__file__).resolve().parent.parent
lock=json.loads((ROOT/"CODE_LOCK_MANIFEST.json").read_text(encoding="utf-8"))
errors=[]
for item in lock["locked_files"]:
    p=ROOT/item["path"]
    if not p.exists():
        errors.append({"path":item["path"],"error":"missing"})
        continue
    sha=hashlib.sha256(p.read_bytes()).hexdigest()
    if sha!=item["sha256"]:
        errors.append({"path":item["path"],"error":"hash_mismatch","expected":item["sha256"],"actual":sha})
print(json.dumps({"status":"PASS" if not errors else "FAIL","errors":errors},ensure_ascii=False,indent=2))
sys.exit(0 if not errors else 1)
