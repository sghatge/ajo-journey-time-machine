import json
from pathlib import Path
from src.simulator import parse_events, simulate

def test_consent_is_fail_closed():
    rows = json.loads((Path(__file__).parents[1] / "data/sample_events.json").read_text())
    result = simulate(parse_events(rows), seed=7)
    assert result.eligible_profiles == 1
    assert result.excluded_profiles == 4
    assert result.projected_actions == 1

def test_simulation_is_deterministic():
    rows = json.loads((Path(__file__).parents[1] / "data/sample_events.json").read_text())
    events = parse_events(rows)
    assert simulate(events, seed=11).model_dump() == simulate(events, seed=11).model_dump()
