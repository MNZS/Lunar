#!/usr/bin/perl -w

# $Id: index.cgi,v 1.1 2002/06/21 21:22:19 root Exp $

use strict;
use POSIX qw(strftime);
use Cwd;
use Fcntl ':flock';
use File::Copy;

## specific modules for this script

## cgi.pm parameters
use CGI;
use CGI::Carp qw(fatalsToBrowser carpout);
$CGI::DISABLE_UPLOADS = 1;
$CGI::POST_MAX = 1024;
my $query = new CGI;
$query = CGI->new();

my %formdata;
my @formfields = $query->param;

for my $field(@formfields) {
  $formdata{$field} = $query->param($field);
  $formdata{$field} = uc($formdata{$field});
  $formdata{$field} =~ s/^(.{1,50})?.*/$1/g;
}

## taint environmentals
delete @ENV{qw(IFS CDPATH ENV BASH_ENV)};
$ENV{'PATH'} = "/usr/bin:/usr/local/bin";

## universal variables
my $domain = (split(/\//, cwd()))[-2];
my $rcs = (qw$Revision: 1.1 $)[-1];
my $images = "controlpanel/images";
$0 = (split(/\//, $0))[-1];
my $self = "controlpanel/$0";

## specific variables for this script
