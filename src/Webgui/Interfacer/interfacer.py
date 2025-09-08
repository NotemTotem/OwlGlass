import os

def find_accounts(target,type):
    if type and type =="email":
        command = f'''.venv\\Scripts\\python.exe "Toolscripts\\accountfinder.py" -e "{target}"'''
        e = os.popen(command)
        output = e.readlines()
        return output


def scan_ports(target, ports):
    command = f'''.venv\\Scripts\\python.exe "Toolscripts\\portscan.py" -a "{target}" -p "{ports}"'''
    e = os.popen(command)
    output = e.readlines()
    print(output)
    return output

def dns_lookup(target, dns_records):
    command = f'''.venv\\Scripts\\python.exe "Toolscripts\\DNSLookerUpper.py" {target} {" ".join(f"--{dns}" for dns in dns_records)}'''
    print(command)
    e = os.popen(command)
    output = e.readlines()
    print(output)
    return output