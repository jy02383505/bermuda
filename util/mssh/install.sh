#!/bin/bash
##!/bin/bash
#执行source install.sh
#运行m会出现提示
#default user : root
#m [username] host/hostname
#m 223.202.52.43
#m refresh 223.202.52.43
#m BGP-BJ-C-5AT
#m refresh  BGP-BJ-C-5AT
#m list devices
echo "alias m='python ${PWD}/mssh.py'" >>~/.bashrc
source ~/.bashrc
