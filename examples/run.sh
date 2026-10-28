#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
PYTHONPATH=src python -m gbt_git_write info
PYTHONPATH=src python -m gbt_git_write check --payload '{"paths": "<在此填写>", "message": "<在此填写>"}'
PYTHONPATH=src python -m gbt_git_write run   --payload '{"paths": "<在此填写>", "message": "<在此填写>"}'
