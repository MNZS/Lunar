#!/usr/bin/perl -w

# $Id: date.cgi,v 1.5 2001/11/27 16:43:38 root Exp $

use strict;
use POSIX qw(strftime);

## cgi.pm param
use CGI;
$CGI::DISABLE_UPLOADS = 1;
$CGI::POST_MAX = 1024;
my $query = new CGI;
$query = CGI->new();

my %formdata;
my @formfields = $query->param;

for my $field(@formfields) {
  $formdata{$field} = $query->param($field);
}

## taint environmentals
delete @ENV{qw(IFS CDPATH ENV BASH_ENV)};
$ENV{'PATH'} = "/usr/local/jail";

## select style of date representation

my $date;

## 26 November 2001
if ($formdata{style} == "1") {
  $date = strftime("%e %B %Y", localtime);

## November 2001
} elsif ($formdata{style} == "2") {
  $date = strftime("%B %Y", localtime);

## November 26
} elsif ($formdata{style} == "3") {
  $date = strftime("%B %e", localtime);

## 26 November
} elsif ($formdata{style} == "4") {
  $date = strftime("%e %B", localtime);

## Nov 26, 2001
} elsif ($formdata{style} == "5") {
  $date = strftime("%b %e, %Y", localtime);

## 26 Nov, 2001
} elsif ($formdata{style} == "6") {
  $date = strftime("%e %b, %Y", localtime);

## Nov 2001
} elsif ($formdata{style} == "7") {
  $date = strftime("%b %Y", localtime);

## Nov 16
} elsif ($formdata{style} == "8") {
  $date = strftime("%b %e", localtime);

## November
} elsif ($formdata{style} == "9") {
  $date = strftime("%B", localtime);

## Nov
} elsif ($formdata{style} == "10") {
  $date = strftime("%b", localtime);

## 26 Nov
} elsif ($formdata{style} == "11") {
  $date = strftime("%e %b", localtime);

## 11/26/2001
} elsif ($formdata{style} == "12") {
  $date = strftime("%m/%e/%Y", localtime);

## 11/26/01
} elsif ($formdata{style} == "13") {
  $date = strftime("%m/%e/%y", localtime);

## 11/26
} elsif ($formdata{style} == "14") {
  $date = strftime("%m/%e", localtime);

## 11/2001
} elsif ($formdata{style} == "15") {
  $date = strftime("%m/%Y", localtime);

## 26/11/2001
} elsif ($formdata{style} == "16") {
  $date = strftime("%e/%m/%Y", localtime);
 
## 26/11/01
} elsif ($formdata{style} == "17") {
  $date = strftime("%e/%m/%y", localtime);

## 26/11
} elsif ($formdata{style} == "18") {
  $date = strftime("%e/%m", localtime);

## 2001
} elsif ($formdata{style} == "19") {
  $date = strftime("%Y", localtime);

## 2001/11/26
} elsif ($formdata{style} == "20") {
  $date = strftime("%Y/%m/%e", localtime);

## 2001/11
} elsif ($formdata{style} == "21") {
  $date = strftime("%Y/%m", localtime);

## 20011126
} elsif ($formdata{style} == "22") {
  $date = strftime("%Y%m%d", localtime);

## 200111 
} elsif ($formdata{style} == "23") {
  $date = strftime("%Y%m", localtime);

## Monday, Tuesday, etc...
} elsif ($formdata{style} == "24") {
  $date = strftime("%A", localtime);

## Mon, Tue, etc...
} elsif ($formdata{style} == "25") {
  $date = strftime("%a", localtime);

## end of if loop
} else {
  $date = strftime("%B %e, %Y", localtime);

}

print "Content-type: text/html\n\n";
print $date;
