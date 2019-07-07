#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

class Client(object):
    """client"""

    def __init__(self):
        super(Client, self).__init__()

    def start(self):
        messages = ["hello world"]
        print "Connect to the server"
         
        server_address = ("123.207.123.108",8080)
         
        #Create a TCP/IP sock
         
        socks = []
         
        for i in range(3):
            socks.append(socket.socket(socket.AF_INET,socket.SOCK_STREAM))
         
        for s in socks:
            s.connect(server_address)
         
        counter = 0
        for message in messages :
            #Sending message from different sockets
            for s in socks:
                counter+=1
                print "  %s sending %s" % (s.getpeername(),message+" version "+str(counter))
                s.send(message+" version "+str(counter))
            #Read responses on both sockets
            for s in socks:
                data = s.recv(1024)
                print " %s received %s" % (s.getpeername(),data)
                if not data:
                    print "%s closing socket "%s.getpeername()
                    s.close()

if __name__ == '__main__':
    client = Client()
    client.start()


