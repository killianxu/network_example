#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket

class Client(object):
    """client"""

    def __init__(self):
        super(Client, self).__init__()
        
    def start_blocking(self):
        self.host = '123.207.123.108'
        self.port = 8080
        self.csock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.csock.connect((self.host, self.port))
        data = self.csock.recv(1024)
        print data

    def start_noblocking(self):
        self.csock.connect((self.host, self.port))
        # self.csock.sendall('Hello, world')
        data = self.csock.recv(1024)
        # self.csock.close()
        # print 'Received', repr(data)


if __name__ == '__main__':
    client = Client()
    client.start_blocking()
