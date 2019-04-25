#!/usr/bin/env bash
set -e

printf "\n[TSF] Loading sample data into omnisci core...\n"

ENVNAME="tsf-tst"
ENVS=$(conda env list | awk '{print $1}' )
if [[ $ENVS = *"$ENVNAME"* ]];
then
    source activate $ENVNAME
else
    printf "\n[TSF] Conda env $ENVNAME does not exist. Please run bash \`./env/env_setup.sh\ first.\`\n"
    exit 1;
fi
python sample_data/sample_data.py