#!/usr/bin/perl -w

# $Id: mkrelay.pl,v 1.18 2003/08/27 19:02:25 root Exp $

use strict;
use Sys::Hostname;
use Rcs;

# run only on nameservers
if (hostname() !~ /^name/) {
  exit 1;
}

&makeRelayFile;

## SubRoutines ########################################

sub makeRelayFile {
  my $accessFile = '/etc/mail/access';
  my $accessGlobal = '/etc/mail/include/access/global-config';
  my @zoneFiles = glob('/var/named/host*');
  push @zoneFiles, '/var/named/named.partners'; # 3rd party sites
  my @domainList;
  my $restart = '/usr/local/lunarbin/mkmail.pl';

  # collect list of our customer domains
  for my $file(@zoneFiles) {
    open(FH,"$file") or die "Can't open $file : $!\n";
    while (my $line = <FH>) {
      next unless ($line =~ /^zone/);
      chomp $line;
      # |zone "wilsonparkfuneralhome.com" in {|
      $line =~ s/^zone.+\"([\w\.\-]+)\".+{$/$1/g;
      next if ($line =~ /in-addr.arpa$/);
      push @domainList, $line;
    }
    close(FH);
  }

  # be redundant for other hosts as well as domains
  push @domainList, "host1.lunarhosting.net";
  push @domainList, "host2.lunarhosting.net";
  if (hostname() =~ /^name1/) {
    push @domainList, "name2.lunarhosting.net";
  } elsif (hostname() =~ /^name2/) {
    push @domainList, "name1.lunarhosting.net";
  } else {
    print "\nThis doesn't appear to be running on either nameserver!\n\n";
    exit;
  }


  # check out /etc/mail/access from rcs
  # print new list of domains
  # check in /etc/mail/access to rcs
  # restart sendmail
  my $rcs = Rcs->new;
  $rcs->file('access');
  $rcs->workdir('/etc/mail');
  $rcs->rcsdir('/etc/mail/RCS');
  $rcs->bindir('/usr/bin');
  $rcs->co('-l');
  open(FH,">$accessFile") or die "Can't open $accessFile : $!\n";
  # print global params
  open(GLOBAL,"$accessGlobal") or die "Can't open $accessGlobal : $!\n";
  my @global = <GLOBAL>;
  close(GLOBAL);
  for my $line(@global) {
    print FH $line;
  }
  # print per domain params
  for my $domain(sort @domainList) {
    print FH "$domain\tRELAY\n";
  }
  close(FH);
  $rcs->ci('-u','-mDomain Management');
  

  system("$restart");

}
