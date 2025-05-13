#This program will search each .txt file in a user supplied directory
#for a user supplied regex and return all lines that match the regex
#with the correspong file name above

#use: python3 userRegexDirSearch /some/dir/path 'regex'

import os, sys, re
from pathlib import Path
userRegex = re.compile((sys.argv[2]))
fileMatchList = []
regexMatchList = []
fileNamesList = []
#loop through directory and make list of ".txt" files
for filename in os.listdir(sys.argv[1]):
	if filename.endswith(".txt"):
    	fileMatchList.append(filename)
#loop through files and read each lines
#add lines that match the user supplied regex to a list
#add that list to a list that corresponds with the file
for filename in fileMatchList:
	currentFile = open(Path(f'{sys.argv[1]}/{filename}'), 'r')
	currentFileList = []
	for currentLine in currentFile.readlines():
        	matches = ''
        	matches = userRegex.findall(currentLine)
        	if matches != '':
            	currentFileList.append(currentLine)
        	if filename not in fileNamesList:
            	fileNamesList.append(filename)
	regexMatchList.append(currentFileList)
	currentFile.close()
#print matching lines for user supplied regex in supplied directory
#prints filenames where lines can be found
FNC = 0
for x in fileNamesList:
	print(fileNamesList[FNC])
	for y in regexMatchList[FNC]:
    	print(y)
	FNC += 1


