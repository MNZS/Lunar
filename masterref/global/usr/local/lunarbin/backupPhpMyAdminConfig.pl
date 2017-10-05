#!/usr/bin/perl -w

use strict;
use File::Copy;

my @dom = glob("/www/*");

for my $i(@dom) {
  if (-e "$i/options/mysql/config.inc.php") {
    my $foo = (split(/\//,$i))[2];
    copy("$i/options/mysql/config.inc.php","/usr/local/phpMyAdmin-config/$foo-config");
    print $foo . "\n";
  }
}
