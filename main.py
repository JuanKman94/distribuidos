#!/usr/bin/env python3

import sys
import time
import json
import socket
import automata
import threading

def print_pals(auto):
    while True:
        time.sleep(automata.INTERVAL * 2)
        l = list()
        dead = list()
        master = { 'ip': '', 'percent': 0.0 }

        print('Peers = [')

        for ip in auto.peers:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect( (ip, automata.TCP_PORT) )

                resp = s.recv(1024)
                resp = json.loads(resp.decode())

                if resp.get('mem', {}).get('percent', 0.0) > master['percent'] or master['ip'] == '':
                    master['ip'] = resp['ip']
                    master['percent'] = resp.get('mem').get('percent')

                l.append(resp)
                s.close()
            except:
                print('ERROR Couldn\'t reach', ip)
                dead.append(ip)

        for i in range(len(l)):
            host = l[i]

            if host['ip'] == master['ip']: print('* ', end = '')
            else: print('  ', end = '' )

            print('{ip}: {perc}'.format(ip = host['ip'], perc = 100.0 - host.get('mem').get('percent')))
            #print(json.dumps(l[i], sort_keys = True, indent = 4))

        print(']')
        for ip in dead:
            auto.delete(ip)

if __name__ != '__main__':
    sys.exit(1)

# Get an interface
ifaces = automata.get_ifaces()
k = 'eth0' # just to default it
for key in ifaces:
    if ifaces[key].get('broadcast', None): k = key
iface = ifaces[k]

socket.setdefaulttimeout(2)

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
