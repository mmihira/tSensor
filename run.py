#!/usr/bin python 

import time
import thread
import threading
import re
from random import randint

#!/usr/bin python 
import time
import thread
import threading
import subprocess
from os.path import expanduser,join,splitext



print "Waiting for sensor to settle"
time.sleep(2)
print "Detecting Motion"

class GitPush:

    def __init__(self):
        self.root = "~/tData_mmihira2/"
        self.root = expanduser(self.root)


    def push(self):

       subprocess.call(['git','-C', self.root ,'add','--all'],shell=False)
       subprocess.call(['git','-C', self.root ,'commit','-m',time.strftime('%Y-%m-%d %H:%M:%S')],shell=False)
       subprocess.call(['git','-C', self.root ,'push','origin','HEAD:dataTest'],shell=False)




"""
logWriter is a asychronous file writer
which logs all detected movement to a 
text file. Also it will push these changes
to a specified remote directory

A thread.lock object is passed in as
argument which each thread that references
this writer will acquire before writing
"""
class logWriter:

    def __init__(self,_lock):
        self.log = open('/home/pi/tData_mmihira2/data.txt','w')
        self.log.write('-- Starting log\n')
        self.lock = _lock
	self.gitWriter = GitPush()

    def writeLnToLog(self, msg):
        self.lock.acquire()
        self.log.write(msg +  '\n')
        self.log.flush()
	# Notice the log file is never closed
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

# Create the log file
log =  logWriter(writeLock)

runProgram = 1
tFile = None
text = ""
temp = ""
tRef = None

while runProgram :

	try:
		while 1:
                       tFile = open('/sys/bus/w1/devices/28-000004f538aa/w1_slave','r')
                       text = tFile.read()
                       temp = re.search('t=(.*)',text).group(1)
                       tRef = upload(time.strftime('%Y-%m-%d %H:%M:%S') + ',' + temp,log)
                       tRef.start()
                       tFile.close()
		       time.sleep(60)


		
	except KeyboardInterrupt:
		print "Exiting"
		GPIO.cleanup()
		runProgram = 0

	except RuntimeError, e:

		if e.message == 'Failed to add edge detection' :
			print e.message
			print "Retrying"
		else:
			print 'Exiting for unknown error : ' + e.message
			GPIO.cleanup()
			runProgram = 0








