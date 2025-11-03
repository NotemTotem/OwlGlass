import socket
import threading
import argparse
import os
from pathlib import Path

wordlist_dir = 'static/resources/wordlists'
def chunked_recv(s):
    #recieve response in chunks until the end of the headers, to save time and memory
    response = b""
    while b"\r\n\r\n" not in response:
        chunk = s.recv(256)
        if not chunk:
            break
        response += chunk

    return response

#parse a response to find the location of a rediret
def locate_redirect(response):
    #split the response into lines so we can find the location header
    lines = response.split(b'\r\n')
    for line in lines:
        #find location header and store the redirect location
        if line[:10] == b"Location: ":
            location = line[10:].decode("UTF-8")
            #split location so we can seperate host path and port from the url
            location_split = location.split('/', 3)

            if len(location_split) > 3:
                path = location_split[3]
            else:
                path = ""

            #if a port is specified we have to define a host and a port
            if ":" in location_split[2]:
                #split it into host and port
                host_and_port = location_split[2].split(":")

                host = host_and_port[0]
                port = int(host_and_port[1])
            #if not use port 80
            else:
                host = location_split[2]
                port = 80

            print(f"Redirected to {location}")

            return host, path, port

def fuzz_sub(host, subdomain, port, recursion_count):
    try:
        #create a socket to connect to port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(TIMEOUT)

            subdomain = subdomain.strip("\r\n")

            full_url = subdomain+"."+host

            #connect to server
            s.connect((full_url, port))

            #send get request to recieve a response
            s.sendall("GET / HTTP/1.0\r\n\r\n".encode())
            response = chunked_recv(s)

            if response:
                code = int(response[9:12])
                #not found code gets filtered out
                if code not in range(400, 500):
                    print(f"\n{full_url} - {code}")
    #error handling prevents crashing
    except socket.error as err:
        #if socket error occurs it is likely that the subdomain doesnt exist
        return
    except Exception as err:
        print(f"Error occured while fuzzing subdomain: {subdomain}\n {err}\n\n")

def fuzz_vhost(host, vhost, port, recursion_count):
    try:
        #create a socket to connect to port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(TIMEOUT)

            vhost = vhost.strip("\r\n")

            host_header = vhost+"."+host

            ip_address = socket.gethostbyname(host)

            #connect to server
            s.connect((ip_address, port))

            #send get request to recieve a response
            s.sendall(f"GET / HTTP/1.0\r\n Host: {host_header}\r\n\r\n".encode())
            response = chunked_recv(s)

            if response:
                code = int(response[9:12])
                #not found code gets filtered out
                if code not in range(400, 500):
                    print(f"\n{host_header} - {code}")

    #error handling prevents crashing
    except socket.error as err:
        #if socket error occurs it is likely that the vhost doesnt exist
        return
    except Exception as err:
        print(f"Error occured while fuzzing vhost: {vhost}\n {err}\n\n")

def fuzz_dir(host, path, port, recursion_count):
    try:
        #create a socket to connect to port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(TIMEOUT)
            #connect to server
            s.connect((host, port))

            path = path.strip("\r\n")

            #send get request for path
            s.sendall(f"GET /{path} HTTP/1.0\r\n\r\n".encode())
            response = chunked_recv(s)

            if not response:
                print(" - Server did not supply a response")
                return
            #filter response for the HTTP code
            code = int(response[9:12])
            #not found code gets filtered out
            if code not in range(400, 500):
                print(f"\n{host}/{path} - {code}")
            #redirect codes we will follow the redirect
            if code in range(300, 400) and FOLLOW_REDIRECTS and recursion_count <= MAX_RECURSION:
                #parse response to find where to redirect
                redirect_host, redirect_path, redirect_port = locate_redirect(response)

                #recursivley follow redirects
                fuzz_dir(redirect_host, redirect_path, redirect_port, recursion_count+1)

            elif recursion_count > MAX_RECURSION:
                print("Max recusions reached: Stopping")
    #error handling prevents crashing
    except socket.error as err:
        #if socket error occurs it is likely that the subdomain doesnt exist
        return
    except Exception as err:
        print(f"Error occured while fuzzing dir: {path}\n {err}\n\n")

def main():
    #if a wordlist was specified
    if args.w:
        #open wordlist
        WORDLIST = open(args.w)
    #if wordlist not specified set the wordlist for subdomain mode
    if not args.w and SUBDOMAIN_MODE:
            WORDLIST = open(Path(f"{wordlist_dir}/subdomains.txt"))
    #if wordlist not specified set the wordlist for directory fuzz mode
    if not args.w and not SUBDOMAIN_MODE:
            WORDLIST = open(Path(f"{wordlist_dir}/paths.txt"))
    #set target functions
    if SUBDOMAIN_MODE:
        target_function = fuzz_sub
    elif VHOST_MODE:
        target_function = fuzz_vhost
    else:
        target_function = fuzz_dir

    #list to reference each thread
    threads = []
    #start a thread for each port
    for word in WORDLIST:
        t = threading.Thread(target=target_function, args=[HOST, word, PORT, 0])
        #add threads to a list so we can iterate them later
        threads.append(t)
        t.start()

    WORDLIST.close()
#take arguments from command flags to define static variables
parser = argparse.ArgumentParser()

parser.add_argument("-u", help="Target URL")
parser.add_argument("-w", help="Path to wordlist file (default: OwlGlass/static/resources/wordlists/paths.txt)")
parser.add_argument("-p", type=int, default=80, help="Port number (default: 80)")
parser.add_argument("-t", type=int, default=3, help="Socket timeout in seconds (default: 3)")
parser.add_argument("-r", action="store_true", help="Follow HTTP redirects (default: False)")
parser.add_argument("-d", type=int, default=2, help="Maximum recursion depth (default: 2)")
parser.add_argument("--subdomain", action="store_true", help="Fuzz for subdomains not directories (default: False)\n    - switches default wordlist to OwlGlass/static/resources/wordlists/subdomains.txt")
parser.add_argument("--vhost", action="store_true", help="Fuzz for vhosts not directories (default: False)\n    - switches default wordlist to OwlGlass/static/resources/wordlists/subdomains.txt")

#parge arguments
args = parser.parse_args()

#set static variables
HOST = args.u
PORT = args.p
TIMEOUT = args.t
FOLLOW_REDIRECTS = args.r
MAX_RECURSION = args.d
SUBDOMAIN_MODE = args.subdomain
VHOST_MODE = args.vhost

if __name__ == "__main__":
    main()
