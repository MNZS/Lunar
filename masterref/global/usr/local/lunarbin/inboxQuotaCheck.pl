#!/usr/bin/perl -w

use strict;
use Sys::Hostname;

## run only on hosting servers
if (hostname() !~ /^host/) {
  exit 0;
}

my @inboxen = glob('/var/spool/mail/*');
my @violators;

for my $inbox(@inboxen) {
  if (-s $inbox > 5000000) {
    push @violators, (split(/\//,$inbox))[-1];
  } else {
    next;
  } 
}

for my $offender(@violators) {
  print $offender . "\n";
}
