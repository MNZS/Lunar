#!/usr/bin/perl -w

# MasterRef
# $Id: named_refresh.pl,v 1.3 2003/10/07 20:30:13 root Exp $

# This script will run once a month to pull a completely fresh group
# of zone files from hosting servers, cleaning out any domains which 
# no longer host with the company.

use strict;
use Sys::Hostname;

require '/usr/local/lunarbin/check_lockfile.pl';

if (hostname() !~ /^name/) {
  exit 0;
}

my @hosts = qw(host1.lunarhosting.net host2.lunarhosting.net);

for my $i(@hosts) {
  system("rm -rf /var/named/systems/$i/*");
}

system("/etc/rc3.d/S45named stop");
sleep 2;
system("/etc/rc3.d/S45named start");
