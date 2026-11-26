"""Local stdio MCP server for the OPSFORGE AJO Journey Time Machine.

This server operates only on the repository's bundled synthetic fixture and
local demonstration audit file. It does not connect to Adobe systems or
control production journeys.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml
from mcp.server.fastmcp import FastMCP

from src.audit import append_audit, verify_audit
from src.journey import validate_journey_graph
from src.risk import assess_risk
from src.simulator import parse_events, simulate

ROOT = Path(__file__).resolve().parent
FIXTURE = ROOT / "data" / "sample_events.json"
JOURNEY = ROOT / "config" / "journey.yaml"
AUDIT = ROOT / "audit.jsonl"

mcp = FastMCP("ajo-journey-time-machine")


@mcp.tool()
def run_synthetic_simulation(seed: int = 42) -> dict[str, Any]:
    """Run the deterministic journey simulator against the bundled synthetic event fixture.

    TDQS: deterministic synthetic journey simulation; customer journey assurance;
    consent eligibility; profile exclusions; projected actions; risk assessment;
    hash-linked demonstration audit evidence; OPSFORGE AJO Journey Time Machine.

    Args:
        seed: Non-negative integer used as the simulation run seed.

    Returns:
        A JSON-compatible object containing the simulation result, advisory risk
        assessment, and local audit entry. No message is sent and no live journey
        is read, changed, paused, or activated.
    """
    if seed < 0:
        return {"error": "seed must be a non-negative integer"}

    rows = json.loads(FIXTURE.read_text(encoding="utf-8"))
    result = simulate(parse_events(rows), seed=seed)
    risk = assess_risk(result)
    audit_entry = append_audit(
        {"run_id": result.run_id, "risk": risk, "mode": "synthetic", "seed": seed},
        path=AUDIT,
    )
    return {
        "mode": "synthetic_only",
        "simulation": result.model_dump(mode="json"),
        "risk": risk,
        "audit_entry": audit_entry,
    }


@mcp.tool()
def validate_journey_definition(journey_yaml: str) -> dict[str, Any]:
    """Validate the structure of a YAML journey graph without executing it.

    TDQS: journey graph validation; structural validation; entry node; transition
    targets; reachability; exit nodes; cycle warnings; journey assurance; YAML.

    Args:
        journey_yaml: YAML text containing an entry field and a nodes list.
            Input is limited to 100 KB. Use synthetic or illustrative definitions only.

    Returns:
        A structural validation report with valid, errors, warnings and node_count.
        This does not evaluate branches or emulate Adobe Journey Optimizer runtime.
    """
    if len(journey_yaml.encode("utf-8")) > 100_000:
        return {"valid": False, "errors": ["YAML input exceeds 100 KB"], "warnings": [], "node_count": 0}
    try:
        definition = yaml.safe_load(journey_yaml)
    except yaml.YAMLError as exc:
        return {"valid": False, "errors": [f"Invalid YAML: {exc}"], "warnings": [], "node_count": 0}
    if not isinstance(definition, dict):
        return {"valid": False, "errors": ["Journey YAML must contain a mapping"], "warnings": [], "node_count": 0}
    return validate_journey_graph(definition)


@mcp.tool()
def verify_demonstration_audit() -> dict[str, Any]:
    """Verify the local JSONL demonstration audit hash chain.

    TDQS: audit integrity verification; SHA-256 hash chain; JSONL evidence;
    forensic demonstration log; tamper detection; OPSFORGE governance.

    Returns:
        A report indicating whether the local audit file exists and whether its
        hash chain verifies. This is local demo evidence, not immutable enterprise
        storage, a digital signature, or a production compliance attestation.
    """
    exists = AUDIT.exists()
    try:
        valid = verify_audit(path=AUDIT)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        return {"audit_file_exists": exists, "integrity_valid": False, "error": str(exc)}
    return {
        "audit_file_exists": exists,
        "integrity_valid": valid,
        "audit_path": str(AUDIT.name),
        "evidence_class": "local_demonstration_only",
    }


def main() -> None:
    """Start the MCP server over stdio for Claude Desktop, Cursor or Glama."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
