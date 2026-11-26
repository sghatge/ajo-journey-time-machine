# Portfolio Case Study — OPSFORGE AJO Journey Time Machine

## Project summary

**AJO Journey Time Machine** is a synthetic-data-first shadow simulator designed to demonstrate how customer journey orchestration can be pressure-tested before operational deployment. It combines a deterministic Python simulation core, a Streamlit control room, explainable risk heuristics, JSON evidence export and a read-only MCP interface.

- **Live demo:** https://ajo-journey-time-machine.streamlit.app/
- **Project site:** https://sghatge.github.io/ajo-journey-time-machine/
- **Source code:** https://github.com/sghatge/ajo-journey-time-machine
- **Category:** Enterprise AI assurance / MarTech governance / journey operations
- **Status:** Released — v0.1.0 ([release notes](https://github.com/sghatge/ajo-journey-time-machine/releases/tag/v0.1.0))

## Problem framing

Journey orchestration changes can create operational and customer-experience risk when consent states, opt-outs, duplicate events or unexpected event sequences are not considered during review. Teams need a repeatable way to inspect scenarios and communicate potential impact without using production customer data or activating campaigns.

## Solution

The prototype provides four synthetic test scenarios:

1. Baseline fixture
2. Consent pressure test
3. Opt-out pressure test
4. Duplicate-event test

The control room presents profile counts, eligibility outcomes, projected actions, risk findings, simplified journey paths, baseline-versus-scenario comparisons and downloadable JSON run evidence.

## Engineering approach

- Python and Pydantic for typed event models and validation
- Deterministic simulation for repeatable test runs
- Streamlit for the interactive control room
- SHA-256 linked JSONL records for local audit-integrity demonstration
- FastMCP interface for local read-only agent experimentation
- pytest and GitHub Actions for automated quality checks

## Demonstrated MVP behavior

The bundled baseline fixture contains five synthetic profiles. In the current baseline model, one profile passes the consent/opt-out eligibility gate and four are excluded. These are fixture outcomes, not customer, campaign or production performance metrics.

The risk panel uses explicit demonstration thresholds. It is an explainable heuristic, not a calibrated risk model or compliance decision.

## Governance and safety boundaries

- No Adobe AEP/AJO connection or Adobe certification is claimed.
- No campaign publish, pause, send or activation action is implemented.
- No real customer data or production identifiers should be used.
- Results are advisory and require human review.
- Local hash-chain evidence is not a substitute for a secured, immutable enterprise audit store.

## Next roadmap

- Implement executable journey graph parsing and branch validation.
- Add timezone-boundary, duplicate-event and event-order adversarial tests.
- Externalize policy rules with versioning and traceable decisions.
- Harden audit storage with signing, retention, access controls and durable storage.
- Expand evaluation coverage before any enterprise integration is considered.

## Portfolio positioning

This project demonstrates practical experience at the intersection of CRM technology, journey orchestration, deterministic testing, AI-agent interfaces and governance-by-design. It is an independent prototype intended to support technical discussion—not a claim of production AJO emulation or certification.
