#!/bin/bash

MAILDATE=`date +%Y%m`
MHONARC=`which mhonarc`

$MHONARC \
   -add \
   -tidxfname index.html \
   --outdir "/www/lunarhosting.net/pub/staff/archives/$MAILDATE" \
   /var/spool/mail/quilmes-archives
