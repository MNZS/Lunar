#!/usr/bin/perl -w

use strict;
use Sys::Hostname;
use Mail::Mailer;
use Lunar::Users;

my $shell = 'sh(?:2)?$';

my %validUsers = ( cmenzes => '1',
		   root => '1',
                   craig => '1',
                   scott => '1', );

if (hostname() =~ /^name/) {
  $validUsers{dnsupdate} = '1';
}

my %shellUsers = getUsers('all');

for my $user(keys %shellUsers) {
  if ($shellUsers{$user}{'shell'} =~ /$shell/ ) {
    &notify($user) unless ($validUsers{$user});
  }
}

sub notify {
 my $login = shift;
 my $hostname = hostname();
 
 my %mailFrom = ( from => 'admin@lunarhosting.net',
                  to => 'emergency-pager', );
 
 my $subject = "ALARM: $login has valid shell on $hostname";
 
  my $mailer = Mail::Mailer->new();
                                                                                
  $mailer->open({
                        To      => "$mailFrom{to}",
                        Subject => "$subject",
                        From    => "$mailFrom{from}",
  });
                                                                                
  $mailer->close;
}

