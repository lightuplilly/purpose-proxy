def __init__(self, config):
    # Shutdown on Ctrl+C
    signal.signal(signal.SIGINT, self.shutdown) 

    # Create a TCP socket
    self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Re-use the socket
    self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # bind the socket to a public host, and a port   
    self.serverSocket.bind((config['HOST_NAME'], config['BIND_PORT']))
    
    self.serverSocket.listen(10) # become a server socket
    self.__clients = {}

while True:

    # Establish the connection
    (clientSocket, client_address) = self.serverSocket.accept() 
    
    d = threading.Thread(name=self._getClientName(client_address), 
    target = self.proxy_thread, args=(clientSocket, client_address))
    d.setDaemon(True)
    d.start()

# get the request from browser
request = conn.recv(config['MAX_REQUEST_LEN']) 

# parse the first line
first_line = request.split('\n')[0]

# get url
url = first_line.split(' ')[1]

http_pos = url.find("://") # find pos of ://
if (http_pos==-1):
    temp = url
else:
    temp = url[(http_pos+3):] # get the rest of url

port_pos = temp.find(":") # find the port pos (if any)

# find end of web server
webserver_pos = temp.find("/")
if webserver_pos == -1:
    webserver_pos = len(temp)

webserver = ""
port = -1
if (port_pos==-1 or webserver_pos < port_pos): 

    # default port 
    port = 80 
    webserver = temp[:webserver_pos] 

else: # specific port 
    port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
    webserver = temp[:port_pos] 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.settimeout(config['CONNECTION_TIMEOUT'])
s.connect((webserver, port))
s.sendall(request)

while 1:
    # receive data from web server
    data = s.recv(config['MAX_REQUEST_LEN'])

    if (len(data) > 0):
        conn.send(data) # send to browser/client
    else:
        break

# Check if the host:port is blacklisted
for i in range(0, len(config['BLACKLIST_DOMAINS'])):
    if config['BLACKLIST_DOMAINS'][i] in url:
        conn.close()
return

def _ishostAllowed(self, host):

    """ Check if host is allowed to access
        the content """
    for wildcard in config['HOST_ALLOWED']:
        if fnmatch.fnmatch(host, wildcard):
            return True
    return False

logging.basicConfig(level = logging.DEBUG,
format = '[%(CurrentTime)-10s] (%(ThreadName)-10s) %(message)s',)

def log(self, log_level, client, msg):

    """ Log the messages to appropriate place """
    LoggerDict = {
       'CurrentTime' : strftime("%a, %d %b %Y %X", localtime()),
       'ThreadName' : threading.currentThread().getName()
    }
    if client == -1: # Main Thread
        formatedMSG = msg
    else: # Child threads or Request Threads
        formatedMSG = '{0}:{1} {2}'.format(client[0], client[1], msg)
    logging.debug('%s', utils.colorizeLog(config['COLORED_LOGGING'],
    log_level, formatedMSG), extra=LoggerDict)

import ColorizePython
# ColorizePython.py
class pycolors:
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m' # End color
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

def colorizeLog(shouldColorize, log_level, msg):
    ## Higher is the log_level in the log()
    ## argument, the lower is its priority.
    colorize_log = {
    "NORMAL": ColorizePython.pycolors.ENDC,
    "WARNING": ColorizePython.pycolors.WARNING,
    "SUCCESS": ColorizePython.pycolors.OKGREEN,
    "FAIL": ColorizePython.pycolors.FAIL,
    "RESET": ColorizePython.pycolors.ENDC
    }

    if shouldColorize.lower() == "true":
        if log_level in colorize_log:
            return colorize_log[str(log_level)] + msg + colorize_log['RESET']
        return colorize_log["NORMAL"] + msg + colorize_log["RESET"]
    return msg 

def shutdown(self, signum, frame):
    """ Handle the exiting server. Clean all traces """
    self.log("WARNING", -1, 'Shutting down gracefully...')
    main_thread = threading.currentThread() # Wait for all clients to exit
    for t in threading.enumerate():
        if t is main_thread:
            continue
            self.log("FAIL", -1, 'joining ' + t.getName())
        t.join()
        self.serverSocket.close()
    sys.exit(0)

