#!/usr/bin/perl -w

# $Id: spam_genwhitelist.pl,v 1.3 2003/06/27 20:55:02 root Exp $

use strict;
use POSIX qw(strftime);
use Sys::Hostname;
use Rcs;

## create a local.cf include file for spamassassin that will whitelist
## incoming mail with a from address that includes a domain name hosted
## with our company

## its a little broad to accept this mail as spammers will sometimes forge
## the from field, however until i see a large increase because of this,
## allowing these domains will prevent other headaches for mail between
## valid users.

## create two variables for documentation with file
my $date = strftime("%c",localtime);
my $hostname = hostname();

if ($hostname ne 'name2.lunarhosting.net') {
  exit 1;
}

## define files used
my $workdir = '/usr/local/masterref/global/etc/mail/spamassassin';
my $rcsdir = "$workdir/RCS";
my $local = "local.cf";

## get list of domains and place into an array
my $named_dir = "/var/named";
chdir $named_dir or die "Cant chdir to $named_dir : $!\n";
my @named_files = glob("host*");
my @domains;

for my $i(@named_files) {
  open(FH, "$named_dir/$i");
    while(<FH>) {
      my $line = $_;
      next unless $line =~ /^zone/;
      $line =~ s/^zone.+\"(.*)\".+{.*/$1/g; 
      chomp $line;
      next if $line =~ /in-addr/;
      push @domains, $line;
    }
  close(FH);
}

## checkout the whitelist file for writing
my $rcs = Rcs->new;

## check out the whitelist
$rcs->bindir('/usr/bin');
$rcs->workdir($workdir);
$rcs->rcsdir($rcsdir);
$rcs->file($local);
$rcs->co('-l');

## open local file for writing
open(FH,">$workdir/$local")
  or die "Can't write to $local : $!\n";

print FH "\#\# Created: $date\n\#\# Held in masterref files on $hostname\n\n";

for my $i(sort @domains) {
  print FH "whitelist_from\t\*\@$i\n";
}

close(FH);

## check the local.cf file back in
$rcs->bindir('/usr/bin');
$rcs->workdir($workdir);
$rcs->rcsdir($rcsdir);
$rcs->file($local);
$rcs->ci('-u', "-mSync'ing file for change in domain list");

