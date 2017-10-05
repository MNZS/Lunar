#!/usr/bin/perl -w

# MasterRef
# $Id: named_update.pl,v 1.3 2003/06/27 21:00:20 root Exp $

# This script will check to see if a 'go' file exists for
# the named service. The 'go' file is a plain 0 length file
# written to the local server by a remote hosting server to
# indicate that an updated hostX.lunarhosting.net named
# configuration file has been written to the server and 
# needs to be read to update the local machine's named params.
#
# The presence of a 'go' file will cause this script to 
# restart named. At the end of the script, the go file will 
# be removed.
#

use strict;
use POSIX qw(strftime);
use Sys::Hostname;
use Socket;
use File::Copy;

# only run this script on a nameserver
if (hostname() !~ /^name/) {
  exit 1;
}

my $go_file = '/var/named/run/named.go';
my $stop  = '/etc/rc3.d/S45named stop';
my $start = '/etc/rc3.d/S45named start';
my $logfile = '/var/log/named/named.go';

my $time = strftime("%H:%M:%S",localtime);
my $date = strftime("%Y%m%d",localtime);

if ( -e $go_file ) {

  ## create a new /etc/mail/access file based on new domain list
  system("/usr/local/lunarbin/mkrelay.pl");
  ## create a new /etc/mail/spamassassin/local/cf file
  system("/usr/local/lunarbin/spamGenWhitelist.pl");

  ## restart named to re-read in configuration files
  system("$stop");
  sleep 2;
  system("$start");
  sleep 2;

  &log_action();

  unlink $go_file;

  exit 0;

} else {

  exit 0;

}

sub log_action {

  my $date = strftime("%b %d %Y",localtime);

  ## log which host the file was written by?
  open(FH,">>$logfile")
    or warn "Can't open Logfile : $!\n";

  print FH "$date -$time - named restarted to include the following updates:\n";

  open(GO,"$go_file") 
    or die "Can't open go file : $!\n";

  while ( my $i = <GO> ) {

    print FH $i;

  }

  close(GO);
  close(FH);

}

