#!/bin/bash

# $Id: archive-system.sh,v 1.15 2003/07/03 13:42:36 root Exp $

REMOTE=$1

if [ $REMOTE = "" ]; then
  echo "You must specify a remote host!"
  exit 1
fi

DATE=`date +%Y%m%d`
ARCHIVE="/usr/local/archives/$REMOTE/"

SYS="$ARCHIVE/system"
WWW="$ARCHIVE/$DATE"

RSYNC=`which rsync`
ARGS="-aPH --partial --delete --delete-after"
SSH="/usr/bin/ssh -p 9490"

# logging parameters
NDAY=`date +%d`
DAY=`date +%a`
MONTH=`date +%b`
YEAR=`date +%y`
TIME=`date +%T`

# log start time
/bin/echo "$MONTH $NDAY ($DAY) - $TIME : Started backup of $REMOTE" >> /var/log/archives

if [ $REMOTE != "name2.lunarhosting.net" ]; then

  if [ ! -d "$ARCHIVE" ]; then
    exit 1;
  fi

  # first make recursive directories
  mkdir -p $SYS/var/spool
  mkdir -p $SYS/usr/lib
  mkdir -p $SYS/usr/local

  if [ $REMOTE = "host2.lunarhosting.net" ] || 
     [ $REMOTE = "host1.lunarhosting.net" ]; 
  then
    mkdir -p $WWW/www
  fi

  ##
  ## NON-WWW DIRECTORIES WILL REMAIN IN A MIRRORED STATE TO THE PARENT
  ##

  # MAIL/CRON/SPOOL BACKUPS
  $RSYNC $ARGS -e "$SSH"  $REMOTE:/var/spool $SYS/var/
  # NAMESERVER
  $RSYNC $ARGS -e "$SSH"  $REMOTE:/var/named $SYS/var/
  # MYSQL 
  $RSYNC $ARGS -e "$SSH"  $REMOTE:/var/lib $SYS/var/
  # ETC
  $RSYNC $ARGS -e "$SSH"  $REMOTE:/etc $SYS/
  # HOME
  $RSYNC $ARGS -e "$SSH"  $REMOTE:/home $SYS/

  # /usr/local
  if [ $REMOTE = "host1.lunarhosting.net" ] ||
     [ $REMOTE = "host2.lunarhosting.net" ];
  then
    $RSYNC $ARGS -e "$SSH" $REMOTE:/usr/local $SYS/usr
  fi

  # /usr/local/mrtg and /usr/local/tftp_dir
  if [ $REMOTE = "name1.lunarhosting.net" ]; then
    $RSYNC $ARGS -e "$SSH" $REMOTE:/usr/local/mrtg $SYS/usr/local
    $RSYNC $ARGS -e "$SSH" $REMOTE:/usr/local/tftp_dir $SYS/usr/local
    $RSYNC $ARGS -e "$SSH" $REMOTE:/usr/local/etc $SYS/usr/local
    $RSYNC $ARGS -e "$SSH" $REMOTE:/usr/local/bin $SYS/usr/local
  fi

  # PERL MODULES
  $RSYNC $ARGS -e "$SSH"  $REMOTE:/usr/lib/perl5 $SYS/usr/lib

  # SQUIRREL MAIL
  if [ $REMOTE = "host1.lunarhosting.net" ] ||
     [ $REMOTE = "host2.lunarhosting.net" ];
  then
    $RSYNC $ARGS -e "$SSH" $REMOTE:/var/spool/squirrelmail $SYS/var/spool
    $RSYNC $ARGS -e "$SSH" $REMOTE:/var/lib/squirrelmail $SYS/var/lib
    $RSYNC $ARGS -e "$SSH" $REMOTE:/usr/share/squirrelmail $SYS/usr/share
  fi

  ##
  ## WWW DIRECTORIES WILL BE STORED DAILY TO ALLOW FOR RECOVERIES 
  ## ACROSS MULTIPLE DAYS
  ##

  if [ $REMOTE = "host1.lunarhosting.net" ]; then
    $RSYNC $ARGS -e "$SSH" $REMOTE:/usr/hosting $WWW/
  fi

  if [ $REMOTE = "host2.lunarhosting.net" ]; then
    $RSYNC $ARGS -e "$SSH" $REMOTE:/www $WWW/
  fi
fi

if [ $REMOTE = "name2.lunarhosting.net" ]; then
  REMOTE2="name1.lunarhosting.net"

  # make remote directories
  $SSH $REMOTE2 mkdir -p $SYS/var/spool
  $SSH $REMOTE2 mkdir -p $SYS/usr/lib
  $SSH $REMOTE2 mkdir -p $SYS/usr/local

  # MAIL/CRON/SPOOL BACKUPS
  $RSYNC $ARGS -e "$SSH"  /var/spool $REMOTE2:$SYS/var/
  # NAMESERVER
  $RSYNC $ARGS -e "$SSH"  /var/named $REMOTE2:$SYS/var/
  # MYSQL
  $RSYNC $ARGS -e "$SSH"  /var/lib $REMOTE2:$SYS/var/
  # ETC
  $RSYNC $ARGS -e "$SSH"  /etc $REMOTE2:$SYS/
  # HOME
  $RSYNC $ARGS -e "$SSH"  /home $REMOTE2:$SYS/
  # /usr/local/master*
  $RSYNC $ARGS -e "$SSH" /usr/local/masterref $REMOTE2:$SYS/usr/local
  $RSYNC $ARGS -e "$SSH" /usr/local/masterbin $REMOTE2:$SYS/usr/local
  # MRTG
  $RSYNC $ARGS -e "$SSH" /usr/local/mrtg $REMOTE2:$SYS/usr/local
  # PERL MODULES
  $RSYNC $ARGS -e "$SSH" /usr/lib/perl5 $REMOTE2:$SYS/usr/lib
fi



##
## LOG THE ACTION TO /VAR/LOG
##

TIME=`date +%T`
/bin/echo "$MONTH $NDAY ($DAY) - $TIME : Completed backup of $REMOTE" >> /var/log/archives

#
exit 0
