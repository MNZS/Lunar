#!/usr/bin/perl -w

# MasterRef
# $Id: snmpBandwidth.pl,v 1.9 2003/06/05 05:39:17 root Exp $

# Poll the gateway router for mrtg information

use strict;
use Sys::Hostname;

if (hostname() !~ /^name/) {
  exit 1;
}

my @configFiles = (glob"/etc/mrtg/*.cfg");
my $cli = `which mrtg`; chomp $cli;
$cli .= ' --logging /var/log/mrtg ';

for my $cfg(@configFiles) {
  system("$cli $cfg");
}
