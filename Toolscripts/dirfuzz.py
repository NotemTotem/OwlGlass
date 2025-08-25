import socket
import threading

HOST = "youtube.com"
WORDLIST = open("common.txt")
PORT = 80
TIMEOUT = 3
FOLLOW_REDIRECTS = True
MAX_RECURSION = 2

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
            if code < 400 or code >= 500:
                print(f"\n{host}/{path} - {code}")
            #redirect codes we will follow the redirect
            if code >= 300 and code < 400 and FOLLOW_REDIRECTS and MAX_RECURSION <= recursion_count:
                #split the response into lines so we can find the location header
                response_array = response.split(b'\r\n')
                for line in response_array:
                    #find location header and store the redirect location
                    if line[:10] == b"Location: ":
                        print("LOCATION FOUND")
                        location = line[10:].decode("UTF-8")
                        #split location so we can seperate host path and port from the url
                        locationsplit = location.split('/', 3)

                        redirect_path = locationsplit[3]

                        redirect_host_port = locationsplit[2]
                        #if a port is specified we split it into the host and the port
                        if ":" in redirect_host_port:
                            redirect_host = redirect_host_port.split(":")[0]
                            redirect_port = int(redirect_host_port.split(":")[1])
                        #if no port use port 80
                        else:
                            redirect_port = 80
                            redirect_host = redirect_host_port

                        print(f"Redirected to {location}")

                        #recursivley follow redirects
                        fuzz_dir(redirect_host, redirect_path, redirect_port, n+1)

                        #break so we dont continue the loop after we found the location header
                        break
            elif recursion_count > 10:
                print("Max recusions reached: Stopping at path")

    #error handling prevents crashing
    except socket.error as err:
        print(f"Socket error occured while fuzzing dir: {path}\n {err}\n\n")
    except Exception as err:
        print(f"Error occured while fuzzing dir: {path}\n {err}\n\n")\

#list to reference each thread
threads = []
#start a thread for each port
for word in WORDLIST:
    t = threading.Thread(target=fuzz_dir, args=[HOST, word, PORT, 0])
    #add threads to a list so we can iterate them later
    threads.append(t)
    t.start()
