import dns.resolver
import dns.name
import argparse
import dns.zone
from pprint import pprint

record_types = []
record_info = {}

def queryDns(target_domain, recursion_count, timeout):
    if recursion_count >= 0:
        resolver = dns.resolver.Resolver()
        resolver.timeout = timeout
        new_recursion = []
        target_info = {}
        for record_type in record_types:
            # Perform DNS lookup for the specified domain and record type
            result_info = []
            try:
                answers = resolver.resolve(target_domain, record_type)
            except dns.resolver.NoAnswer: #do something instead of continue with these errors
                continue
            except dns.resolver.NXDOMAIN:
                continue
            except dns.resolver.Timeout:
                continue
            except dns.resolver.NoNameservers:
                continue
            except dns.name.LabelTooLong:
                continue
            # Print the answers
            for rdata in answers:
                result_info.append(rdata.to_text())
                if int(rdata.rdtype) != 6 and int(rdata.rdtype) != 16 : # if not SOA ::: this is stupid 
                    new_recursion.append(rdata.to_text())
                        
            target_info[record_type] = result_info
            record_info[target_domain] = target_info

        for name in new_recursion:
            queryDns(name, recursion_count-1, timeout)
    return

ns_servers = []
def dns_zone_xfer(address):
    ns_answer = dns.resolver.query(address, 'NS')
    for server in ns_answer:
        print("[*] Found NS: {}".format(server))
        ip_answer = dns.resolver.query(server.target, 'A')
        for ip in ip_answer:
            print("[*] IP for {} is {}".format(server, ip))
            try:
                zone = dns.zone.from_xfr(dns.query.xfr(str(ip), address))
                for host in zone:
                    print("[*] Found Host: {}".format(host))
            except Exception as e:
                print("[*] NS {} refused zone transfer!".format(server))
                continue


parser = argparse.ArgumentParser(
    prog="DNS scraper",
    description="Scrapes DNS records",
    epilog="No more help"
)

parser.add_argument("target")


parser.add_argument("-a", "--A", action="store_true")
parser.add_argument("-ns", "--NS", action="store_true")
parser.add_argument("-md", "--MD", action="store_true")
parser.add_argument("-mf", "--MF", action="store_true")
parser.add_argument("-cname", "--CNAME", action="store_true")
parser.add_argument("-soa", "--SOA", action="store_true")
parser.add_argument("-mb", "--MB", action="store_true")
parser.add_argument("-mg", "--MG", action="store_true")
parser.add_argument("-mr", "--MR", action="store_true")
parser.add_argument("-null", "--NULL", action="store_true")
parser.add_argument("-wks", "--WKS", action="store_true")
parser.add_argument("-ptr", "--PTR", action="store_true")
parser.add_argument("-hinfo", "--HINFO", action="store_true")
parser.add_argument("-minfo", "--MINFO", action="store_true")
parser.add_argument("-mx", "--MX", action="store_true")
parser.add_argument("-txt", "--TXT", action="store_true")
parser.add_argument("-rp", "--RP", action="store_true")
parser.add_argument("-afsdb", "--AFSDB", action="store_true")
parser.add_argument("-x25", "--X25", action="store_true")
parser.add_argument("-isdn", "--ISDN", action="store_true")
parser.add_argument("-rt", "--RT", action="store_true")
parser.add_argument("-nsap", "--NSAP", action="store_true")
parser.add_argument("-nsap-ptr", "--NSAP-PTR", action="store_true")
parser.add_argument("-sig", "--SIG", action="store_true")
parser.add_argument("-key", "--KEY", action="store_true")
parser.add_argument("-px", "--PX", action="store_true")
parser.add_argument("-gpos", "--GPOS", action="store_true")
parser.add_argument("-aaaa", "--AAAA", action="store_true")
parser.add_argument("-loc", "--LOC", action="store_true")
parser.add_argument("-nxt", "--NXT", action="store_true")
parser.add_argument("-srv", "--SRV", action="store_true")
parser.add_argument("-naptr", "--NAPTR", action="store_true")
parser.add_argument("-kx", "--KX", action="store_true")
parser.add_argument("-cert", "--CERT", action="store_true")
parser.add_argument("-a6", "--A6", action="store_true")
parser.add_argument("-dname", "--DNAME", action="store_true")
parser.add_argument("-apl", "--APL", action="store_true")
parser.add_argument("-ds", "--DS", action="store_true")
parser.add_argument("-sshfp", "--SSHFP", action="store_true")
parser.add_argument("-ipseckey", "--IPSECKEY", action="store_true")
parser.add_argument("-rrsig", "--RRSIG", action="store_true")
parser.add_argument("-nsec", "--NSEC", action="store_true")
parser.add_argument("-dnskey", "--DNSKEY", action="store_true")
parser.add_argument("-dhcid", "--DHCID", action="store_true")
parser.add_argument("-nsec3", "--NSEC3", action="store_true")
parser.add_argument("-nsec3param", "--NSEC3PARAM", action="store_true")
parser.add_argument("-tlsa", "--TLSA", action="store_true")
parser.add_argument("-hip", "--HIP", action="store_true")
parser.add_argument("-cds", "--CDS", action="store_true")
parser.add_argument("-cdnk", "--CDNSKEY", action="store_true")
parser.add_argument("-csync", "--CSYNC", action="store_true")
parser.add_argument("-spf", "--SPF", action="store_true")
parser.add_argument("-unspec", "--UNSPEC", action="store_true")
parser.add_argument("-eui48", "--EUI48", action="store_true")
parser.add_argument("-eui64", "--EUI64", action="store_true")
parser.add_argument("-uri", "--URI", action="store_true")
parser.add_argument("-caa", "--CAA", action="store_true")
parser.add_argument("-ta", "--TA", action="store_true")
parser.add_argument("-dlv", "--DLV", action="store_true")

parser.add_argument("-x", "--ALL", action="store_true", help="Set all record types")
parser.add_argument("-d", "--depth", type=int, help="Usage: -d <depth of sesarch/number of recursions>", default=0)
parser.add_argument("-t", "--timeout", type=int, help="Usage: -t <number of seconds>", default=3)
parser.add_argument("--ZONE", action="store_true")

# Set the target domain and record type
args = parser.parse_args()

target_domain = args.target
recursion_count = args.depth
timeout = args.timeout
ZONE_MODE = args.ZONE

arg_dict = (vars(args))

#check for all flag
if args.ALL:
    for key in arg_dict.keys():
        arg_dict[key]= True

#remove everything but dns record types
#make it cleaner later
first_key = next(iter(arg_dict))
arg_dict.pop(first_key)
arg_dict.popitem() #-x
arg_dict.popitem() #-r
arg_dict.popitem() #-t
arg_dict.popitem() #--ZONE

#append present flags to list
for arg_name, arg_value in arg_dict.items():
    if arg_value:
        record_types.append(str(arg_name))

queryDns(target_domain, recursion_count, timeout)
dns_zone_xfer(target_domain)

print(record_info)


