#!/bin/bash
phantomjs run-qunit.js http://127.0.0.1:8888/test/js/qunit.html\?coverage
mv jscoverage.pdf ../../docs/jscoverage.pdf
