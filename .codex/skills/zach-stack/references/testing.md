# Testing conventions (`zach-stack`)

## Baseline expectations

- Add targeted unit tests for new logic.
- Add integration tests for boundaries (API, persistence, worker interfaces).
- Add at least one end-to-end path for critical flows.

## Frontend checks

- For UI work, include interaction-level validation against real page behavior (manual Playwright flow check and automated checks where feasible).

## Docs/test coupling

- Every major behavior change should include an updated doc entry describing intent and validation command.
- Avoid relying on broad integration tests only; use focused tests for failure isolation.
