import os
command = '''.venv\Scripts\python.exe "Toolscripts\\accountfinder.py" -e "jaydenoooo@icloud.com"'''

e = os.popen(command)
output = e.readlines()

for line in output: 
    print(line,end='')