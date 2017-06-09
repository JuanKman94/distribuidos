#!/usr/bin/env python3

import time
import socket
import automata
import threading
import netifaces

PORT = 3000
MAX_LEN = 256

def listen_handler(sock, addr):
    print('Listening on {0}:{1}...'.format(addr[0], addr[1]))
    sock.bind( addr )
    try:
        while True:
            conn = sock.recvfrom(MAX_LEN)

            msg = '''Data from:
      * {ip}
      * {s}'''.format(ip = conn[1][0],
                s = str(conn[0], encoding='utf-8')
                )

            print(msg)
    except:
        sock.close()

    return 0

def broadcast_handler(sock, addr):
    data = "pinging {iface} ({ip}:{port})\r\n".format(
                iface = key,
                ip = addr[0],
                port = addr[1]
            ).encode()

    print('Broadcasting to {0}:{1}...'.format(addr[0], addr[1]))
    try:
        while True:
            sock.sendto(data, addr)
            time.sleep(1)
    except:
        sock.close()

    return 0

ifaces = automata.get_ifaces()
k = 'eth0'

for key in ifaces:
    k = key

iface = ifaces[k]
addr = (iface['broadcast'], PORT)
my_addr = (iface['addr'], PORT)

### Broadcaster
broadcaster = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
broadcaster.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

t_broadcast = threading.Thread(
        target = broadcast_handler,
        args = (broadcaster, addr)
)
t_broadcast.start()

### Listener
listener = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )

t_listen = threading.Thread(
        target = listen_handler,
        args = (listener, my_addr)
)
t_listen.start()


t_broadcast.join()
t_listen.join()

print("\n\nexiting...")
