#!/usr/bin/perl -w

# $Id: archive-cleanse.pl,v 1.5 2003/10/02 12:55:16 root Exp $

use strict;
use POSIX qw(strftime);
use Date::Manip;
use Sys::Hostname;

## only run on archives.lunarhosting.net
if (hostname() ne 'name2.lunarhosting.net') {
  exit;
}

if (-e '/usr/local/nobackups') {
  exit 0;
}

# check for global stop file
require '/usr/local/lunarbin/check_lockfile.pl';

## hosting servers with archive directories
my @hostServers = qw(host1.lunarhosting.net host2.lunarhosting.net);

## number of days to go back for directory deletion

# sun mon tue wed thu fri sat 

# 4 days worth of backups
#my %pastDays = ( 'sun' => '0',
#		 'mon' => '0',
#		 'tue' => '6',
#		 'wed' => '6',
#		 'thu' => '6',
#		 'fri' => '6',
#		 'sat' => '4',
#	       );

# 3 days worth of backups
my %pastDays = ( 'sun' => '0',
                'mon' => '0',
                'tue' => '5',
                'wed' => '5',
                'thu' => '5',
                'fri' => '3',
                'sat' => '3',
              );

## find today three character code
my $today = lc(strftime("%a",localtime));

## find date for X number of days ago in YYYYMMDD format
my $targetDir = &ParseDateDelta("$pastDays{$today} days ago");
$targetDir = &UnixDate("$targetDir","%Y%m%d");
exit if ($targetDir eq '');

## WWW archive directory
my $archiveDir = '/usr/local/archives';

## march the lemmings to the edge
for my $hostName(@hostServers) {
  if (-d "$archiveDir/$hostName/$targetDir") {
    system("rm -rf $archiveDir/$hostName/$targetDir");
  }
}
