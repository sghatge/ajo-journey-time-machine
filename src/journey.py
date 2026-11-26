"""Structural validation for synthetic journey graph definitions."""
from __future__ import annotations

from collections import defaultdict, deque
from typing import Any


ALLOWED_KINDS = {"entry", "condition", "channel", "exit"}
ALLOWED_CHANNELS = {"email", "push", "sms"}


def validate_journey_graph(definition: dict[str, Any]) -> dict[str, Any]:
    """Validate graph structure without executing or activating a journey.

    Returns a stable report containing valid, errors, warnings and node_count.
    Cycles are warnings because looping journeys may be intentional; unreachable
    nodes and invalid references are errors.
    """
    errors: list[str] = []
    warnings: list[str] = []
    nodes = definition.get("nodes", [])
    if not isinstance(nodes, list) or not nodes:
        return {
            "valid": False,
            "errors": ["Journey must contain a non-empty nodes list"],
            "warnings": [],
            "node_count": 0,
        }

    ids: list[str] = []
    by_id: dict[str, dict[str, Any]] = {}
    for index, node in enumerate(nodes):
        if not isinstance(node, dict):
            errors.append(f"Node at index {index} must be a mapping")
            continue
        node_id = node.get("id")
        if not isinstance(node_id, str) or not node_id.strip():
            errors.append(f"Node at index {index} has a missing or blank id")
            continue
        if node_id in by_id:
            errors.append(f"Duplicate node id: {node_id}")
            continue
        ids.append(node_id)
        by_id[node_id] = node

    entries = [node_id for node_id, node in by_id.items() if node.get("kind") == "entry"]
    if len(entries) != 1:
        errors.append(f"Journey must contain exactly one entry node; found {len(entries)}")
    declared_entry = definition.get("entry")
    if declared_entry not in by_id:
        errors.append(f"Declared entry node does not exist: {declared_entry}")
    elif entries and declared_entry != entries[0]:
        errors.append(f"Declared entry '{declared_entry}' is not the entry node '{entries[0]}'")

    adjacency: dict[str, list[str]] = defaultdict(list)
    for node_id, node in by_id.items():
        kind = node.get("kind")
        if kind not in ALLOWED_KINDS:
            errors.append(f"{node_id}: unsupported kind '{kind}'")
        targets = node.get("next", [])
        if not isinstance(targets, list):
            errors.append(f"{node_id}: next must be a list")
            targets = []
        if kind == "exit" and targets:
            errors.append(f"{node_id}: exit nodes cannot have outgoing transitions")
        if kind in {"entry", "channel"} and not targets:
            errors.append(f"{node_id}: {kind} nodes must have at least one outgoing transition")
        if kind == "condition" and len(targets) < 2:
            errors.append(f"{node_id}: condition nodes must define at least two branches")
        if kind == "channel" and node.get("channel") not in ALLOWED_CHANNELS:
            errors.append(f"{node_id}: channel must be one of email, push or sms")
        if len(targets) != len(set(t for t in targets if isinstance(t, str))):
            errors.append(f"{node_id}: duplicate outgoing transition")
        for target in targets:
            if not isinstance(target, str) or target not in by_id:
                errors.append(f"{node_id}: transition target does not exist: {target}")
            else:
                adjacency[node_id].append(target)

    reachable: set[str] = set()
    if declared_entry in by_id:
        queue = deque([declared_entry])
        while queue:
            current = queue.popleft()
            if current in reachable:
                continue
            reachable.add(current)
            queue.extend(adjacency.get(current, []))
    unreachable = sorted(set(by_id) - reachable)
    if unreachable:
        errors.append("Unreachable nodes: " + ", ".join(unreachable))

    # A cycle is surfaced for human review, not automatically rejected.
    visiting: set[str] = set()
    visited: set[str] = set()
    has_cycle = False

    def visit(node_id: str) -> None:
        nonlocal has_cycle
        if node_id in visiting:
            has_cycle = True
            return
        if node_id in visited:
            return
        visiting.add(node_id)
        for target in adjacency.get(node_id, []):
            visit(target)
        visiting.remove(node_id)
        visited.add(node_id)

    for node_id in by_id:
        visit(node_id)
    if has_cycle:
        warnings.append("Cycle detected; review loop exit conditions before operational use")

    if not any(node.get("kind") == "exit" for node in by_id.values()):
        errors.append("Journey must contain at least one exit node")

    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "node_count": len(by_id),
    }
