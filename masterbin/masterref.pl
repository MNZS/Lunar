#!/usr/bin/perl -w

# get a confirm before action takes place
# go through guarded files and make sure they have rcs tags

# $Id: masterref.pl,v 1.68 2003/08/13 19:59:35 root Exp $

# Keep global files on remote machines in sync

use strict;
use Sys::Hostname;
use Getopt::Long;
use POSIX qw(strftime);
use Parallel::ForkManager;

my @hosts = qw(
		host1
		host2
		name1
		name2
	      );

# command line arguments
my $host;
my $list;
my $regex;
my $all;
GetOptions (
	'all'		=> \$all,
	'host=s'	=> \$host,
	'list'		=> \$list,
	'regex=s'	=> \$regex,
);


# masterref sources
my $sourceDir = '/usr/local/masterbin/sources';
my $user = 'root@';

# rsync arguments
my $sshPort = '9490';
my $rsync = `which rsync`; chomp $rsync;
my $ssh = `which ssh`; chomp $ssh;
my $args = '-qavPH';
#my $delete = '--partial --delete --delete-after';
my $delete = '--delete';
my $exclude = '--exclude=RCS*';
my $shell = qq|-e "$ssh -p $sshPort"|; 
my $cli = "$rsync $args $delete $exclude $shell";

# ensure the script is being ran on masterref
if (hostname() ne 'name2.lunarhosting.net') {
  print "\nThis script may only be ran on masterref!\n\n";
  exit 1;
}

if ($list) {
  print "\n";
  for my $server(@hosts) {
    print "$server\n";
  }
  print "\n";
  exit 0;
}

if ($all) {
  $regex = '.*';
}

## ensure the correct hosts are selected
print "You have selected to push files to the following hosts:\n";
for my $server(@hosts) {
  ## if host is specified, do filtering
  if ($host) {
    next if $server !~ /^$host$/;
    print "  $server\n";
  } elsif ($regex) {
    next if $server !~ /$regex/;
    print " $server\n";
  } else {
    exit 1;
  }
}
print "\n";
print "Would you like to continue? (y/N) ";
my $answer = <STDIN>;
chomp $answer;
if ($answer ne 'y') { print "\nNo hosts were processed.\n\n"; exit 1; };

open(SRC,"$sourceDir/global")
  or die "Can't open Source File : $!\n";
my @sourceGlobal = <SRC>;
close(SRC);

# create start time
my $startTime = strftime("%X",localtime);

my $process = new Parallel::ForkManager('10');

# push files out
for my $server(@hosts) {
  ## if host is specified, do filtering
  if ($host) {
    next if $server !~ /^$host$/;
  } elsif ($regex) {
    next if $server !~ /$regex/;
  } else {
    exit 1;
  }

  $process->start and next;

  ## 
  print "Beginning ref for $server...\n";

  ## go over the list
  for my $line(@sourceGlobal) {
    chomp $line;
    next if $line =~ /^$/;
    next if $line =~ /^#/;
    my ($src,$dst) = split(/ /,$line);
    my $display = $src;
    $display =~ s/^\/usr\/local\/masterref\/(?:global|common|unique)?(?:\/(?:host1|host2|name1|name2))?//g;
    system("$cli $src $user$server:$dst");
  }

  if ( -e "$sourceDir/$server" ) {
    open(HOST,"$sourceDir/$server")
      or die "Can't open $sourceDir/$server : $!\n";
    my @sourceHost = <HOST>;
    close(HOST);
    for my $line(@sourceHost) {
      chomp $line;
      next if $line =~ /^$/;
      next if $line =~ /^#/;
      my ($src,$dst) = split(/ /,$line);
      my $display = $src;
      $display =~ s/^\/usr\/local\/masterref\/(?:global|common|unique)?(?:\/(?:host1|host2|name1|name2))?//g;
      system("$cli $src $user$server:$dst");
    }
  }

  ##
  print "End of ref for $server...\n";

  $process->finish;
}

$process->wait_all_children;

my $endTime = strftime("%X",localtime);

print "MasterRef Session Summary\n  Start Time:\t$startTime\n  End Time:\t$endTime\n";

exit;
