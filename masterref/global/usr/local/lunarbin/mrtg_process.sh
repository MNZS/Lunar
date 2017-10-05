#!/bin/bash

# $Id: mrtg_process.sh,v 1.1 2003/04/02 19:08:41 root Exp $

for i in `ls /usr/local/mrtg/conf/wireless/*.cfg`; do 

  /usr/local/mrtg/bin/mrtg $i --logging /usr/local/mrtg/log/wireless.log

done

exit
