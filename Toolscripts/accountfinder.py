import argparse
import sys
import requests
import re
import json

DEVELOPMENT = '--development' in sys.argv and not '--json' in sys.argv
JSON_ONLY = '--json' in sys.argv
WEBSITECHECK = '--websitecheck' in sys.argv

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
        parser.debug_print(f"targetType of {target_object['targetType']!r} not present in web_check.")

    url = web_object['url'].replace('{}',target)

    if web_object['errorType'] == 'status_code':
        try:
            r = requests.get(url)
        except Exception as e:
            parser.debug_print(e)
            return False,url
        if r.status_code == 200:
            return True,url
        else:
            return False,url
    else:
        parser.debug_print(f"status_code of {web_object['status_code']!r} not currently implemented.")

def return_target_entry(target_string):
    #Check if target string is an email
    if re.match("[^@]+@[^@]+\\.[^@]+",target_string):
        return {
            'target':target_string,
            'targetSplit':target_string.split('@'),
            'username':target_string.split('@')[0],
            'domain':target_string.split('@')[1],
            'targetType':'email'
        }
    #Otherwise assume its a username.
    else:
        return {
            'target':target_string,
            'targetSplit':None,
            'username':None,
            'domain':None,
            'targetType':'username'
        }

def main():
 
    #Parsing arguements 
    if args.t and len(args.t) >1:
        parser.error("Please only provide one email or username for now.")

    if not args.t and not WEBSITECHECK:
        parser.error('Please specify an email or username using -e or -u ')

    #Loading in web objects from json file.
    with open('static\\resources\\accountfinder\\data.json') as json_file:
        website_objects = json.load(json_file)  
    
    report = {
        'targets':[],
        'checks':[]
    }

    if not WEBSITECHECK:
        target_string = args.t[0]
        target_object = return_target_entry(target_string)
        report['targets'].append(target_object)
    #Tracking iteration count so we can set a max num of websites to check.
    index = -1
    for key, website in website_objects.items():
        index+=1
        parser.debug_print(f"Index:{index}, Website:{website}")
        #This lets us set a max number of websites to check before printing the results.
        if index > 4:
            break
        if index == 0:
            #The first entry is just a schema object so we skip this.
            continue
        if 'isNSFW' in website:
            #Some websites are NSFW as I got the json dataset from an opensource project. As such we must skip these.  
            continue
        if WEBSITECHECK:
            target_string = website['username_claimed']
            target_object = return_target_entry(target_string)

        try:
            response,attempted_url = web_check(target_object,website)
        except Exception as e:
            parser.warning(e)
            response = False
            attempted_url = website['url'].replace('{}',target_string)

        report_entry = {
            'website':website,
            'accountFound':response,
            'attemptedUrl':attempted_url
        }
        
        report['checks'].append(report_entry)

    if JSON_ONLY:
        pass
    else:
        length = 100
        print('\n'+'-'*length)
        print(f'\n{" "*((length//2)-(len('FINAL REPORT')//2))}FINAL REPORT\n')
        print('-'*length)
        if not WEBSITECHECK:
            print(f"\n{' '*((length//2)-len('- USER INFO -')//2)}- USER INFO -")
            print(f"Target: {report['targets'][0]['target']!r}")
        print(f"\n{' '*((length//2)-len('- WEBSITES CHECKED -')//2)}- WEBSITES CHECKED -")
        for website in report['checks']:
            if website["accountFound"] == True:
                print(f"Account found: {website['accountFound']}\nWebsite: https://{website['website']['urlMain']}\nAttempted url: https://{website['attemptedUrl']}")    
        for website in report['checks']:
            if website["accountFound"] == False:
                print(f"Account found: {website['accountFound']}\nWebsite: https://{website['website']['urlMain']}\nAttempted url: https://{website['attemptedUrl']}")    

parser.add_argument('-t',action='append',help='Target string to find accounts under (email or username)')
#parser.add_argument('-w',help="The website(s) to check. comma-seperated (default: all)")
parser.add_argument('--development',action='store_true',help="Provides additional debugging information during runtime (default: true)")
parser.add_argument('--json',action='store_true',help="Provides additional debugging information during runtime (default: true)")
parser.add_argument('--websitecheck',action='store_true',help='Provides a list of websites that were incorrectly identified by accountfinder as not having a known user.')

if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)

args = parser.parse_args()

if __name__ == "__main__":
    main()