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
if exist .venv\Scripts\ (
  set "venv_path=%CD%\.venv\Scripts" 
) else (
  set "venv_path=%CD%\.venv\bin" 
)

if exist pyproject.toml (
echo -
echo -
powershell -Command "Write-Host 'Requirements file found. Compiling and syncing packages.' -ForegroundColor Green"
echo -
echo -
<<<<<<< HEAD
.venv\Scripts\pip.exe install .
=======
%venv_path%\pip.exe install .  
>>>>>>> e6960a971d828d289148d77304217e99f193fb6e
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
<<<<<<< HEAD
cmd /k ".venv\Scripts\python.exe src\Webgui\webgui.py"
=======
cmd /k "%venv_path%\python.exe src\Webgui\webgui.py" 
>>>>>>> e6960a971d828d289148d77304217e99f193fb6e
