#!/usr/bin/env python3

import automata

while True:
    nier = automata.automata(port = 9000)
    master_ip = nier.beacon()

    if not master_ip:
        print('No master found. Becoming one...')
        nier.become_master()
    else:
        print('master found {0}. pinging...'.format(master_ip))
        resp = nier.ping()

        if not resp: nier.close()
