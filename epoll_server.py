#!/usr/bin/env python
# -*- coding: utf-8 -*-
import select
import socket
import Queue


class Server(object):

    def __init__(self):
        super(Server, self).__init__()

    def start(self):
        # Create a TCP/IP socket, and then bind and listen
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setblocking(False)
        server_address = ('', 8080)
        print "Starting up on %s port %s" % server_address
        server.bind(server_address)
        server.listen(5)
        message_queues = {}
        # The timeout value is represented in milliseconds, instead of seconds.
        timeout = 5000
        # Create a limit for the event
        READ_ONLY = (select.EPOLLIN)
        READ_WRITE = (READ_ONLY | select.EPOLLOUT)
        # Set up the epoll
        epoll = select.epoll()
        epoll.register(server.fileno(), READ_ONLY)
        # Map file descriptors to socket objects
        fd_to_socket = {server.fileno(): server, }
        while True:
            print "Waiting for the next event"
            events = epoll.poll(timeout)
            if len(events) == 0:
                print 'Time out'
                break
            print "*" * 20
            print len(events)
            print events
            print "*" * 20
            for fd, flag in events:
                s = fd_to_socket[fd]
                if flag & (select.EPOLLIN):
                    if s is server:
                        # A readable socket is ready to accept a connection
                        connection, client_address = s.accept()
                        print " Connection ", client_address
                        connection.setblocking(False)

                        fd_to_socket[connection.fileno()] = connection
                        epoll.register(connection, READ_ONLY)

                        # Give the connection a queue to send data
                        message_queues[connection] = Queue.Queue()
                    else:
                        data = s.recv(1024)
                        if data:
                            # A readable client socket has data
                            print "  received %s from %s " % (data, s.getpeername())
                            message_queues[s].put(data)
                            epoll.modify(s, READ_WRITE)
                        else:
                            # Close the connection
                            print "  closing", s.getpeername()
                            # Stop listening for input on the connection
                            epoll.unregister(s)
                            s.close()
                            del message_queues[s]
                elif flag & select.EPOLLHUP:
                    # A client that "hang up" , to be closed.
                    print " Closing ", s.getpeername(), "(HUP)"
                    epoll.unregister(s)
                    s.close()
                elif flag & select.EPOLLOUT:
                    # Socket is ready to send data , if there is any to send
                    try:
                        next_msg = message_queues[s].get_nowait()
                    except Queue.Empty:
                        # No messages waiting so stop checking
                        print s.getpeername(), " queue empty"
                        epoll.modify(s, READ_ONLY)
                    else:
                        print " sending %s to %s" % (next_msg, s.getpeername())
                        s.send(next_msg)
                elif flag & select.epollERR:
                    # Any events with epollR cause the server to close the
                    # socket
                    print "  exception on", s.getpeername()
                    epoll.unregister(s)
                    s.close()
                    del message_queues[s]

if __name__ == '__main__':
    server = Server()
    server.start()
