#!/usr/bin/perl -w

use strict;

my $countfile = "/www/HOSTING_DOMAIN/options/counter.txt";

#################################################

## get the current count
open(FH, "$countfile")
  or die "Cant open counter file : $!\n";
  my $current = <FH>;
close(FH);

## increment the number by one
$current++;

## write the new number back to the count file
open(FH, ">$countfile")
  or die "Cant open counter file : $!\n";
  print FH $current;
close(FH);

## display the new number
print "Content-type: text/html\n\n";
print "$current\n";
