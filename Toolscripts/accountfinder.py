import argparse
import sys

class MyParser(argparse.ArgumentParser):
    def error(self,message):
        sys.stderr.write('error: %s\n' % message)
        # self.print_help()
        sys.exit(2)

parser = MyParser()
parser.add_argument('-u','--username',help='username',nargs=1)
parser.add_argument('-e','--email',help='email',nargs=1)
if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)
args = parser.parse_args()

if args.email and args.username:
    parser.error("Please specify EITHER email or username")

email = args.email
username = args.username
if not email and not username:
    print('Pleasore specify an email or username using -e ')

def main():
    pass

main()