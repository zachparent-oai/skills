#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

echo "==> lint: validate custom skill structure and markdown style"
python3 scripts/validate-custom-skills.py

echo "==> validate: run quick_validate on .custom skills"
for skill in .custom/{zach-stack,init-repo,agentify-repo,configure-codex}; do
  if [ -d "$skill" ]; then
    python3 skills/.system/skill-creator/scripts/quick_validate.py "$skill"
  fi
done

echo "PASS: custom skill lint/tests complete"
