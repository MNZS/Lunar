#!/usr/bin/perl -w

# $Id: urchin_logrotate.pl,v 1.1 2003/04/02 19:08:41 root Exp $

use strict;
use Date::Manip;
use Sys::Hostname;

## only run on host servers
if (hostname() !~ /^host/) {
  exit;
}

my $logDir = '/var/log/www';

my $daysAgo = &ParseDateDelta("5 days ago");
$daysAgo = &UnixDate("$daysAgo","%Y%m%d");

my @logFiles = glob("$logDir/*");

exit if ($#logFiles < 0);

for my $file(@logFiles) {
  next if (-d $file);
  next if ($file eq '.');
  next if ($file eq '..');
  if ($file =~ /$daysAgo$/) {
    unlink $file or warn "Could not unlink $file : $!\n";
  }
}
