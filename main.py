#!/usr/bin/env python3

import sys
import time
import socket
import automata
import threading

PORT = 3000

def print_pals(auto):
    while True:
        time.sleep(30)
        print('Peers = [', end = '')
        for k in auto.peers:
            print(' \'{0}\' '.format(k), end = '')
        print(']')

if __name__ != '__main__':
    sys.exit(1)

# Get an interface
ifaces = automata.get_ifaces()
k = 'eth0' # just to default it
for key in ifaces:
    if ifaces[key].get('broadcast', None): k = key
iface = ifaces[k]

broadcaster = automata.automata(address = iface['addr'])
broadcaster.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

thread_ltn = threading.Thread(
                target = broadcaster.listen,
                name = 'listener'
            )
thread_ltn_tcp = threading.Thread(
                target = broadcaster.listen_peer,
                name = 'listener_tcp'
            )

thread_br = threading.Thread(
            target = broadcaster.beacon,
            name = 'broadcaster'
        )

thread_st = threading.Thread( target = print_pals, args = (broadcaster, ) )

thread_br.start()
thread_ltn.start()
thread_ltn_tcp.start()
thread_st.start()

thread_br.join()
thread_ltn_tcp.join()
thread_st.join()
nier.close()

print("\n\nExiting...")
