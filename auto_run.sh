#!/bin/bash

export PATH=/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin

#########################
#
# SS2 注文單- 豐田外倉
#
#########################
/usr/bin/python3 /home/otsuka/otsuka_platform/get_fresh_data.py u_f_w_r > /dev/null 2>&1
