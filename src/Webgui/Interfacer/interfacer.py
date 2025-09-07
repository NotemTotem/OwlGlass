import os

def find_accounts(target,type):
    if type and type =="email":
        command = f'''.venv\\Scripts\\python.exe "Toolscripts\\accountfinder.py" -e "{target}"'''
        e = os.popen(command)
        output = e.readlines()
        return output
