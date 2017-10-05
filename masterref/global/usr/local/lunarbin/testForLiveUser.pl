#!/usr/bin/perl

use strict;
use warnings;

my $passFile = '/etc/passwd';

open(PW,$passFile);
while(<PW>) {
  my @entry = split(/:/,$_);
  if ($entry[2] > 499) {
    if (!-d $entry[5]) {
      print "$entry[0] -> " . (split(/\//,$entry[5]))[3] . "\n";
      print " Delete this user? ";
      my $answer = <STDIN>; chomp $answer;
      if ($answer eq 'y') {
        system("userdel -r $entry[0]");
      } else {
        next 
      }
    }
  }
}
close(PW);
