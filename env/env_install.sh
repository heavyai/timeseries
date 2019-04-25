#!/usr/bin/env bash
set -e

ENVNAME="tsf-tst"
ENVS=$(conda env list | awk '{print $1}' )
if [[ $ENVS = *"$ENVNAME"* ]];
then
    printf "\n[TSF] Conda env exists.\n"
else
    printf "\n[TSF] Creating conda environment...\n"
    conda env create --name $ENVNAME --file env/py36_test.yml
fi    

printf "\n[TSF] Activating conda environment...\n"
source activate $ENVNAME

printf "\n[TSF] Testing environment…\n"
python -c "import pymapd; print(dir(pymapd))"
python -c "import clipper_admin; print(dir(clipper_admin))"
python -c "import fbprophet; print(dir(fbprophet))"

printf "\n[TSF] Environment setup complete! Run server via \`bash start.sh\`.\n"