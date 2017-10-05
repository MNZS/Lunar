#!/bin/bash

# $Id: adddisk.sh,v 1.1 2003/04/02 19:08:41 root Exp $

# Add up the disk usage for each domain

for i in `ls /www`; do

  if [ $i != "lost+found" ] && 
     [ $i != "www.safetysupplyillinois.com" ] &&
     [ $i != "metaldecor.lunarmedia.net" ] &&
     [ $i != "www.family-jewelry.com" ]; then

    #j=`du -sH /www/$i/pub`
    j=`du -sb /www/$i/pub/public_html`

    echo "$j" > /etc/hosting-options/$i/disk

  fi

done
