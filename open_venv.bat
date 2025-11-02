if exist .venv\Scripts\ (
  set "venv_path=%CD%\.venv\Scripts\activate" 
) else (
  set "venv_path=%CD%\.venv\bin\activate" 
)

cmd /k "%venv_path%"