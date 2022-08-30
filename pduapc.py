# module pduapc
#
# Interfacing APC PDUs via telnet "CLI"
#
# This code is published under the MIT License
# When forking, reusing and/or modifying, please retain the following line:
# Copyright (c) MyElectrons.com; https://github.com/MyElectrons/PDU-Commander
#
# Tested with AP7900, AP7901, and AP7902


from pdulog import Debg, Info, Warn, Err
import pdulog

import telnetlib
import time
import re

def_host = 'ap7900' # hostname or IP address
def_user = 'device'
def_pswd = 'apc'

def_port = 23
def_timeout = 7

beol = b'\r\n' # binary end of line


def apc_pdu_sequencer(cfg=None, seq=None):

    def Display_Intro(mlines):
        Debg(mlines)
        if not pdulog.quiet:
            print('Address:', cfg['host'])
            for st in mlines.splitlines():
                if 'Unit ID:' in st:
                    unit_id = st
                if 'Outlets:' in st:
                    outlets = st
            if 'unit_id' in vars() and unit_id:
                print(unit_id)
            if 'outlets' in vars() and outlets:
                print(outlets)

    def Display_Step(ln):
        Info(ln)
        if not pdulog.quiet:
            print(ln)

    def Display_Result(mlines, getcmd=False, opcode=''):
        mres=''
        for st in mlines.splitlines():
            if re.search(r'E[0-9]{3}', st):
                err_st = st
            if not re.search(r'OK|APC>|E[0-9]{3}|%s' % (opcode), st):
                mres += st + '\n'
        mres = mres.rstrip()
        if mres:
            if getcmd or not pdulog.quiet:
                print(mres)
            if getcmd:
                Info('\n' + mres)
        if 'err_st' in vars() and err_st:
            Warn('Command failed to execute: ' + err_st)


    if cfg is None:
        cfg = {}
    cfg.setdefault('host', def_host)
    cfg.setdefault('user', def_user)
    cfg.setdefault('pswd', def_pswd)
    cfg.setdefault('port', def_port)
    cfg.setdefault('timeout', def_timeout)

    if seq is None or seq == []:
        seq = [('get', 'status')]

    Debg('cfg = ' + str(cfg))
    Debg('seq = ' + str(seq))

    tn = telnetlib.Telnet(cfg['host'], port = cfg['port'], timeout = cfg['timeout'])
    tnto = cfg['timeout']
    try:
        rd_uname = tn.read_until(b'User Name :', tnto).decode('ascii')
        tn.write(cfg['user'].encode('ascii') + beol)
        rd_paswd = tn.read_until(b'Password  :', tnto).decode('ascii')
        tn.write(cfg['pswd'].encode('ascii') + b' -c' + beol)
        rd_1stAPC = tn.read_until(b'APC>', tnto).decode('ascii')
        Display_Intro(rd_1stAPC)
        if 'User Name :' in rd_1stAPC:
            raise Exception('Wrong ussername/password. Bailing out.')
        for tt in seq: # process command:argument two-tuple
            Display_Step(str(tt))
            if 'on' == tt[0] or 'off' == tt[0]:
                cmd = tt[0] + ' ' + str(tt[1])
                tn.write(cmd.encode('ascii') + beol)
                res = tn.read_until(b'APC>', tnto).decode('ascii')
                Display_Result(res, opcode=tt[0])
            elif 'get' == tt[0]:
                cmd = str(tt[1])
                tn.write(cmd.encode('ascii') + beol)
                res = tn.read_until(b'APC>', tnto).decode('ascii')
                Display_Result(res, True, opcode=tt[1])
            elif 'delay' == tt[0]:
                time.sleep(int(tt[1]))
            else:
                Warn('Unrecognized command "%s" - skipped.' % (tt[0]))
    except Exception as e:
        Err('Exception while in Telnet session: "%s"' % (str(e)))
    finally:
        tn.write(b'bye' + beol)
        tn.close()

