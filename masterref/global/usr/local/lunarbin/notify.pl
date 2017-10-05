#!/usr/bin/perl -w

# MasterRef
# $Id: notify.pl,v 1.2 2003/04/25 17:20:57 root Exp $

# This script will check the 5 minute load avg for the machine via
# the /proc/loadavg file. If the load is above 5.00 the script will
# then page the machine admin notifying them of the high system load.

use strict;
use Mail::Mailer;
use POSIX qw(strftime);
use Sys::Hostname;

my $threshold;
if (hostname() =~ /^name2/) {
  $threshold = '5';
} else {
  $threshold = '3';
}
my $loadfile  	= '/proc/loadavg';
my $stopfile  	= '/var/run/notify.stop';
my $logfile	= '/var/log/notify';
my $date	= strftime("%Y%m%d %H:%M:%S", localtime);

## mail settings
my $to    	= 'emergency-pager';
my $bcc		= 'host-alarm@lunarhosting.net';
my $from      	= 'cmenzes@lunarmedia.net';

## get the current 5 minute average
open(FH,"$loadfile");
my $avg = (split(/ /, <FH>))[1];
close(FH);

## test to see if there is a stop file
if ( -e "$stopfile" ) {
  ## check to see if host is still running hot
  if ($avg > $threshold) {
    open(LOG,">>$logfile");
    print LOG "$date (PERSIST) - Average:$avg (Stopfile Present)\n";
    exit 0;
  } else {
    &notify('recover');
    unlink $stopfile;
    open(LOG,">>$logfile");
    print LOG "$date (RECOVERY) - Average:$avg (Stopfile Removed)\n"; 
    close(LOG);
    exit 0;
  }
} else {
  ## compare current 5 min avg to threshold
  if ($avg > $threshold) {
    &notify('alarm');
    open(FH,">$stopfile"); 
    print FH "$date -> $avg";
    close(FH);
    open(LOG,">>$logfile");
    print LOG "$date (ALARM) - Average:$avg (Stopfile Created)\n";
    close(LOG);
  } else {
    exit 0;
  }
}

sub notify {
  my $action = shift;

  my $hostname = uc(hostname());

  my $subject = uc($action);
  $subject    .= " - $hostname Load Average :";
  $subject    .= " $avg";

  my $mailer = Mail::Mailer->new();

  $mailer->open({
                        To      => "$to",
                        Bcc     => "$bcc",
                        Subject => "$subject",
                        From    => "$from",
  });

  $mailer->close;

}
