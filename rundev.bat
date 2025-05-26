@echo off
echo Running mypy...
mypy src
if errorlevel 1 (
    echo Mypy found errors, exiting...
    exit /b 1
)

echo Running Application...
fastapi dev src/fast.py