#!/usr/bin/perl -w

# MasterRef
# $Id: searchindex.pl,v 1.1 2003/04/02 19:08:41 root Exp $

use strict;
use Sys::Hostname;

if (hostname() !~ /^host/) {
  exit 1;
}

chdir '/www';

my @list = glob("*");

for my $i(@list) {
  chomp $i;
  system("/usr/bin/perl /www/$i/options/search/indexer.pl")
    if (-e "/etc/hosting-options/$i/search");
}
