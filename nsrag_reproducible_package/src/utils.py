import json
from pathlib import Path
def load_jsonl(path):
    return [json.loads(l) for l in open(path,encoding="utf-8") if l.strip()]
def ensure_dir(path): Path(path).mkdir(parents=True, exist_ok=True)
