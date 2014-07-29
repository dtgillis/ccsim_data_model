#!/bin/bash

ROOT_DIR=/home/dtgillis/workspace/ccsimUI


cd ${ROOT_DIR}

echo "dumping specificity tables"

python2 manage.py sqlclear specificity | python2 manage.py dbshell

echo "rebuilding database"

python2 manage.py syncdb

echo "loading testmarkerid table"

python2 manage.py loaddata specificity/data/testmarkerid.json

echo "database rebuild with initial specificity info"






