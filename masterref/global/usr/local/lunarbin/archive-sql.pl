#!/usr/bin/perl -w 

# MasterRef
# $Id: archive-sql.pl,v 1.1 2003/04/02 19:08:41 root Exp $

use strict;
use Sys::Hostname;

if (hostname() !~ /^host/) {
  exit 1;
}

my $mysqldump = `which mysqldump`; chomp $mysqldump;

my @domains = glob("/etc/hosting-options/*");

for my $i(@domains) {
  if ( -e "$i/mysql" ) {
    next if $i eq '/etc/hosting-options/.';
    next if $i eq '/etc/hosting-options/..';
    open(FH,"$i/mysql");
    my $database = <FH>; chomp $database;
    close(FH);
    my $domain = (split(/\//,$i))[-1];
    chomp $domain;
    system("$mysqldump -T /www/$domain/options/mysqldump --fields-terminated-by=',' $database");
  }
}

my $archive = '/usr/local/mysql-backup/system';
system("$mysqldump -T $archive --fields-terminated-by=',' mysql");
