#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p mlflow/mlartifacts
mlflow server --backend-store-uri "sqlite:///$(pwd)/mlflow/mlruns.db" --default-artifact-root "file://$(pwd)/mlflow/mlartifacts" --host 127.0.0.1 --port 5000
