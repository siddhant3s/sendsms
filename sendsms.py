#!/usr/bin/python2
import urllib, urllib2, urlparse, re, argparse, ConfigParser, os.path, getpass,sys,logging, cookielib

default_auth_file=os.path.expanduser('~/.sendsms.auth')
### Command Line Praser's Arguements
parser=argparse.ArgumentParser(description="Sends sms non-interctively using indyarocks.com")
parser.add_argument('-t','--authfile',metavar='FILE',default=default_auth_file,help='Specify the authorization file mannually. By default it is ~/.sendsms.auth')
parser.add_argument('-q','--quiet', action='store_true',default=False, help="Don't output anything. Overrides --debug below")
parser.add_argument('-d','--debug', action='store_true',default=False, help="Show debugging information.")
parser.add_argument('-u','--username', help="Supply username here. If supplied, you will be prompted for the password")
parser.add_argument('--force-login', action='store_true',help="Force a new login, dumping old cookies and session information")
parser.add_argument("to",help="The number to send the message to. Can be a nick as defined in the Phonebook section of authfile. Will check first in the Phonebook")
parser.add_argument("message",default=None, nargs='?',help="The message you want to send. Else will be read from stdin")
args=parser.parse_args()
### End Parser
### Load Config File
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
### function that get's from Phonebook
def get_from_phonebook(name):
    if config.has_option('Phonebook',name):
        try:
            to=str(config.getint('Phonebook', args.to)) #this ensure that the file contains a valid int
        except ValueError:
            logging.critical ("Your phonebook contains a malformed entry for %s" % name)
            sys.exit(4)
        else:
            return to
    else:
        return None
###
### Set the global variable 'to' 
try:
    to=str(int(args.to)) # a quick check if it consist of only numbers.
except ValueError:
    #That means that the args.to was not a number, now try to check if it is on Phonebook
    to=get_from_phonebook(args.to)
    if not to:
        #not exist in phonebook
        logging.critical("The name %s you specified was not found in the Phone book." % args.to)
        sys.exit(4)
    else:
        loginfo("Read %s's number from the phonebook as %s" % (args.to, to))

if not len(to) == 10:
    logging.critical("The number must be of 10 digits")
    sys.exit(4)
###
### Fetch the message either from stdin or --message        
if args.message:
    message=args.message
else:
    loginfo("Please Enter the message( 140 chars only)")
    message=sys.stdin.read()

message=message[:140]
###
### Fetch Username either from --username or prompt
if args.username:
    username=args.username
    password=getpass.getpass("Enter the password:")
else:
    username=confget('Login','username')
    password=confget('Login','password')
###
loginfo("Username:%s" % username)
logging.debug("Password:%s" % password)
### Cookies
filecookiejar = cookielib.MozillaCookieJar(os.path.expanduser('~/.sendsms.cookies'))
try_with_previous = False
try:
    filecookiejar.load(ignore_discard=True)
except:
    logging.debug("Cannot open the cookie file. Check if it exists. Ignore if this is first time.")
    cookieprocessor=urllib2.HTTPCookieProcessor()
    loginfo("No previous Authentication session")
else:
    loginfo("Previous Authentication session found. Will try with that first")
    logging.debug("Previous Cookie read from file: %s" % filecookiejar)
    cookieprocessor=urllib2.HTTPCookieProcessor(filecookiejar)
    try_with_previous=True
o = urllib2.build_opener( cookieprocessor )
def tryopen(opener,url,data=None):
    global logging
    while True:
        try:
            f = opener.open(url,data)
            return f
        except urllib2.URLError:
            logging.debug("Caught an Exception URLError. Retrying...")
            pass
### sendmessage function
def sendmessage(to_number,messagel):
    global confget
    global o
    global logging
    ### Fetch the Unique send request ID
    loginfo("Now trying to fetch the unique send request number")
    # get the unique sending request number (?r=1022401524)
    f = tryopen(o,config.get('Auth','sendsms'))
    s = f.read()
    compiled = re.compile(r'send_msgs.php\?r=[0-9]+')
    #the unique number GET argument appended to send_msgs.php
    send_msgs_get=compiled.findall(s)[0]      #GET arguement containing unique value r=1022401524
    fullsendsms=urlparse.urljoin(confget('Auth','sendsms'),send_msgs_get)
    logging.debug("Fetched the Unique sending URL: %s " % fullsendsms)

    ### send the message
    info =  urllib.urlencode({
            'receiver':to,                     #number of the person to whom you are sending
            'receiver_msg': message,                #the message
            'sender_name': confget('Login','name'), #sender's name, don't know if it is required
            'spam_check_code': "",                  #website put it as blank
            'sms_type':'3'                          #website defines this type as `flash sms'
            })
    logging.debug("POST Query: %s" % info)
    
    f = tryopen(o,fullsendsms,info)
    ###
    ### check if it was sent properly
    returl = f.geturl()
    logging.debug("Returned URL: %s" % returl)
    if os.path.split(urlparse.urlparse(returl).path)[-1] == confget('Auth','sms_sent'):
        return 'sent'
    elif returl == confget('Auth','loginpage'):
        return 'login'
    else:
        return 'failed'
    ###
###
### login function 
def login(uname,passwd):
    global logging
    global o
    global confget
    global filecookiejar
    logging.debug("Logging using url: %s" % confget('Auth','logincheck'))
    login_encode=urllib.urlencode({'username':uname, 'pass':passwd})
    logging.debug("login_encode:%s" % login_encode)
    cookieprocessor=urllib2.HTTPCookieProcessor() #new cookie processor
    o = urllib2.build_opener(cookieprocessor) # a new urlopener
    f = tryopen(o,confget('Auth','logincheck'),login_encode)
    logging.debug("Sent Login information, got the following return URL: %s", f.geturl())
    if f.geturl()==confget('Auth','logindone'):
        #save cookies
        cj=cookieprocessor.cookiejar
        cookie=enumerate(cj).next()[1]
        logging.debug("New Cookie:%s:" % cookie)
        filecookiejar.set_cookie(cookie)
        filecookiejar.save(ignore_discard=True)
        logging.debug("Cookies saved in %s" % filecookiejar.filename)
        return True
    else:
        return False
###
### Send the message and check if it was sent
loginfo("Sending to %s, the following message:\n%s" % (to,message))
###First check without loggin in using previous cookies
logging.debug("try_with_previous:%s"% try_with_previous)
while True:
    if not try_with_previous:
         ### Logging in
        loginfo("Trying to login")
        if login(username,password):
            loginfo("Login Successfull")
            try_with_previous=True
        else:
            loginfo("Login Failed. Check username, password")
            sys.exit(3)
            
    result=sendmessage(to,message)
    if result=='sent':
        loginfo("Seems Like message was successfully sent.")
        sys.exit(0)
    elif result=='failed':
        loginfo("SMS Not sent. Can't figure out why. Perhaps try again later")
        sys.exit(2)
    elif result=='login':
        try_with_previous=False
