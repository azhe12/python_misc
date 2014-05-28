#!/usr/bin/python
import socket

s = socket.socket()

host = socket.gethostname()
port=2000

#s.bind((host, port))

s.connect((host, port))

print s.recv(1024)
