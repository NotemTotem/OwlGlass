import os
command = '''.venv\\Scripts\\python.exe "Toolscripts\\accountfinder.py" -e "jaydenoooo@icloud.com" --json --development'''

e = os.popen(command)
output = e.readlines()

def find_accounts(target,type):
    if type and type =="email":
        command = '''.venv\\Scripts\\python.exe "Toolscripts\\accountfinder.py" -e "{target}" --json --development'''
for line in output: 
    print(line,end='')