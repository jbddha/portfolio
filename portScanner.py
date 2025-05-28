#!python3
#This is a simple port scanner I wrote for experiments with sockets, and threading
#Scans the specified port range of an ip and returns open ports and banners if supplied
#Usage: python3 portScanner.py <IP> <ports>
#The ports argument is optional and will handle the format 22,80,1389 OR a range like 1-100
#If no ports arguments is supplied, the program will scan ports 1-100

import sys, socket, re
from concurrent.futures import ThreadPoolExecutor
portRangeRegex = re.compile(r"(\d+)-(\d+)")
deviceName = sys.argv[1]
#Function for scanning one port
def scanPort(hostname, port):
	try:
    	newS = socket.socket() #Create a new sockout with a timeout of 2 seconds
    	newS.settimeout(2)
    	newS.connect((hostname,port)) #Attempt to connect to a port and grab banner
    	try:
        	banner = "no banner"
        	bBytes = newS.recv(1024)
        	banner = bBytes.decode().strip() #Decodes the bytes object returned by the banner grab and strips whitespace for nice formatting
    	except socket.timeout:
        	pass
    	print(f"port {port} open : {banner}") #Print whether if port is open and if banner available
    	newS.close()
	except (ConnectionRefusedError, socket.timeout): #Handling possible errors
    	pass
	except OSError as e:
    	print(e)
	except socket.gaierror:
    	print("IP is invalid")
ports = range(1, 100)
if sys.argv[2]: #Handling the optional second argument
	userPorts = sys.argv[2]
	if portRangeRegex.search(userPorts): #Regex capture for the range
    	groups = portRangeRegex.search(userPorts)
    	ports = range(int(groups[1]), (int(groups[2]) + 1))
	else:
    	portList = userPorts.split(",") #Create a list of ports supplied by user
    	ports = []
    	for port in portList:
        	ports.append(int(port)) #Convert to integers
with ThreadPoolExecutor(max_workers=500) as executor: #Use of max 500 threads to execute port scanning
	for port in ports:
    	executor.submit(scanPort, deviceName, port)
