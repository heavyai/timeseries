#!/usr/bin/env bash
set -e

if hash conda 2>/dev/null
then
	printf '\n[TSF] Conda is already installed.\n'
else
    UNSUPPORTED="UnSupported"
    LINUX="Linux"
    MACOS="MacOs"
    systemOut="$(uname -s)"
    case "${systemOut}" in
        Linux*) machine=$LINUX;;
        Darwin*) machine=$MACOS;;
        *) machine=$UNSUPPORTED
    esac

    if [[ "$machine" -eq "$LINUX" ]];
    then
        printf "\n[TSF] Downloading (mini)conda install script for linux (it's ~42MB)…\n"
        curl -fS https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh > ~/miniconda.sh
    elif [[ "$machine" -eq "$MACOS" ]];
    then
        printf "\n[TSF] Downloading (mini)conda install script for macos (it's ~33MB)…\n"
        curl -fS https://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh > ~/miniconda.sh
    elif [[ "$machine" -eq "$UNSUPPORTED" ]];
    then
        printf "\n[TSF] Installations are only supported for linux and MacOs.\n"
        exit 0;
    else
        printf "\n[TSF] Unexpected error. Aborting installation.\n"
        exit 1;
    fi

    printf "\n[TSF] Installing (mini)aconda…\n"
    bash ~/miniconda.sh -b -p $HOME/Miniconda3
    PATH=$PATH:$HOME/Miniconda3/bin
    rm ~/miniconda.sh
    if [ -f ~/.bashrc ]; then
        source ~/.bashrc
    fi
    printf '\n[TSF] Conda successfully installed.\n'
fi
printf "\n[TSF] Should see path to conda:\n"
which conda

bash ./env/env_setup.sh
