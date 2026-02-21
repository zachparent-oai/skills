default:
  @just --list

pre-commit:
  PRE_COMMIT_HOME=.pre-commit-cache pre-commit install --install-hooks

pre-commit-check:
  PRE_COMMIT_HOME=.pre-commit-cache pre-commit run --all-files

test:
  uv run scripts/test-custom-skills.py

sync-skills:
  uv run scripts/sync-custom-skills.py sync

check-skills:
  uv run scripts/sync-custom-skills.py check

checks:
  uv run scripts/test-custom-skills.py
  uv run scripts/run-skill-evals.py
