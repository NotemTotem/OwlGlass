import argparse
import sys
import requests

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
        self.web_objects = {
            "chess.com":{
                'errorType':'status_code',
                'url':'chess.com/member/<target>',
                'urlMain':'chess.com',
                'username_claimed':'red',
                
            }
    
        }

class MyParser(argparse.ArgumentParser):
    def error(self,message):
        sys.stderr.write('error: %s\n' % message)
        # self.print_help()
        sys.exit(2)
    def warning(self,message):
        sys.stderr.write('warning: %s\n' % message)
parser = MyParser()
websitemanager = WebsiteManager()


def web_check(target_object,web_object):
    if target_object["targetType"] == 'email':
        target = target_object["targetSplit"][1]
    elif target_object["targetType"] == 'username':
        target = target_object["target"]
    else:
        parser.error("targetType of {s!r}" % f'{target_object["targetType"]} not present in web_check.')

    url = web_object['url'].replace('<target>',target)

    if web_object['errorType'] == 'status_code':
        r = requests.get(url)
        if r.status_code == 200:
            return True
        else:
            return False
    else:
        parser.error("status_code of {s!r}" % f'{web_object["status_code"]} not currently implemented.')
def main():

    if args.e:
        target_object = {
            'target':args.e,
            'targetSplit':args.e.split('@'),
            'targetType':'email'
        }
    elif args.u:
        target_object = {
            'target':args.u,
            'target_type':'username'
        }
    if not args.w:
        WEBSITES = websitemanager.web_objects       
    
    if args.development:
        DEVELOPMENT_ENV = True
    
    print("Enumerating through websites")
    for index, key in enumerate(WEBSITES.keys()):
        print(f"Index:{index}, Key:{key}")
        print(WEBSITES[key])
        response = web_check(target_object,WEBSITES[key])

parser.add_argument('-u',action='append',help='Username to find accounts under (required if email not specified)')
parser.add_argument('-e',action='append',help='Email to find accounts under (required if username not specified)')
parser.add_argument('-w',help="The website(s) to check. comma-seperated (default: all)")
parser.add_argument('--development',action='store_true',help="Provides additional debugging information during runtime (default: true)")
if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)

args = parser.parse_args()
print(args)
if args.e and args.u:
    parser.error("Please specify EITHER an email OR username")

if args.e and len(args.e) >1 or args.u and len(args.u) >1:
    parser.error("Please only provide one email or username for now.")

if not args.e and not args.u:
    parser.error('Please specify an email or username using -e or -u ')



if __name__ == "__main__":
    main()