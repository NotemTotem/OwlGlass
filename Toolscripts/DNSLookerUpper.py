import dns.resolver
import argparse

def recurse_cname(recursion_count):
    return

parser = argparse.ArgumentParser(
    prog="DNS scraper",
    description="Scrapes DNS records",
    epilog="No more help"
)

parser.add_argument("target")
parser.add_argument("-a", "--A", action="store_true")
parser.add_argument("-av6", "--AAAA", action="store_true")
parser.add_argument("-cn", "--CNAME", action="store_true", help="Subdomains")
parser.add_argument("-mx", "--MX", action="store_true", help="Mail server")
parser.add_argument("-ns", "--NS", action="store_true", help="Nameserver")
parser.add_argument("-soa", "--SOA", action="store_true", help="Start of authority")
parser.add_argument("-x", "--ALL", action="store_true", help="Set all record types")
parser.add_argument("-r", "--recurse", type=int, help="Usage: -r (number of recursions)", default=0)

# Set the target domain and record type
args = parser.parse_args()

target_domain = args.target
record_types = []
arg_dict = (vars(args))

#check for all flag
if args.ALL:
    for key in arg_dict.keys():
        arg_dict[key]= True

#removes everything but dns record 
#make it cleaner later
first_key = next(iter(arg_dict))
arg_dict.pop(first_key)
arg_dict.popitem()
arg_dict.popitem()


#append present flags to list
for arg_name, arg_value in arg_dict.items():
    if arg_value:
        record_types.append(str(arg_name))

resolver = dns.resolver.Resolver()
for record_type in record_types:
    # Perform DNS lookup for the specified domain and record type
    try:
        answers = resolver.resolve(target_domain, record_type)
    except dns.resolver.NoAnswer:
        continue
    # Print the answers
    print(f"{record_type} records for {target_domain}:")
    for rdata in answers:
        print(f" {rdata}")