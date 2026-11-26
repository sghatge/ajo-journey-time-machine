from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field

Consent = Literal["granted", "denied", "pending", "unknown"]

class CustomerEvent(BaseModel):
    event_id: str
    profile_id: str
    event_type: str
    occurred_at: datetime
    consent: Consent = "unknown"
    channel: Literal["email", "push", "sms"] = "email"
    opted_out: bool = False
    attributes: dict = Field(default_factory=dict)

class JourneyNode(BaseModel):
    id: str
    kind: Literal["entry", "condition", "channel", "exit"]
    next: list[str] = Field(default_factory=list)
    channel: str | None = None
    requires_consent: bool = True

class SimulationResult(BaseModel):
    run_id: str
    seed: int
    input_events: int
    eligible_profiles: int
    excluded_profiles: int
    projected_actions: int
    findings: list[str]
    profile_paths: dict[str, list[str]]
