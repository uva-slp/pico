#!/bin/bash
cd ../../app
coverage3 run --source="." manage.py test
coverage3 report --include="$PWD/*" --omit="$PWD/manage.py" -m
coverage3 html -d ../docs/coverage
mv .coverage ../test/python/.coverage
