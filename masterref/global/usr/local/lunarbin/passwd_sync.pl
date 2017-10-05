#!/usr/bin/perl -w

# $Id: passwd_sync.pl,v 1.4 2003/07/30 20:58:41 root Exp $


exit;


use strict;
use Net::SSH qw(ssh);
use Sys::Hostname;

# Script will synchronize the password used on name2 with all other 
# lunar servers for a specific user.
# In order for user to be eligible for for password synchronization,
# the username needs to be present in the privelaged group as listed

if (hostname() ne 'name2.lunarhosting.net') {
  print "Must be ran from name2!\n";
  exit 1;
}

# check for global stop file
require '/usr/local/lunarbin/check_lockfile.pl';

# list of hosts where password should be copied
my @hosts = qw(	name1.lunarhosting.net
		host1.lunarhosting.net 
		host2.lunarhosting.net );

my %users = &createUserList;

&comparePasswd;

&syncPasswd;

## subroutines #####################################################

sub createUserList {
  my $group  = 'privelaged';
  my $file   = '/etc/group';
  my $shadow = '/etc/shadow';
  my %users;

  open(FH,"$file")
    or die "Can't open $file : $!\n";
  while(my $line = <FH>) {
    next unless ($line =~ /^privelaged:/);
    chomp $line;
    my $csv = (split(/:/,$line))[-1];
    my @list = split(/,/,$csv);
    for my $user (@list) {
      open(PW,"$shadow")
        or die "Can't open shadow file : $!\n";
      while(my $entry = <PW>) {
        next unless ($entry =~ /^$user:/);
        my $passwd = (split(/:/,$entry))[1];
        $users{$user} = "$passwd";
      }
      close(PW);
    }
  }
  close(FH);
  return %users;
}

sub syncPasswd {
  for my $server(@hosts) {
    my $ssh = 'root@';
    $ssh .= "$server";
    for my $user(keys %users) {
      my $command = 'usermod -p ';
      $command .= qq|'$users{$user}' |;
      $command .= "$user";
      ssh("$ssh","$command");
    }
    ssh("$ssh",'/usr/local/lunarbin/panelpasswd.pl');
  }
}

sub comparePasswd {
  my $flag = 0;

}
