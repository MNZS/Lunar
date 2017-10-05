#!/usr/bin/perl -w

use strict;
use Cwd;

my $domain = (split /\//, cwd())[-2];
my @mypic;
my @myurl;

$|=1;

## this content dynamically generated

## START
## END
## end of dynamically generated content
 
## generate random number
srand(time ^ $$);

## pick number from the hat
my $pick = rand(@mypic);

## print out results
print qq|Content-type: text/html\n\n|;
print qq|<A HREF="$myurl[$pick]"> <IMG SRC="http://www.$domain/images/$mypic[$pick]></A>|;

