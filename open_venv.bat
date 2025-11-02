if exist .venv\Scripts\ (
  set "venv_path=%CD%\.venv\Scripts\activate" 
) else (
	
  set "venv_path=%CD%\.venv\bin\Activate.ps1" 
)

powershell -file %venv_path%