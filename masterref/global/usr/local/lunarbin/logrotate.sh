#!/bin/bash

## ftp log rotation
###############################################
ftpdir="/var/log/ftp"

## remove last months archives
rm -f $ftpdir/*.0

## move into ftp directory
cd $ftpdir

## move ftp logfiles
for i in `ls ftp*`; do
  mv $ftpdir/$i $ftpdir/$i.0
done

## restart ftpd
/etc/rc3.d/S51proftpd restart

##################################################


## archives logs for non-urchin sites

wwwdir="/var/log/www"

## move into www directory
cd $wwwdir

for i in `ls /etc/hosting-options`; do

  if [ ! -e "/etc/hosting-options/$i/urchin" ]; then

    mv $wwwdir/www-xfer.$i $wwwdir/www-xfer.$i.0
    mv $wwwdir/www-error.$i $wwwdir/www-error.$i.0

  fi

done

## gracefully restart http
/usr/local/apache/bin/apachectl graceful
