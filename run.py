#!/usr/bin python

import time
import thread
import threading
import re
from collections import deque
from os.path import expanduser, join, splitext
import subprocess

# Number of reading before cleaning repo
noCountBeforeResetClean = 2880

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

class DataWriter:
    """
    DataWriter is a asychronous file writer which both writes
    the latest information to local cache and also writes
    the latest data to the git repository.

    A thread.lock object is passed in as
    argument which each thread that references
    this writer will acquire before writing.
    """

    def __init__(self, lock, que):
        self.lock = lock
	self.gitWriter = GitWriter()
	self.que = que
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

class UploadThread(threading.Thread):
    def __init__(self,_toWrite,_log):
	threading.Thread.__init__(self)
        self.toWrite = _toWrite
        self.log = _log

    def run(self):
        # This is a blocking call
        log.writeLnToLog(self.toWrite)

class Monitor:
    # Seconds between temperature measurement
    sleepDelay = 60

    def __init__(self):
        # The contents of the data file
        self.dataQue = deque()
        # The main write lock
        self.writeLock = thread.allocate_lock()
        self.log = DataWriter(self.writeLock, self.dataQue)

    def run():
        while True:
            try:
                while True:
                   tFile = open('/sys/bus/w1/devices/28-000004f538aa/w1_slave','r')
                   text = tFile.read()
                   temp = re.search('t=(.*)',text).group(1)

                   threadRef = UploadThread(time.strftime('%Y-%m-%d %H:%M:%S') + ',' + temp, self.log)
                   threadRef.start()

                   tFile.close()
                   time.sleep(Monitor.sleepDelay)

            except KeyboardInterrupt:
                print "Exiting"
                exit(0)
            except RuntimeError, e:
                if e.message == 'Failed to add edge detection' :
                    print e.message
                    print "Retrying"
                else:
                    print 'Exiting for unknown error : ' + e.message
                    exit(1)

Monitor().run()

