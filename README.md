# timeseries

## Prerequisites

Should have [docker](https://docs.docker.com/install/) and [omnisci-core](https://github.com/omnisci/mapd-core) up and running on system/ server accessible by machine running TSF server.  

## Install
Clone the repository on to your machine and from your project directory, do the following:
Get a conda installation with (Miniconda)[https://docs.conda.io/en/latest/miniconda.html] and virtual environment setup:

    bash ./env/env_setup.sh

## Start Server

    bash ./start.sh

Logs are stored at `timeseries/log.log`

## Example Notebooks
Demo notebooks are available at `notebooks/`. Make sure the server is running before running the notebooks. 
