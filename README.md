# 🧭 OPSFORGE — AJO Journey Time Machine

[![Quality Gate](https://github.com/sghatge/ajo-journey-time-machine/actions/workflows/ci.yml/badge.svg)](https://github.com/sghatge/ajo-journey-time-machine/actions/workflows/ci.yml) ![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white) ![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?logo=streamlit&logoColor=white) ![License](https://img.shields.io/badge/license-MIT-green)

🚀 **Live demo:** [ajo-journey-time-machine.streamlit.app](https://ajo-journey-time-machine.streamlit.app/) · **Source:** [GitHub repository](https://github.com/sghatge/ajo-journey-time-machine)

**A deterministic, synthetic-data-first shadow simulator for customer journey orchestration.** Explore consent gates, opt-out handling, duplicate-event signals, projected actions, risk heuristics and hash-chained audit evidence through a polished Streamlit control room and a read-only MCP tool.

> **Safety boundary:** This is an independent assurance prototype. It does not connect to Adobe Experience Platform (AEP) or Adobe Journey Optimizer (AJO), is not Adobe-certified, and cannot publish, pause, send or activate campaigns. Results are advisory and require human review.

## Live product\n\nOpen the hosted [Streamlit application](https://ajo-journey-time-machine.streamlit.app/) to explore the synthetic scenario lab. The public demo uses bundled synthetic events only; do not enter real customer or production data.\n\n## Product experience
- **Control-room UI:** dark Streamlit workspace with scenario selection, run metrics, risk summary and exportable evidence.
- **Scenario lab:** baseline, consent pressure, opt-out pressure and duplicate-event test scenarios.
- **Deterministic engine:** repeatable evaluation of the bundled synthetic event fixture.
- **Fail-closed eligibility:** unknown, pending or denied consent is excluded; opt-outs are excluded.
- **Explainability:** profile paths and findings are visible for review.
- **Audit trail:** append-only JSONL records linked by SHA-256 hashes, with integrity verification.
- **MCP surface:** read-only `run_synthetic_simulation` tool for local agent experimentation.
- **Quality gate:** GitHub Actions runs pytest and Python compilation checks on pushes and pull requests.

## Project documentation
- [Architecture and data flow](docs/architecture.md)
- [Portfolio case study](docs/portfolio-case-study.md)
- [Changelog](CHANGELOG.md)
- [v0.1.0 release notes](RELEASE_NOTES_v0.1.0.md)

## Quick start — Windows PowerShell
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Run tests with `python -m pytest -q`. Run the MCP server with `python -m src.mcp_server`.

## Deploy on Streamlit Community Cloud
1. Push this repository to GitHub.
2. Sign in at [share.streamlit.io](https://share.streamlit.io/) with GitHub.
3. Select **Create app**, repository `sghatge/ajo-journey-time-machine`, branch `main`, main file `app.py`.
4. Deploy. No Adobe credentials or secrets are needed for this synthetic-only MVP.

Platform availability, limits and terms can change; verify current terms before relying on hosted deployment for business-critical use.

## Design principles
1. Synthetic by default — no production customer data or direct identifiers.
2. Fail closed — missing or non-granted consent does not pass eligibility.
3. Explainable — exclusions and findings are surfaced.
4. Deterministic — same fixture and seed produce the same result.
5. Human authority — simulation never grants deployment permission.

## Known MVP limitations
This first release models a deliberately small subset of journey behavior. The YAML journey file is illustrative and is not yet a full executable graph interpreter. The simulator is not a complete AJO emulator, does not reproduce all Adobe runtime semantics, and does not establish production safety. Risk is a transparent heuristic, not a calibrated probability. Audit files on ephemeral hosting are demo evidence only; use a secured append-only store for durable evidence.

## Roadmap
- [x] Synthetic fixture and deterministic simulation core
- [x] Consent and opt-out fail-closed checks
- [x] Risk summary and profile trace view
- [x] Hash-chain audit evidence
- [x] Streamlit scenario lab and JSON export
- [x] GitHub Actions quality gate
- [ ] Executable journey graph and branch validation
- [ ] Explicit timezone and duplicate-event adversarial test coverage
- [ ] Policy-as-code rules and versioned scenario packs
- [ ] Signed, durable audit evidence and deployment hardening

## License
MIT — see `LICENSE`.
