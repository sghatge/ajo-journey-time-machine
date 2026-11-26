from .models import SimulationResult

def assess_risk(result: SimulationResult) -> dict:
    total = result.eligible_profiles + result.excluded_profiles
    projected = result.projected_actions
    findings = list(result.findings)
    if result.excluded_profiles:
        severity = "HIGH" if result.excluded_profiles / max(total, 1) >= 0.25 else "MEDIUM"
    else:
        severity = "LOW"
    if projected >= 1000:
        severity = "HIGH"
        findings.append("Projected action volume is at least 1,000 in this synthetic run")
    return {"severity": severity, "profiles_evaluated": total, "projected_actions": projected, "excluded_profiles": result.excluded_profiles, "exclusion_rate": round(result.excluded_profiles / max(total, 1), 4), "findings": findings, "decision": "HUMAN_REVIEW_REQUIRED" if severity != "LOW" else "SIMULATION_ONLY"}
