@echo off
echo -
echo -
powershell -Command "Write-Host 'Starting setup, please be patient.' -ForegroundColor Green"

if not exist .venv (
echo -
echo -
powershell -Command "Write-Host 'Creating virtual environment.' -ForegroundColor Green"
echo -
echo -
python -m venv .venv
)
if exist pyproject.toml (
echo -
echo -
powershell -Command "Write-Host 'Requirements file found. Compiling and syncing packages.' -ForegroundColor Green"
echo -
echo -
.venv\Scripts\pip.exe install .
) else (
echo -
echo -
powershell -Command "Write-Host 'ERROR No pyproject file found.' -ForegroundColor Red"
echo -
echo -
)
powershell -Command "Write-Host 'Setup complete.' -ForegroundColor Green"
echo -
echo -
cmd /k ".venv\Scripts\python.exe src\Webgui\webgui.py"
