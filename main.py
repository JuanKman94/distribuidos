#!/usr/bin/env python
# python 3.5

import socket
import sys
import threading

HOST, PORT = '', 3000

try:
    # AF_INET for IPv4
    # SOCK_STREAM for TCP, SOCK_DGRAM for UDP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind( (HOST, PORT) )
    s.listen(10)
except Exception as ex:
    print('Failed to create socket. Error {0}'.format(ex))
    sys.exit(1)

print('Socket binding complete. Listening on port {0}'.format(PORT))

def client_thread(conn, addr = []):
    conn.send('Welcome to this bare-bones server. Type something'.encode())

    while True:
        data = conn.recv(1024)
        if not data: break

        data = str(data, encoding = 'utf-8')

        reply = 'OK... ' + str(len(data)) + ' ' + data
        print( 'Message received. Responding through port {0}: {1}'.format(addr[1], data ))
        conn.sendall(reply.encode())

    print('Came out of loop, bro')
    conn.close()

try:
    while True:
        (conn, addr) = s.accept() # blocking call

        print('Connected with {0}: {1}'.format(addr[0], addr[1]))

        threading.Thread( target = client_thread, args = (conn, addr)).start()
except Exception as ex:
    print('Something happened, man!')

s.close()
