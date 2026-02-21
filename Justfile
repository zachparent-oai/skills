default:
  @echo "Run: just test"

pre-commit:
  PRE_COMMIT_HOME=.pre-commit-cache pre-commit install --install-hooks

pre-commit-check:
  PRE_COMMIT_HOME=.pre-commit-cache pre-commit run --all-files

test:
  uv run scripts/test-custom-skills.py

sync-custom-skills:
  uv run scripts/sync-custom-skills.py

agentify-sync:
  uv run scripts/sync-custom-skills.py sync

agentify-check:
  uv run scripts/sync-custom-skills.py check

agentify-status:
  uv run scripts/sync-custom-skills.py check

agentify-checks:
  uv run scripts/test-custom-skills.py
  uv run scripts/run-skill-evals.py
