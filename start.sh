#!/usr/bin/env bash
set -e

ENVNAME="tsf-tst"
echo "[TSF] Starting server…"
echo "You can watch server output with \`tail -f timeseries/log.log\`"
source activate $ENVNAME
python timeseries/forecast.py