default:
  @echo "Run: just test"

test:
  uv run scripts/test-custom-skills.py

sync-custom-skills:
  uv run scripts/sync-custom-skills.py

verify-mirror:
  uv run scripts/verify-custom-skill-mirror.py
