from collections import defaultdict
from .models import CustomerEvent, JourneyNode, SimulationResult

DEFAULT_JOURNEY = [
    JourneyNode(id="entry", kind="entry", next=["consent_check"]),
    JourneyNode(id="consent_check", kind="condition", next=["email_step", "exit"]),
    JourneyNode(id="email_step", kind="channel", channel="email", next=["exit"]),
    JourneyNode(id="exit", kind="exit"),
]

def simulate(events: list[CustomerEvent], seed: int = 42, journey=None) -> SimulationResult:
    by_profile = defaultdict(list)
    for event in sorted(events, key=lambda e: (e.occurred_at, e.event_id)):
        by_profile[event.profile_id].append(event)
    paths, findings = {}, []
    eligible = excluded = projected = 0
    for profile_id, profile_events in sorted(by_profile.items()):
        latest = profile_events[-1]
        path = ["entry", "consent_check"]
        if len({e.event_id for e in profile_events}) != len(profile_events):
            findings.append(f"{profile_id}: duplicate event identifiers detected")
        if latest.opted_out or latest.consent != "granted":
            excluded += 1
            reason = "opted out" if latest.opted_out else f"consent={latest.consent}"
            findings.append(f"{profile_id}: excluded because {reason}")
            path.append("exit")
        else:
            eligible += 1
            projected += 1
            path.extend(["email_step", "exit"])
        paths[profile_id] = path
    if not events:
        findings.append("No input events supplied; no profiles evaluated")
    return SimulationResult(run_id=f"shadow-{seed}-{len(events)}", seed=seed, input_events=len(events), eligible_profiles=eligible, excluded_profiles=excluded, projected_actions=projected, findings=findings, profile_paths=paths)

def parse_events(rows: list[dict]) -> list[CustomerEvent]:
    return [CustomerEvent.model_validate(row) for row in rows]
