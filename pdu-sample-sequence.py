#!/usr/bin/python3

import pduapc


s = [
    ('get', 'status'),
    ('off', 'all'),
    ('delay', '1'),
    ('on', 1),
    ('delay', '1'),
    ('on', '2'),
    ('delay', 1),
    ('on', '8'),
    ('delay', 6),
    ('get', 'current'),
    ('get', 'power'),
    ('off', '1,2'),
    ('delay', 1),
    ('off', 'all'),
    ('get', 'status'),
]

pduapc.apc_pdu_sequencer(seq = s)
