#!/usr/bin/python2
import urllib, urllib2, urlparse, re, argparse, ConfigParser, os.path, getpass,sys,logging

default_auth_file=os.path.expanduser('~/.sendsms.auth')

parser=argparse.ArgumentParser(description="Sends sms non-interctively using indyarocks.com")
parser.add_argument('-t','--authfile',metavar='FILE',default=default_auth_file,help='Specify the authorization file mannually. By default it is ~/.sendsms.auth')
parser.add_argument('-q','--quiet', action='store_true',default=False, help="Don't output anything. Overrides --debug below")
parser.add_argument('-d','--debug', action='store_true',default=False, help="Show debugging information.")
parser.add_argument('-u','--username', help="Supply username here. If supplied, you will be prompted for the password")
parser.add_argument('--force-login', action='store_true',help="Force a new login, dumping old cookies and session information")
parser.add_argument("to",help="The number to send the message to. Can be a nick as defined in the authfile")
parser.add_argument("message",default=None, nargs='?',help="The message you want to send. Else will be read from stdin")
args=parser.parse_args()

logging.basicConfig(level=logging.WARNING if args.quiet else logging.DEBUG if args.debug else logging.INFO, format="%(message)s")
loginfo=logging.info
config=ConfigParser.ConfigParser()
loginfo("Reading Authfile:%s" % args.authfile)

if not config.read(args.authfile):
    logging.critical("Cannot Open authfile: %s.\n"
                     "Run with --setup argument to setup your authfile.\n"
                     "Exiting\n"%args.authfile)
    sys.exit(0)
loginfo("Read!")
confget=config.get
if args.message:
    message=args.message
else:
    loginfo("Please Enter the message( 140 chars only)")
    message=sys.stdin.read()

message=message[:140]
if args.username:
    username=args.username
    password=getpass.getpass("Enter the password:")
else:
    username=confget('Login','username')
    password=confget('Login','password')

loginfo("Username:%s" % username)
logging.debug("Password:%s" % password)
loginfo("Trying to login")
logging.debug("Logging using url: %s" % confget('Auth','logincheck'))
login_encode=urllib.urlencode({'username':username, 'pass':password})
o = urllib2.build_opener( urllib2.HTTPCookieProcessor() )
f = o.open(confget('Auth','logincheck'),login_encode)
logging.debug("Sent Login information, got the following return URL: %s", f.geturl())
if f.geturl()==confget('Auth','logindone'):
    loginfo("Login Successfull")
else:
    loginfo("Login Failed. Check username, password")
    sys.exit(3)

loginfo("Now trying to fetch the unique send request number")
# get the unique sending request number (?r=1022401524)
f = o.open(config.get('Auth','sendsms'))
s = f.read()
compiled = re.compile(r'send_msgs.php\?r=[0-9]+')
#the unique number GET argument appended to send_msgs.php
send_msgs_get=compiled.findall(s)[0]      #GET arguement containing unique value r=1022401524
fullsendsms=urlparse.urljoin(confget('Auth','sendsms'),send_msgs_get)
logging.debug("Fetched the Unique sending URL: %s " % fullsendsms)
loginfo("Sending to %s, the following message:\n %s" % (args.to,message))
info =  urllib.urlencode({
        'receiver':args.to,                     #number of the person to whom you are sending
        'receiver_msg': message,                #the message
        'sender_name': confget('Login','name'), #sender's name, don't know if it is required
        'spam_check_code': "",                  #website put it as blank
        'sms_type':'3'                          #website defines this type as `flash sms'
        })
logging.debug("POST Query: %s" % info)
f = o.open(fullsendsms,info)
returl = f.geturl()
logging.debug("Returned URL: %s" % returl)
if os.path.split(urlparse.urlparse(returl).path)[-1] == confget('Auth','sms_sent'):
    loginfo("Seems like the SMS was sucessfully sent. Exiting")
else:
    loginfo("SMS Not sent. Can't figure out why. Perhaps try again later")


