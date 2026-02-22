default:
  @just --list

pre-commit:
  uv run pre-commit install --install-hooks

pre-commit-check:
  uv run pre-commit run --all-files

test:
  uv run scripts/test-custom-skills.py

sync-skills:
  uv run scripts/sync-custom-skills.py sync

check-skills:
  uv run scripts/sync-custom-skills.py check

checks:
  uv run pre-commit run --all-files
  uv run scripts/test-custom-skills.py
  uv run scripts/run-skill-evals.py
