#!/bin/bash
phantomjs run-qunit.js file://`pwd`/qunit.html\?coverage
mv jscoverage.pdf ../../docs/jscoverage.pdf
