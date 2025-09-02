import socket
import threading
import argparse

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

            path = location_split[3]

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

#fuzz a path to find error code
def fuzz_dir(host, path, port, recursion_count):
    try:
        #create a socket to connect to port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(TIMEOUT)
            #connect to port
            open = s.connect((host, port))

            path = path.strip("\r\n")

            #send get request for path
            s.sendall(f"GET /{path} HTTP/1.0\r\n\r\n".encode())
            response = s.recv(512)


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
                print("Max recusions reached: Stopping at path")

    #error handling prevents crashing
    except socket.error as err:
        print(f"Socket error occured while fuzzing dir: {path}\n {err}\n\n")
    except Exception as err:
        print(f"Error occured while fuzzing dir: {path}\n {err}\n\n")\

def main():
    #take arguments from command flags to define static variables
    parser = argparse.ArgumentParser()

    parser.add_argument("-u", help="Target URL")
    parser.add_argument("-w", default="../static/resources/wordlists/common.txt", help="Path to wordlist file (default: static/resources/wordlists/common.txt)")
    parser.add_argument("-p", type=int, default=80, help="Port number (default: 80)")
    parser.add_argument("-t", type=int, default=3, help="Socket timeout in seconds (default: 3)")
    parser.add_argument("-r", action="store_true", help="Follow HTTP redirects (default: False)")
    parser.add_argument("-d", type=int, default=2, help="Maximum recursion depth (default: 2)")

    #parge arguments
    args = parser.parse_args()

    #set static variables
    global MAX_RECURSION
    global TIMEOUT
    global FOLLOW_REDIRECTS
    HOST = args.u
    WORDLIST = open(args.w)
    PORT = args.p
    TIMEOUT = args.t
    FOLLOW_REDIRECTS = args.r
    MAX_RECURSION = args.d

    #list to reference each thread
    threads = []
    #start a thread for each port
    for word in WORDLIST:
        t = threading.Thread(target=fuzz_dir, args=[HOST, word, PORT, 0])
        #add threads to a list so we can iterate them later
        threads.append(t)
        t.start()

if __name__ == "__main__":
    main()
