#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
rm -rf build package.zip
mkdir build
uv pip install -r requirements.txt --target build --quiet
cp config.py net.py discover.py measure.py collect.py weather.py lambda_function.py build/
cd build
zip -r ../package.zip . -x '*.pyc' '__pycache__/*' >/dev/null
echo "built package.zip"