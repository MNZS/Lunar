#!/usr/bin/perl -w

# Masterref
# $Id: archive-system.pl,v 1.3 2003/04/10 07:34:18 root Exp $

use strict;
use Sys::Hostname;

# check for global stop file
require '/usr/local/lunarbin/check_lockfile.pl';

if (hostname() ne 'name2.lunarhosting.net') {
  exit 1;
}

my @hosts = qw ( host1.lunarhosting.net
		 host2.lunarhosting.net
		 name1.lunarhosting.net
		 name2.lunarhosting.net );

for my $i(@hosts) {
  system("/usr/local/lunarbin/archive-system.sh $i");
}
