from src.journey import validate_journey_graph


VALID = {
    "entry": "entry",
    "nodes": [
        {"id": "entry", "kind": "entry", "next": ["gate"]},
        {"id": "gate", "kind": "condition", "next": ["email", "exit"]},
        {"id": "email", "kind": "channel", "channel": "email", "next": ["exit"]},
        {"id": "exit", "kind": "exit", "next": []},
    ],
}


def test_valid_graph_passes():
    report = validate_journey_graph(VALID)
    assert report["valid"] is True
    assert report["node_count"] == 4
    assert report["errors"] == []


def test_missing_transition_target_fails():
    graph = {**VALID, "nodes": [VALID["nodes"][0], {"id": "gate", "kind": "condition", "next": ["bad_email", "exit"]}, {"id": "bad_email", "kind": "channel", "channel": "email", "next": ["missing"]}, VALID["nodes"][3]]}
    report = validate_journey_graph(graph)
    assert report["valid"] is False
    assert any("does not exist: missing" in item for item in report["errors"])


def test_condition_requires_two_branches():
    graph = {**VALID, "nodes": [VALID["nodes"][0], {"id": "gate", "kind": "condition", "next": ["exit"]}, VALID["nodes"][2], VALID["nodes"][3]]}
    report = validate_journey_graph(graph)
    assert any("at least two branches" in item for item in report["errors"])


def test_unreachable_nodes_fail():
    graph = {**VALID, "nodes": [*VALID["nodes"], {"id": "orphan", "kind": "exit", "next": []}]}
    report = validate_journey_graph(graph)
    assert any("Unreachable nodes: orphan" in item for item in report["errors"])


def test_cycles_are_reported_for_review():
    graph = {
        "entry": "entry",
        "nodes": [
            {"id": "entry", "kind": "entry", "next": ["loop"]},
            {"id": "loop", "kind": "channel", "channel": "push", "next": ["loop", "exit"]},
            {"id": "exit", "kind": "exit", "next": []},
        ],
    }
    report = validate_journey_graph(graph)
    assert report["valid"] is True
    assert report["warnings"] and "Cycle detected" in report["warnings"][0]
