# Command Line Interface (CLI) and Sequencer with Python (bash, sh, other scripts) integration for APC ap7900 and other compatible Power Distribution Units (PDU)
 
While AP79xx(b) are versatile PDU devices that provide a variety of access and control options, somehow there was no ready to use **CLI tool** available that one could call from the command line or a script and tell it what sockets to switch on or off on PDU(s), or what to measure.
 
There were several sketches I found on the Net, these would potentially make PDU's controllable from scripts, mostly using telnet in conjunction with pexpect, as well as SNMP. However, those were only sketches and still required a lot of tinkering; none of the predecessor projects that I've seen provided even a rudimentary error handling.
 
This little project covers the power control needs I had. Thanks to it I can now run a chron-job that will:
1) **Power up** the backup rig (and *do it in a properly staged way*),
2) Perform backups (this part is obviously outside of the scope of this project),
3) **Power it down** completely (*eliminating wasting of dozens of Watts by standby PSUs power draw*).
 
All the steps had to be done without any human interactions required - simply because I'd forget about it after a while.
 
This project can also be used for **power monitoring** purposes. Just keep in mind that the precision of current and power measurements of the AP79xx series is somewhat low (to my taste, Ok?)
I'd be happy to give it a try and modify and adapt this project for a perfect integration with measured PDU(s). Should you need it implemented fast - *just send a unit that needs to be supported my way*.
By the way the same applies to another brand and/or SKU of the PDU or UPS or... :wink:
 
## Prerequisites
**python3** version 3.7 and up
 
## Usage Examples
 
### All defaults
Give it no parameters - it will go to "ap7901" (it should be a DNS-resolvable name) and retrieve its status:
<pre>
<b>./pdu-commander.py</b>
</pre>
```
Address: ap7901
Unit ID: ap7901
Outlets: 8
('get', 'status')
1: ON    : Outlet 1
2: ON    : Outlet 2
3: ON    : Outlet 3
4: ON    : Outlet 4
5: ON    : Outlet 5
6: ON    : Outlet 6
7: ON    : Outlet 7
8: ON    : Outlet 8
```
It will use the default APC username and password, telnet port 23, 7 seconds for telnet timeouts.
 
### Turn one outlet ON
Actionable commands consist of a command and its argument, divided by a column ':'
<pre>
<b>./pdu-commander.py on:1</b>
</pre>
```
Address: ap7901
Unit ID: ap7901
Outlets: 8
('on', '1')
1: Outlet 1       : Outlet Turned On
```
 
### A sequence of ON and OFF commands with a 3 seconds delay between them
<pre>
<b>./pdu-commander.py on:1-3,8 delay:3 off:all</b>
</pre>
```
Address: ap7901
Unit ID: ap7901
Outlets: 8
('on', '1-3,8')
 1: Outlet 1       : Outlet Turned On
 2: Outlet 2       : Outlet Turned On
 3: Outlet 3       : Outlet Turned On
 8: Outlet 8       : Outlet Turned On
('delay', '3')
('off', 'all')
 1: Outlet 1       : Outlet Turned Off
 2: Outlet 2       : Outlet Turned Off
 3: Outlet 3       : Outlet Turned Off
 4: Outlet 4       : Outlet Turned Off
 5: Outlet 5       : Outlet Turned Off
 6: Outlet 6       : Outlet Turned Off
 7: Outlet 7       : Outlet Turned Off
 8: Outlet 8       : Outlet Turned Off
```
There could be as many commands called in one sequence as needed.

### Connection details can be specified
<pre>
<b>./pdu-commander.py -a 192.168.7.242 -u device -p your_password "on: 1-2, 8" "delay: 3" "off: 2"</b>
</pre>
```
Address: 192.168.7.242
Unit ID: ap7902
Outlets: 16
('on', '1-2,8')
1: Outlet 1       : Outlet Turned On
2: Outlet 2       : Outlet Turned On
8: Outlet 8       : Outlet Turned On
('delay', '3')
('off', '2')
2: Outlet 2       : Outlet Turned Off
```
Note that the command:argument parameters must be passed as a single argument - hence if you like or need to use spaces in them, please remember to put quotes around each "command : argument" pair.
 
### Read current and power, and be quiet
<pre>
<b>./pdu-commander.py -q -a 192.168.7.242 get:current get:power</b>
</pre>
```
Current on bank 1 is 1.4A
Current on bank 2 is 0.0A
Current on total is 1.4A
168 VA
168 Watts
```
 
### There's HELP, when needed
<pre>
<b>./pdu-commander.py -h</b>
</pre>
```
usage: pdu-commander.py [-h] [-a ADDR] [-u USER] [-p PSWD] [-P PORT] [-t TOUT] [-d] [-v | -q] [command:argument [command:argument ...]]
 
Supported commands:
 on | off - control outlets on PDU's that support individual outlet switching
 get      - read PDU data, including: status, current, power
 delay    - pause for a number of seconds before the next command gets executed
 
positional arguments:
 command:argument      commands to be executed
 
optional arguments:
 -h, --help            show this help message and exit
 -a ADDR, --addr ADDR  IP address or DNS-resolvable host name of PDU
 -u USER, --user USER  username, default="device"
 -p PSWD, --pswd PSWD  password, default="apc"
 -P PORT, --port PORT  Telnet port, default=23
 -t TOUT, --tout TOUT  Telnet timeout, default=7 (seconds)
 -d, --debug           log debug messages in addition to info and errors
 -v, --verbosity       increase output verbosity on stdout: -v or -vv
 -q, --quiet           only output responses to "get" requests
 
If called without command:argument parameters the script will execute "get:status"

Copyright (c) MyElectrons.com, 2022
```

## Things to remember
 
### Maximum delays
Each `pdu-commander.py` script invocation opens a single telnet session and executes all commands within that session. That said - the delays cannot be longer than the telnet session timeout (as configured in device settings).
 
Usually delays shorter than 60 seconds are safe.
 
Should you need a longer pause between certain actions - it's better to invoke the `pdu-commander.py` again later, after the needed long delay has passed.
 
### Logging
The script will record all its actions into a log file `pdu-log.log` in the current directory. The file gets appended with every script invocation. Should you need to use another logging facility and/or functionality - just let me know, or code it away in the `pdulog.py` module.
 
### Concurrent sessions
The PDU series that I tested did not support any concurrency of control sessions. Therefore in order to use this project successfully please make sure all the configuration of the unit(s) is done, completed, and sessions are closed or logged-out before the `pdu-commander.py` script invocation.

## Tested thoroughly with
- ap7901 - :thumbsup:
- ap7902 - :thumbsup:
 
*Happy controlling!*

-- :heart: -- Serge.
