#!/usr/bin/env python3

import time
import socket
import automata
import threading

PORT = 3000

def print_pals(auto):
    while True:
        print(auto.pals)
        time.sleep(3)

ifaces = automata.get_ifaces()
k = 'eth0' # just to default it
for key in ifaces:
    if ifaces[key].get('broadcast', None): k = key
iface = ifaces[k]
bc_addr = (iface['broadcast'], PORT)

while True:
    ### Broadcaster
    nier = automata.automata(address = iface['addr'], port = PORT)
    nier.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    t_broadcast = threading.Thread(
            target = nier.beacon,
            name = 'broadcaster',
            args = (bc_addr,)
    )
    t_broadcast.start()

    ### Listener
    listener = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )

    t_listen = threading.Thread(target = nier.up, name = 'listener')
    t_listen.start()

    ### Status
    t_status = threading.Thread( target = print_pals, args = (nier,) )
    t_status.start()

    t_broadcast.join()
    t_listen.join()
    t_status.join()
    nier.close()

print("\n\nexiting...")
