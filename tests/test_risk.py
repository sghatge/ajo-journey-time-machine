import json
from pathlib import Path
from src.simulator import parse_events, simulate
from src.risk import assess_risk

def test_exclusions_raise_review():
    rows = json.loads((Path(__file__).parents[1] / "data/sample_events.json").read_text())
    report = assess_risk(simulate(parse_events(rows)))
    assert report["severity"] in {"MEDIUM", "HIGH"}
    assert report["decision"] == "HUMAN_REVIEW_REQUIRED"
