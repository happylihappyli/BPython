@echo off
echo Running all BPython tests...

echo.
echo ==========================================
echo Running test_stdlib_basic.bpy...
src\Python-3.12.2\PCbuild\amd64\python.exe test_stdlib_basic.bpy
if %ERRORLEVEL% NEQ 0 goto :error

echo.
echo ==========================================
echo Running test_stdlib_data.bpy...
src\Python-3.12.2\PCbuild\amd64\python.exe test_stdlib_data.bpy
if %ERRORLEVEL% NEQ 0 goto :error

echo.
echo ==========================================
echo Running test_stdlib_concurrency.bpy...
src\Python-3.12.2\PCbuild\amd64\python.exe test_stdlib_concurrency.bpy
if %ERRORLEVEL% NEQ 0 goto :error

echo.
echo ==========================================
echo Running test_functional.bpy...
src\Python-3.12.2\PCbuild\amd64\python.exe test_functional.bpy
if %ERRORLEVEL% NEQ 0 goto :error

echo.
echo ==========================================
echo Running test_numpy.bpy...
src\Python-3.12.2\PCbuild\amd64\python.exe test_numpy.bpy
if %ERRORLEVEL% NEQ 0 goto :error

echo.
echo ==========================================
echo ALL TESTS PASSED!
goto :eof

:error
echo.
echo TEST FAILED!
exit /b 1
