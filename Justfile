default:
  @echo "Run: just test"

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
