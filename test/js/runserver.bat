setlocal
start "" http://localhost:8888/test/js/qunit.html?coverage
cd ../..
SET cmd="python -V"
FOR /F "tokens=*" %%i IN (' %cmd% ') DO SET ver=%%i
IF "%ver:~0,8%" == "Python 3" (
    python -m http.server 8888
) ELSE (
    python -m SimpleHTTPServer 8888
)
