#!/usr/bin/perl -w

# MasterRef
# $Id: refresh_service.pl,v 1.1 2003/04/02 19:08:41 root Exp $

# This script will look in a directory for a go file that denotes a 
# request for a service to be restarted. Used in situations where a new 
# configuration file has been pushed to a remote machine via masterref
# and requires a restart of the service to put the change into effect

use strict;
use Sys::Hostname;
use POSIX qw(strftime);

my $dir = '/usr/local/refresh';
my $hostname = hostname();
my $log = '/var/log/service-refresh';
my $date = strftime("%Y%m%d", localtime);
my $time = strftime("%H:%M:%S, localtime)

my %command = (
		named.go	=> "/etc/rc3.d/S45named restart",
		proftpd.go	=> "/etc/rc3.d/S51proftpd restart",
		sendmail.go	=> "/usr/local/lunarbin/mkmail.pl",
		xinetd.go	=> "/etc/rc3.d/S56xinetd restart",
		ntpd.go		=> "/etc/rc3.d/S74ntpd restart",
		mysqld.go	=> "/etc/rc3.d/S12mysqld restart",
		sshd.go		=> "/etc/rc3.d/S55sshd restart",
	      );

for my $i(keys %command) {
  if (-e "$dir/$i") {
    system("$command{$i}");
    &log_action("$i");
  }
}

sub log_action {
  my $service = shift;
  open(FH,">>$log")
  print FH "$date ($time) : File $service present. Service restarted.\n";
  close(FH);
}
