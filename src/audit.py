import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone

def append_audit(record: dict, path="audit.jsonl") -> dict:
    target = Path(path)
    previous_hash = "GENESIS"
    if target.exists():
        lines = [line for line in target.read_text(encoding="utf-8").splitlines() if line.strip()]
        if lines:
            previous_hash = json.loads(lines[-1])["hash"]
    payload = {"timestamp": datetime.now(timezone.utc).isoformat(), "previous_hash": previous_hash, "record": record}
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    entry = {**payload, "hash": digest}
    with target.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, sort_keys=True) + "\n")
    return entry

def verify_audit(path="audit.jsonl") -> bool:
    target = Path(path)
    if not target.exists():
        return True
    previous_hash = "GENESIS"
    for line in target.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        entry = json.loads(line)
        if entry["previous_hash"] != previous_hash:
            return False
        payload = {k: v for k, v in entry.items() if k != "hash"}
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        if entry["hash"] != hashlib.sha256(canonical.encode("utf-8")).hexdigest():
            return False
        previous_hash = entry["hash"]
    return True
