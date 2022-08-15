#!/usr/bin/python3

# PDU CLI Commander
# A Command Line Interface wrapper for PDU sequencer module(s)

import pduapc
from pdulog import Debg, Info, Err
import pdulog

import argparse
import textwrap
import re

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent('''\
        Supported commands:
          on | off - control outlets on PDU's that support individual outlet switching
          get      - read PDU data, including: status, current, power
          delay    - pause for a number of seconds before the next command gets executed
        '''),
    epilog=textwrap.dedent('''\

        If called without command:argument parameters the script will execute "get:status"

        Copyright (c) : MyElectrons.com
        ''')
    )
parser.add_argument('-a', '--addr', help='IP address or DNS-resolvable host name of PDU')
parser.add_argument('-u', '--user', type=str, help='username, default="device"')
parser.add_argument('-p', '--pswd', type=str, help='password, default="apc"')
parser.add_argument('-P', '--port', type=int, help='Telnet port, default=23')
parser.add_argument('-t', '--tout', type=int, help='Telnet timeout, default=7 (seconds)')
parser.add_argument("-d", "--debug", action="store_true", help="log debug messages in addition to info and errors")
vq_grp = parser.add_mutually_exclusive_group()
vq_grp.add_argument("-v", "--verbosity", action="count", default=0, help="increase output verbosity on stdout: -v or -vv")
vq_grp.add_argument("-q", "--quiet", action="store_true", help="only output responses to \"get\" requests")
parser.add_argument('commands', metavar='command:argument', type=str, nargs='*', #action='append',
                    help='commands to be executed')
args = parser.parse_args()

cfg = {}
if args.addr:
    cfg['host'] = args.addr
if args.user:
    cfg['user'] = args.user
if args.pswd:
    cfg['pswd'] = args.pswd
if args.port:
    cfg['port'] = args.port
if args.debug:
    pdulog.DebugOn()
if args.verbosity:
    pdulog.verbose = args.verbosity
if args.quiet:
    pdulog.quiet = args.quiet

seq = []
if args.commands:
    for c in args.commands:
        cmd_arg_ok = False
        text = re.sub(r'[\s]+', '', c)
        m = re.search('(.+):(.+)', text)
        if m:
            k = m.group(1)
            v = m.group(2)
            if k != '' and v != '':
                cmd_arg_ok = True
                seq.append((k,v))
        if not cmd_arg_ok:
            Err('Unable to parse "%s" as a command:argument pair. Bailing out.' % (c))
            exit(1)

pduapc.apc_pdu_sequencer(cfg, seq)
