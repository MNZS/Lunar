#!/usr/bin/perl -w

# MasterRef
# $Id: mrtg_servers.pl,v 1.1 2003/04/02 19:08:41 root Exp $

use strict;
use Sys::Hostname;

if (hostname() !~ /^name1/) {
  exit 1;
}

my $cli = '/usr/local/lunarbin/mrtg_servers.sh';

system("$cli");
