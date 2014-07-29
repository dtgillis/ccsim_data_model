#!/bin/bash

ROOT_DIR=/home/dtgillis/workspace/ccsimUI


cd ${ROOT_DIR}

echo "dump experiment_data tables"

python2 manage.py sqlclear experiment_data | python2 manage.py dbshell

echo "rebuilding database"

python2 manage.py syncdb

echo "loading parameters"

python2 manage.py loaddata experiment/data/parameters.initial.json

echo "loading software"

python2 manage.py loaddata experiment/data/software.initial.json

echo "loading gev model table"

python2 manage.py loaddata experiment/data/gev_models.json

#
#echo "loading sensitive data table"
#
#python2 manage.py loaddata sensitive/data/sensitivity.json





