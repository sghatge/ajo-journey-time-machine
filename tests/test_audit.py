from src.audit import append_audit, verify_audit

def test_hash_chain_detects_tampering(tmp_path):
    path = tmp_path / "audit.jsonl"
    append_audit({"action": "simulation"}, path)
    assert verify_audit(path)
    path.write_text(path.read_text().replace("simulation", "tampered"))
    assert not verify_audit(path)
