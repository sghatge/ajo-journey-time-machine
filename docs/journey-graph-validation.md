# Journey graph validation

The v0.2.0 development track introduces a structural validator for the illustrative YAML journey definition.

## What it checks

- Exactly one entry node and consistency with the declared entry ID
- Unique, non-empty node IDs
- Supported node kinds and channel types
- Existing transition targets and no duplicate outgoing edges
- Minimum branch count for condition nodes
- No outgoing edges from exit nodes
- Reachability from the declared entry node
- Cycles surfaced as warnings for human review

## Safety and scope

The validator checks graph structure only. It does not execute a customer journey, interpret Adobe Journey Optimizer runtime semantics, evaluate production policy, or activate a campaign. Cycles are warnings rather than automatic failures because intentional loops may exist; loop termination must be reviewed by a human.

Run tests with:

```powershell
python -m pytest -q
```
