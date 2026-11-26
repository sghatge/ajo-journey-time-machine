# OPSFORGE AJO Journey Time Machine v0.1.0

**Release type:** Initial public MVP  
**Live demo:** https://ajo-journey-time-machine.streamlit.app/  
**Repository:** https://github.com/sghatge/ajo-journey-time-machine

## Highlights

- Deterministic synthetic journey simulation
- Consent and opt-out fail-closed checks
- Baseline, consent pressure, opt-out pressure and duplicate-event scenarios
- Streamlit control room with journey visualization
- Baseline comparison, risk findings and profile traces
- SHA-256 linked audit evidence and JSON export
- Read-only MCP simulation tool
- Automated GitHub Actions quality checks

## Important limitations

This is an independent assurance prototype. It does not connect to Adobe Experience Platform or Adobe Journey Optimizer, is not Adobe-certified, and is not a full AJO runtime emulator. It cannot publish, pause, send or activate campaigns. Risk thresholds are illustrative heuristics. Use synthetic data only; all findings require human review.

## Verification

The repository's GitHub Actions quality workflow has passed for the current application feature commit. The release documentation commit should also complete the quality workflow before the GitHub Release is published.
