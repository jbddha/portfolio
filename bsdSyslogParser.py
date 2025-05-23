#This is a simple log parser for parsing syslogs in the BSD format
#Outputs a cleanly formatted JSON file after parsing the log from user input
#Usage: python3 bsdSyslogParser.py logfile.txt

import re, sys, os, json
from datetime import datetime
from pathlib import Path
#syslog fields regex
fieldsRegex = re.compile(
	r"""(
    	(\w{3}) #Month
    	\s+
    	(\d{1,2}) #Day
    	\s+
    	(\d{2}:\d{2}:\d{2}) #Time
    	\s+
    	([a-zA-Z0-9.-]+) #Hostname
    	\s+
    	([a-zA-Z0-9.\-\[\]:]+) #Process Id
    	\s+
    	(.*) #Message
	)""",
	re.VERBOSE,
)
FLC = 0
try:
#Create files to store new data in
	newFile = Path("newLog.json")
	failedLines = Path("failedLines.txt")
	#Open file from user argument
	with open(sys.argv[1], "r", encoding="utf-8") as file:
    	for line in file:
        	parsedText = fieldsRegex.findall(line) #Find regex matches
        	if parsedText:
            	groups = parsedText[0]
            	date = datetime.strptime(f"{groups[1]} {groups[2]}", "%b %d").strftime("%b %d")
            	newEntry = { #JSON formatting
                	"date": date,
                	"time": groups[3],
                	"hostname": groups[4],
                	"process id": groups[5],
                	"message": groups[6],
            	}
            	with open(newFile, "a") as file: #Append new log file
                	json.dump(newEntry, file, indent=4)
                	file.write("\n")
        	else:
            	with open(failedLines, "a") as file: #Handling bad lines/mismatches
                	file.write(line)
                	FLC +=1
except (FileNotFoundError, IOError, OSError) as e:
	print(e)
print(f"New .json file created at {newFile}")
if FLC > 0:
	print(f"Failed lines stored in {failedLines}")
