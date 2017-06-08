#!/usr/bin/env python3

import automata
import socket
import netifaces

PORT = 3000

ifaces = automata.get_ifaces()

for key in ifaces:
    iface = ifaces[key]
    addr = (iface['broadcast'], PORT)
    data = "pinging {iface} ({ip}:{port})\r\n".format(
                iface = key,
                ip = addr[0],
                port = addr[1]
            ).encode()

    print("Sending data:\n  * To {0}".format(addr[0]))
    print('  * Message "{0}"'.format(str(data, encoding='utf-8').rstrip()))

    s = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    s.sendto(data, addr)
    res = s.recvfrom(256)

    print('Received data:\n  * From {0}'.format(res[1][0]))
    print('  * Message: "{0}"'.format(str(res[0], encoding='utf-8').rstrip()))

    s.close()

print("\n\nexiting...")
