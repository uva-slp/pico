#!/bin/bash
cd ../..
coverage3 run app/manage.py test
coverage3 report -m
coverage3 html
rm -rf pico # new uploads directory created here ; delete it
