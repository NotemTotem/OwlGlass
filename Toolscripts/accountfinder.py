import argparse
import sys

#In future websites will be stored in data.json 
class WebsiteManager:
    def __init__(self):
        """
        Manages supported websites.
        errorType; currently only supports status_code
        url; the url to test username. 
        urlMain; the main url to access the website
        username_claimed; a currently existing user (for testing purposes)
        entry schema:
        "websitename":{
            'errorType':str,
            'url':str,
            'urlMain':str,
            'username_claimed':str
        }
        """
        self.website_objects = {
            "chess.com":{
                'errorType':'status_code',
                'url':'chess.com/member/{}',
                'urlMain':'chess.com',
                'username_claimed':'red'
            }
        }

class MyParser(argparse.ArgumentParser):
    def error(self,message):
        sys.stderr.write('error: %s\n' % message)
        # self.print_help()
        sys.exit(2)
    
websitemanager = WebsiteManager()
parser = MyParser()

parser.add_argument('-u','--username',help='username',nargs=1)
parser.add_argument('-e','--email',help='email',nargs=1)
parser.add_argument('-wl','--websitelist',help='lists scrapeable websites',nargs=0)
if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)

args = parser.parse_args()

if args.websitelist:
    #Will eventually list supported websites
    pass
    sys.exit(1)

if args.email and args.username:
    parser.error("Please specify EITHER email or username")

if not args.email and not args.username:
    parser.error('Pleasore specify an email or username using -e ')

def main():
    pass

    main()