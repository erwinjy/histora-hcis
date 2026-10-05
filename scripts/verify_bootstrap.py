from pathlib import Path
import ast,json,sys
ROOT=Path(__file__).resolve().parent.parent
errors=[]
required=[
"backend/hcis/main.py","backend/hcis/domain/models.py","backend/hcis/domain/contracts.py",
"backend/hcis/adapters/contracts.py","backend/hcis/model_control/contracts.py",
"backend/hcis/acquisition/contracts.py","backend/hcis/storage/contracts.py",
"frontend/src/App.tsx","frontend/src-tauri/tauri.conf.json",
"CODE_LOCK_MANIFEST.json","RUN_AGENT_PROMPT.txt"
]
for rel in required:
    if not (ROOT/rel).exists(): errors.append("missing:"+rel)
for p in (ROOT/"backend/hcis").rglob("*.py"):
    try: ast.parse(p.read_text(encoding="utf-8"))
    except Exception as e: errors.append(f"syntax:{p.relative_to(ROOT)}:{e}")
models=(ROOT/"backend/hcis/domain/models.py").read_text(encoding="utf-8")
for table in ["sources","source_versions","source_locations","claims","fact_candidates","evidence",
              "source_relations","textual_variants","observations","provider_profiles","model_profiles",
              "research_questions","hypotheses","golden_cases","research_runs"]:
    if f'"{table}"' not in models: errors.append("missing_table:"+table)
print(json.dumps({"status":"PASS" if not errors else "FAIL","errors":errors},ensure_ascii=False,indent=2))
sys.exit(0 if not errors else 1)
