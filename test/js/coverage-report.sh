#!/bin/bash
phantomjs run-qunit.js file://`pwd`/test/js/qunit.html\?coverage
mv jscoverage.pdf ../../docs/jscoverage.pdf
