#!/bin/bash
URL="http://localhost:8888/test/js/qunit.html?coverage"
cd ../..

if which xdg-open > /dev/null
then
    xdg-open $URL
elif which gnome-open > /dev/null
then
    gnome-open $URL
fi

V=`python -V 2>&1`
if [[ ${V:7:1} =~ ^3 ]] ;
then
    python -m http.server 8888
else
    python -m SimpleHTTPServer 8888
fi
