#!/bin/bash
#

# $Id: mailarchive-monthly.sh,v 1.1 2003/04/02 19:08:41 root Exp $

# this file cleans out the monthly email log for the 
# archive user

USER="quilmes-archives"
GROUP="cmenzes"
DATE=`date +%Y%m`

# backup the previous month's messages
mv /var/spool/mail/$USER /var/spool/mail/$USER.$DATE

# create a new mail file
touch /var/spool/mail/$USER

# apply the appropriate permissions and ownership
chown $USER /var/spool/mail/$USER
chgrp $GROUP /var/spool/mail/$USER
chmod 660 /var/spool/mail/$USER
