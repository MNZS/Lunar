#!/bin/bash

# $Id: mrtg_servers.sh,v 1.1 2003/04/02 19:08:41 root Exp $

for i in `ls /usr/local/mrtg/conf/servers/*.cfg`; do 

  /usr/local/mrtg/bin/mrtg $i --logging /usr/local/mrtg/log/servers.log

done

exit
