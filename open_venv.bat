@echo off
if exist .venv\Scripts\ (
  set "venv_path=%CD%\.venv\Scripts\activate.bat"
  call "%venv_path%"

) else (
  set "venv_path=%CD%\.venv\bin\Activate.ps1"
  powershell -NoExit -ExecutionPolicy Bypass -file "%venv_path%"
)

if exist .venv\Scripts\ (
  set "venv_path=%CD%\.venv\Scripts\activate.bat"
  call "%venv_path%"

) else (
  set "venv_path=%CD%\.venv\bin\Activate.ps1"
  powershell -NoExit -ExecutionPolicy Bypass -file "%venv_path%"
)
