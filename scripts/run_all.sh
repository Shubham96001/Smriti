#!/usr/bin/env bash
set -euo pipefail

python -m pytest -q
python scripts/security_audit.py
(cd frontend && npm run build)