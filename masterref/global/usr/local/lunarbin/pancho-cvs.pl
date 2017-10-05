#!/usr/bin/perl -w

use strict;
use Mail::Mailer;
use Sys::Hostname;
use POSIX qw(strftime);

my %validUsers = ( cmenzes => '1', 
		   craig => '1',
		   scott => '1', );

my %seenUsers;

my %validHosts = ( 'name2.lunarhosting.net' => '1' );

my @who = `who`;
my $hostname = hostname();

for my $login(@who) {
  chomp $login;
  $login =~ s/ +/CJM/g;
  my ($who,$where,$month,$day,$time,$from) = split(/CJM/,$login);
  next if $seenUsers{$who};
  if (!$validUsers{$who}) {
    &notify($login);
    &log($login);
    $seenUsers{$who} = '1';
  } #else {
    #&checkHost($login);
  #}
}

sub checkHost {
  my $login = shift;
  my ($who,$where,$month,$day,$time,$from) = split(/CJM/,$login);
  $from =~ s/[()]//g;
  if ($hostname =~ /^(?:host|name1)/) {
    if (!$validHosts{$from}) {
      &notify($login);
    }
  }
}

sub log {
 my $login = shift;
 my $date = strftime("%c",localtime);
 my ($who,$where,$month,$day,$time,$from) = split(/CJM/,$login);
 open(FH,">>/var/log/.pancho-cvs") or die "$!\n";
 print FH "$date\n  $who $where\t$month $day $time\t$from";
 close(FH);
}

sub notify {
 my $login = shift;
 my ($who,$where,$month,$day,$time,$from) = split(/CJM/,$login);

 my %mailFrom = ( from => 'admin@lunarhosting.net',
		  to => 'emergency-pager', );

 my $subject = "ALARM: $who logged into $hostname from $from";

  my $mailer = Mail::Mailer->new();
                                                                                
  $mailer->open({
                        To      => "$mailFrom{to}",
                        Subject => "$subject",
                        From    => "$mailFrom{from}",
  });
                                                                                
  $mailer->close;
}
