#!/usr/bin python 

import time
import thread
import threading
import re
from random import randint
from collections import deque

#!/usr/bin python 
import time
import thread
import threading
import subprocess
from os.path import expanduser,join,splitext


# Define Global Config
# Number of reading before cleaning repo
noCountBeforeResetClean = 2880

# Seconds between temperature measurement
measureInterval = 60

# Target reading number to have in the data file
dataFileLen = 2880

class GitWriter:

    def __init__(self):
       self.root = "~/tData/"
       self.root = expanduser(self.root)
       subprocess.call(['git','-C', self.root ,'config','user.name','mmihira2'],shell=False)
       subprocess.call(['git','-C', self.root ,'config','user.email','zlayser@hotmail.com'],shell=False)
       self.tidyGit()

    def addCommit(self):
       subprocess.call(['git','-C', self.root ,'add','--all'],shell=False)
       subprocess.call(['git','-C', self.root ,'commit','-m',time.strftime('%Y-%m-%d %H:%M:%S')],shell=False)


    def push(self):

       self.addCommit()
       subprocess.call(['git','-C', self.root ,'push','origin','HEAD:data'],shell=False)
       pass

    def tidyGit(self):
       subprocess.call(['git','-C', self.root ,'reset','--hard','ebfdb4a7'],shell=False)
       subprocess.call(['git','-C', self.root ,'clean','-df'],shell=False)
       subprocess.call(['git','-C', self.root ,'gc'],shell=False)
       self.addCommit()
       subprocess.call(['git','-C', self.root ,'push','-f','origin','HEAD:data'],shell=False)

class logWriter:
    """
    logWriter is a asychronous file writer
    which logs all detected movement to a 
    text file. Also it will push these changes
    to a specified remote directory

    A thread.lock object is passed in as
    argument which each thread that references
    this writer will acquire before writing
    """

    def __init__(self,_lock,_que):
        self.lock = _lock
	self.gitWriter = GitWriter()
	self.que = _que
	self.count = 0

    def writeLnToLog(self, msg):
        self.lock.acquire()
	self.log = open('/home/pi/tData/data.js','w')
	self.que.append(msg)

	global dataFileLen
	if len(self.que) > dataFileLen:
		self.que.popleft()

	self.log.write('tData=[');
	strBuffer = []
	for i in self.que:
		strBuffer.append('"')
		strBuffer.append(i)
		strBuffer.append('"')
		strBuffer.append(',')
	strBuffer.pop()
	strBuffer.append('];')
	self.log.write("".join(strBuffer))

        self.log.flush()
	self.log.close()

	self.count += 1

	global noCountBeforeResetClean
        if self.count > noCountBeforeResetClean:
            self.gitWriter.tidyGit()
            self.count = 0

	self.gitWriter.push()
        self.lock.release()

class upload(threading.Thread):

    def __init__(self,_toWrite,_log):
	threading.Thread.__init__(self)
        self.toWrite = _toWrite
        self.log = _log

    def run(self):
        # This is a blocking call
        log.writeLnToLog(self.toWrite)


# The main write lock
writeLock = thread.allocate_lock()

# The contents of the data file
dataQue = deque()

# Create the log file
log =  logWriter(writeLock,dataQue)

runProgram = 1



while runProgram :

	try:
		while 1:
                       tFile = open('/sys/bus/w1/devices/28-000004f538aa/w1_slave','r')
                       text = tFile.read()
                       temp = re.search('t=(.*)',text).group(1)
                       tRef = upload(time.strftime('%Y-%m-%d %H:%M:%S') + ',' + temp,log)
                       tRef.start()
                       tFile.close()
		       
		       time.sleep(measureInterval)


		
	except KeyboardInterrupt:
		print "Exiting"
		runProgram = 0

	except RuntimeError, e:

		if e.message == 'Failed to add edge detection' :
			print e.message
			print "Retrying"
		else:
			print 'Exiting for unknown error : ' + e.message
			runProgram = 0








