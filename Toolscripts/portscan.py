import socket
import threading
import argparse

#dictionary of ports and common services and the requests that will make the service send a banner response
#"common port":["common service", "request to get banner"]
PORT_PROBE_DICTIONARY = {
    20: ["FTP", b"\x00"],
    21: ["FTP", b"\r\n"],
    22: ["SSH", b"\r\n"],
    23: ["Telnet", b"\r\n"],
    25: ["SMTP", b"\r\n"],
    53: ["DNS", b"\x00"],
    80: ["HTTP", b"HEAD / HTTP/1.0\r\n\r\n"],
    88: ["Kerberos", b"\x00"],
    110: ["POP3", b"\r\n"],
    135: ["MSRPC", b"\x00"],
    161: ["SNMP",
        b"\x30\x26\x02\x01\x01\x04\x06\x70\x75\x62\x6c\x69\x63"
        b"\xa0\x19\x02\x04\x71\x1d\x9f\x25\x02\x01\x00\x02\x01"
        b"\x00\x30\x0b\x30\x09\x06\x05\x2b\x06\x01\x02\x01\x05"
        b"\x00"],
    389: ["LDAP", b"\x00"],
    443: ["HTTPS", b"HEAD / HTTP/1.0\r\n\r\n"],
    445: ["SMB", b"\x00"],
    464: ["Kerberos", b"\x00"],
    587: ["SMTP", b"\r\n"],
    873: ["RSYNC", b"\x00"],
    1194: ["OpenVPN", b"\x00"],
    2049: ["NFS", b"\x00"],
    2483: ["Oracle DB", b"\x00"],
    2484: ["Oracle DB", b"\x00"],
    3306: ["MySQL", b"\x00"],
    3389: ["RDP", b"\x03\x00\x00\x0b\x06\xd0\x00\x00\x12\x34\x00"],
    5432: ["PostgreSQL", b"\x00"],
    5985: ["WinRM (HTTP)", b"GET /wsman HTTP/1.1\r\n\r\n"],
    5986: ["WinRM (HTTPS)", b"GET /wsman HTTP/1.1\r\n\r\n"]
}

#guess the service and the required probe to find banner
def grab_banner(s, port):
    #if there is a known probe then send a request that will probe a banner response
    if PORT_PROBE_DICTIONARY.get(port):
        s.sendall(PORT_PROBE_DICTIONARY.get(port)[1]) #[1] is the banner probe

    try:
        #try to grab banner in chunks
        banner = b""
        while len(banner) < 4096:
            try:
                chunk = s.recv(64)
                if not chunk:
                    break
                banner += chunk
            except socket.timeout:
                break

        if banner:
            output = f"\n - Banner:\n{banner}"
        else:
            raise Exception("Banner returned Null")

    except Exception as err:
        output = f"\n - Failed To Grab Banner: {err}"

        #search for port in dictionary to provide a guess at the service
        service_guess = PORT_PROBE_DICTIONARY.get(port)[0] #[0] is the service name
        if service_guess:
            output += f"\n - Possibly {service_guess}"
        else:
            output += "\n - No Info"

    return output

def scan_port(address, port):
    try:
        #create a socket to connect to port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(TIMEOUT)
            #connect to port
            #connect_ex() returns an integer value that tells about the connection 0 = succesful, other values indicate error codes
            open = s.connect_ex((address, port))

            #if connection succeeds
            if open == 0:
                status = (f"Port {port} is open")

                #store results
                results[PORTS.index(port)] = status + grab_banner(s, port)

    #error handling prevents crashing
    except socket.error as err:
        print(f"Socket error occured while scanning port: {port}\n {err}\n\n")
    except Exception as err:
        print(f"Error occured while scanning port: {port}\n {err}\n\n")\


def main():
    #Parse ports argument for single values, lists, or ranges
    for part in args.p.split(","):
        if "-" in part:
            start, end = part.split("-")
            PORTS.extend(range(int(start), int(end) + 1))
        else:
            PORTS.append(int(part))
    PORTS = sorted(set(PORTS))

    #define blank array so threads can store scan results in order of port
    global results
    results = [None] * len(PORTS)

    #list to reference each thread
    threads = []
    #start a thread for each port
    for port in PORTS:
        t = threading.Thread(target=scan_port, args=[ADDRESS, port])
        #add threads to a list so we can iterate them later
        threads.append(t)
        t.start()

    #wait for threads to finish before continuing
    for t in threads:
        t.join()

    #print results
    for result in results:
        if result:
            print(result)

#take arguments from command flags to define static variables
parser = argparse.ArgumentParser()

parser.add_argument("-a", help="Target address")
parser.add_argument("-t", type=int, default=3, help="Socket timeout in seconds (default: 3)")
parser.add_argument("-p", default="0-999", help="Port(s) to scan (default: 0-999). Examples: 22,80,443 or 20-30")

#parse arguments
args = parser.parse_args()

#set static variables
ADDRESS = args.a
TIMEOUT = args.t
PORTS = []

if __name__ == "__main__":
    main()
