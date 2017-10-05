#!/usr/bin/perl -w

# MasterRef
# $Id: mailarchive-update.pl,v 1.1 2003/04/02 19:08:41 root Exp $

use strict;
use Sys::Hostname;

if (hostname() ne 'host1.lunarhosting.net') {
  exit 1;
}

`/usr/local/lunarbin/mailarchive-update.sh`;
