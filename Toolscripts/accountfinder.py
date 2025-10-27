import argparse
import sys
import requests

DEVELOPMENT = '--development' in sys.argv and not '--json' in sys.argv
JSON_ONLY = '--json' in sys.argv

class MyParser(argparse.ArgumentParser):
    def error(self,message):
        sys.stderr.write('error: %s\n' % message)
        # self.print_help()
        sys.exit(2)
    def warning(self,message):
        sys.stderr.write('warning: %s\n' % message)
    def debug_print(self,message):
        if DEVELOPMENT:
            sys.stderr.write('debug: %s\n' % message)
parser = MyParser()


def web_check(target_object,web_object):
    if target_object["targetType"] == 'email':
        target = target_object["username"]
    elif target_object["targetType"] == 'username':
        target = target_object["target"]
    else:
        parser.error("targetType of {s!r}" % f'{target_object["targetType"]} not present in web_check.')

    url = web_object['url'].replace('<target>',target)

    if web_object['errorType'] == 'status_code':
        try:
            r = requests.get('https://'+url)
        except Exception as e:
            parser.error(e)
        if r.status_code == 200:
            return True,url
        else:
            return False,url
    else:
        parser.error("status_code of {s!r}" % f'{web_object["status_code"]} not currently implemented.')
def main():


            'targetType':'email'
        }
            'targetType':'username'
        }
    if not args.w:
        WEBSITES = websitemanager.web_objects       

def main():
 
    #Parsing arguements 
    if args.t and len(args.t) >1:
        parser.error("Please only provide one email or username for now.")

    if not args.t and not WEBSITECHECK:
        parser.error('Please specify an email or username using -e or -u ')

    
    report = {
        'target':target_object,
        'checks':[]
    }
    for index, key in enumerate(WEBSITES.keys()):
        parser.debug_print(f"Index:{index}, Key:{key}")
        parser.debug_print(WEBSITES[key])
        response,attempted_url = web_check(target_object,WEBSITES[key])

        report_entry = {
            'website':WEBSITES[key],
            'accountFound':response,
            'attemptedUrl':attempted_url
        }
        
        report['checks'].append(report_entry)
    
    if JSON_ONLY:
        pass
    else:
        print('\n'+'-'*30)
        print(f'\nFINAL REPORT\n')
        print('-'*30)
        print(f"\n - USER INFO - ")
        print(f"Target string: '{report['target']['target']}'\nTarget type: {report['target']['targetType']}")
        print(f"\n - WEBSITES CHECKED - ")
        for website in report['checks']:
            print(f"Account found: {website['accountFound']}\nWebsite: https://{website['website']['urlMain']}\nAttempted url: https://{website['attemptedUrl']}")    

parser.add_argument('-w',help="The website(s) to check. comma-seperated (default: all)")
parser.add_argument('--development',action='store_true',help="Provides additional debugging information during runtime (default: true)")
parser.add_argument('--json',action='store_true',help="Provides additional debugging information during runtime (default: true)")

if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)

args = parser.parse_args()

if __name__ == "__main__":
    main()