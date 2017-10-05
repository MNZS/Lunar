#!/usr/bin/perl -w

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

## declare variable
my $time;

## make judgement on how time is displayed
if ($formdata{style} == "1") {
  ## 10:30:15 AM
  $time = strftime("%r", localtime);

} elsif ($formdata{style} == "1") {
  ## 10:30 AM
  $time = strftime("%l:%M", localtime);

} elsif ($formdata{style} == "2") {
  ## 10 AM
  $time = strftime("%l %p", localtime);

} elsif ($formdata{style} == "3") {
  ## 10:30:15
  $time = strftime("%l:%M:%S", localtime);

} elsif ($formdata{style} == "4") {
  ## 10:30
  $time = strftime("%l:%M", localtime);

} elsif ($formdata{style} == "5") {
  ## 10
  $time = strftime("%l", localtime);

} elsif ($formdata{style} == "6") {
  ## 22:30:15
  $time = strftime("%X", localtime);

} elsif ($formdata{style} == "7") {
  ## 22:30
  $time = strftime("%k:%M", localtime);

} elsif ($formdata{style} == "8") {
  ## 22
  $time = strftime("%k", localtime);

} else {
  ## 10:30 AM  ## default
  $time = strftime("%l:%M %p", localtime);

}

## print out content type and time
print "Content-type: text/html\n\n";
print $time;
