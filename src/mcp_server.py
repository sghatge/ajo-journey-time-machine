import json
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from .simulator import parse_events, simulate
from .risk import assess_risk
from .audit import append_audit

mcp = FastMCP("ajo-journey-time-machine")

@mcp.tool()
def run_synthetic_simulation(seed: int = 42) -> dict:
    """Run the bundled synthetic event fixture through the local shadow simulator."""
    root = Path(__file__).resolve().parents[1]
    rows = json.loads((root / "data" / "sample_events.json").read_text(encoding="utf-8"))
    result = simulate(parse_events(rows), seed=seed)
    risk = assess_risk(result)
    append_audit({"run_id": result.run_id, "risk": risk, "mode": "synthetic"}, path=root / "audit.jsonl")
    return {"simulation": result.model_dump(mode="json"), "risk": risk}

if __name__ == "__main__":
    mcp.run()
