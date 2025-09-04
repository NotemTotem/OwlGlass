import os
command = '''.venv\\Scripts\\python.exe "Toolscripts\\accountfinder.py" -e "jaydenoooo@icloud.com" --json --development'''

e = os.popen(command)
output = e.readlines()

for line in output: 
    print(line,end='')