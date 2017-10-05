#!/usr/bin/perl 

# MasterRef
# $Id: daemonwatch.pl,v 1.4 2003/09/17 15:22:38 root Exp $

## This script will run to ensure that the server is listening on 
## specific TCP ports. If a connection to the port fails, a page 
## will be sent to an administrator.

use strict;
use IO::Socket;
use Sys::Hostname;
use Mail::Mailer;
use POSIX qw(strftime);

my %services = (
		 sshd	  => '9490',
	       );

## set up logging and notification values
my $logfile = '/var/log/daemonwatch';
my $date = strftime("%Y%m%d",localtime);
my $time = strftime("%H:%M:%S",localtime);
my $to = 'emergency-pager';
my $from = 'daemonwatch@lunarhosting.net';

## set up values for socket
my $proto = 'tcp';
my $false = 0;
my $hostname = hostname();
my $host = gethostbyname("$hostname");
my $ip = inet_ntoa("$host");

## extra services for hosting servers
if ($hostname =~ /^host/) {
  $services{pop3} = '110';
  $services{proftpd} = '21';
  $services{mysql} = '3306';
  $services{smtpd} = '25';
  $services{httpd} = '80';
}

for my $daemon(keys %services) {
  my $disco = '0';
  my $checkport = IO::Socket::INET->new(
    PeerAddr => "$ip",
    PeerPort => "$services{$daemon}",
    Proto    => "$proto",
    Timeout  => '0',
  ) or $disco = "1";

  if ($disco) {
    &notify("$daemon");
    &log_action("$daemon");
  }

  close $checkport if (!$disco);
}

sub log_action {
  my $daemon = shift;
  open(FH,">>$logfile");
  print FH "$date $time $hostname not responding to $daemon:$services{$daemon}\n";
  close(FH);
}

sub notify {
  my $daemon = shift;
  my $subject = "$time - $hostname not listening on $services{$daemon}:$daemon";
  my $mailer = Mail::Mailer->new();

  $mailer->open({
                        To      => "$to",
                        Subject => "$subject",
                        From    => "$from",
  });

  $mailer->close;

}
