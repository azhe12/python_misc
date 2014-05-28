#!/usr/bin/env python
#encoding=utf-8

import threading
import urllib2
import Queue
import time

hosts = ['https://www.python.org/', 
        'https://www.python.org/download/',
        'http://www.pythontab.com/',
        'http://python.cn/']


headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
class getUrl(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        host = self.queue.get()
        req = urllib2.Request(host, headers=headers)
        res = urllib2.urlopen(req)
        res.read(1000)
        print '%s: %s' % (self.getName(), host)
        self.queue.task_done()

start = time.time()
queue = Queue.Queue()
for host in hosts:
    queue.put(host)

for t in range(4):
    t = getUrl(queue)
    t.start()

queue.join()
print '\nElapse: %d s' % (time.time() - start)
