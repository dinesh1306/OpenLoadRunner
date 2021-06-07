#! /bin/bash
PARENT_DIR=../../
yum install python3
pip3 install pyinstaller
/usr/local/bin/pyinstaller ../cmds/load_runner
cp build/load_runner/load_runner /usr/bin/ 
