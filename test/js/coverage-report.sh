#!/bin/bash
phantomjs test/js/run-qunit.js file://`pwd`/test/js/qunit.html\?coverage
mv jscoverage.pdf ../../docs/jscoverage.pdf
