#!/usr/bin/env python
# python 3.5

import distribuidos_ca as ca
import sys
import threading

HOST, PORT = '', 3000

try:
    s = ca.server(address = HOST, port = PORT)
    s.up()
except Exception as ex:
    print('Failed to create socket. Error {0}'.format(ex))
    sys.exit(1)

try:
    while True:
        (conn, addr) = s.accept() # blocking call

        print('Connected with {0}: {1}'.format(addr[0], addr[1]))

        threading.Thread( target = s.handle_conn, args = (conn, addr)).start()
except Exception as ex:
    print('Something happened, man!')

s.close()
