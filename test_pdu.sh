#!/bin/bash

for i in {1..5}
do
./pdu-commander.py off:all delay:1 on:1 delay:1 on:2 delay:1 on:3 delay:1 on:4 delay:1 on:5 delay:1 on:6 delay:1 on:7 delay:1 on:8
./pdu-commander.py delay:1 off:1 delay:1 off:2 delay:1 off:3 delay:1 off:4 delay:1 off:5 delay:1 off:6 delay:1 off:7 delay:1 off:8
done

