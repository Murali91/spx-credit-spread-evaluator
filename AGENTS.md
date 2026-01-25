# AGENTS.md — Rules for Autonomous Contributions (Codex)

This repository supports autonomous/semi-autonomous work by coding agents (Codex, etc.).
These rules are **mandatory** for every agent task and PR.

---
## Logic & Specification Authority

All business logic and system behavior must be implemented according to:

- docs/BRD.md  
- docs/Decision_Spec_v0.1.md  
- docs/Data_Sources.md  
- docs/UX_Copy.md  

These documents are the **source of truth** for:
- what the system should do
- how decisions are made
- what constitutes ENTER vs WAIT
- what data sources are used
- how explanations are presented

If there is any conflict between:
- existing code
- agent assumptions
- or implementation ideas

the documents above take precedence.

Agents must **read and understand these documents before coding**.
Do not invent new logic or modify decision rules unless explicitly instructed.

## 0) Prime Directive

**Do not change product scope or output contract.**

- No brokerage integration.
- No trade execution.
- Output must remain strictly:
  - `ENTER` or `WAIT` (exact casing)
  - plus bullet-point explanations and optional risk flags
- Keep architecture testable and minimal.

---

## 1) Branch & PR Discipline

- Work on a **feature branch** (never directly on the default branch).
- One GitHub Issue → one PR.
- PR title format: `[Issue #] <short description>`
- PR description must include:
  - what changed
  - how to run tests
  - any assumptions or limitations

---

## 2) Required Quality Gate (Must Run Before Pushing)

After changes, run:

- `python -m pytest -q`

If tests fail:
- Fix, rerun, repeat until passing.

If new behavior was added:
- Add/adjust tests to cover it.

**No PR should be opened if tests are failing.**

---

## 3) Mandatory Self-Review (At Least 1 Round)

Every task must include **at least one round** of self-review after implementation,
*before* requesting human review or posting “done”.

### Self-Review Checklist (must execute and verify)

**A) Spec & Contract Compliance**
- [ ] Output is strictly `ENTER` or `WAIT` + bullet reasons
- [ ] No extra output formats, no JSON blobs in UI, no additional recommendation words
- [ ] No brokerage integration, no order placement, no user-specific advice

**B) Architecture & Code Health**
- [ ] Engine logic remains in `engine/` (no business logic in Streamlit UI)
- [ ] Data retrieval remains in `data/providers/`
- [ ] Thresholds live in `engine/thresholds.py` (no magic numbers scattered)
- [ ] Types are explicit (`engine/types.py`) and used consistently

**C) Reliability**
- [ ] Graceful handling of missing data (no KeyError crashes)
- [ ] Provider failures do not crash the app; they result in `WAIT` + explanation
- [ ] Streamlit app runs from repo root:
  - `streamlit run app/streamlit_app.py`

**D) Test Integrity**
- [ ] Tests do **not** hit the network
- [ ] External calls (yfinance, requests, etc.) are mocked in unit tests
- [ ] `pytest -q` passes locally

### Self-Review Output (required in PR)
In the PR description (or final task summary), include:

- “Self-review completed: YES”
- A short bullet list of what you checked
- Mention the exact command used to run tests (e.g. `python -m pytest -q`)

---

## 4) One-Loop “Fix → Review → Fix” Rule

When addressing review comments or bugs:

1. Implement the fixes
2. Run the Quality Gate (`pytest`)
3. Perform the Self-Review Checklist (Section 3)
4. If self-review finds issues, fix them and rerun `pytest`
5. Only then push commits / update PR

**At least one full loop is required per task.**

---

## 5) Logging & Explainability Rules

- Explanations shown to users must be concise bullets.
- Keep explanations traceable to factors:
  - Trend
  - Volatility
  - Event risk
  - Skew/liquidity proxy
- Avoid jargon; when used, include a short clarification.

---

## 6) What NOT to Do

- Do not add new features beyond the Issue scope.
- Do not add paid APIs unless the Issue explicitly requests it.
- Do not introduce complex ML models in v0.1.
- Do not refactor unrelated files “for cleanliness” unless required.
- Do not change folder structure without explicit instruction.

---

## 7) Commit Guidelines

- Small, focused commits preferred.
- Commit messages:
  - `Fix: <...>`
  - `Feat: <...>`
  - `Test: <...>`
  - `Docs: <...>`

---

## 8) When Blocked

If you cannot proceed due to missing info:

- Do **not** guess silently.
- Add a short note in the PR description:
  - what is missing
  - what assumption you made (if any)
  - what you recommend next

---

## 9) Definition of Done (for any PR)

A PR is “Done” only if:

- [ ] Issue requirements are implemented
- [ ] `python -m pytest -q` passes
- [ ] Self-review completed and documented
- [ ] Output contract preserved (`ENTER/WAIT + bullets`)
- [ ] No network calls in tests
- [ ] Streamlit app still runs

---
