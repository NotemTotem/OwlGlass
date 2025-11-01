import os
from pathlib import Path
from sys import platform
if platform == 'linux' or platform == 'linux2':
    python_location = '.venv/bin/python'
else:
    python_location = '.venv/Scripts/python.exe'

python_location = Path(python_location)

def find_accounts(target,type):
    toolscript_location = Path("Toolscripts/accountfinder.py")
    if type and type =="email":
        command = f'''{python_location} {toolscript_location} -e "{target}"'''
        e = os.popen(command)
        output = e.readlines()
        return output


def scan_ports(target, ports):
    toolscript_location = Path("Toolscripts/portscan.py")
    command = f'''{python_location} {toolscript_location} -a "{target}" -p "{ports}"'''
    e = os.popen(command)
    output = e.readlines()
    print(output)
    return output

def dns_lookup(target, dns_records):
    toolscript_location = Path("Toolscripts/DNSLookerUpper.py")
    command = f'''{python_location} {toolscript_location} {target} {" ".join(f"--{dns}" for dns in dns_records)}'''
    print(command)
    e = os.popen(command)
    output = e.readlines()
    print(output)
    return output

def fuzz_dirs(target, recursion_depth, port):
    toolscript_location = Path("Toolscripts/dirfuzz.py")
    command = f'''{python_location} {toolscript_location} -u {target} -p {port} -d {recursion_depth} '''
    print(command)
    e = os.popen(command)
    output = e.readlines()
    print(output)
    return output


def fuzz_subs(target, recursion_depth, port):
    toolscript_location = Path("Toolscripts/dirfuzz.py")
    command = f'''{python_location} {toolscript_location} -u {target} -p {port} -d {recursion_depth} --subdomain'''
    print(command)
    e = os.popen(command)
    output = e.readlines()
    print(output)
    return output

def fuzz_vhosts(target, recursion_depth, port):
    toolscript_location = Path("Toolscripts/dirfuzz.py")
    command = f'''{python_location} {toolscript_location} -u {target} -p {port} -d {recursion_depth} --vhost '''
    print(command)
    e = os.popen(command)
    output = e.readlines()
    print(output)
    return output
