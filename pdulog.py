# module: pdulog.py

import logging

verbose = 0
debug = False
quiet = False


logging.basicConfig(filename='pdu-log.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)


logging.info("===== Running PDU-Commander CLI =====")

logger = logging.getLogger('PDU-CLI')


def DebugOn():
    logger.level = logging.DEBUG
    debug = True


def Debg(_debg_msg):
    logger.debug(_debg_msg)
    if 2 <= verbose and not quiet:
        print('DEBUG:', _debg_msg)

def Info(_info_msg):
    logger.info(_info_msg)
    if 1<= verbose and not quiet:
        print('INFO:', _info_msg)

def Warn(_warn_msg):
    logger.warning(_warn_msg)
    if not quiet:
        print('WARNING:', _warn_msg)

def Err(_err_msg):
    logger.error(_err_msg)
    if not quiet:
        print('ERROR:', _err_msg)

