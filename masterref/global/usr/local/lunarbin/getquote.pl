#!/usr/bin/perl -w

# MasterRef
# $Id: getquote.pl,v 1.1 2003/04/02 19:08:41 root Exp $

use URI::URL;
use LWP::UserAgent;
use Sys::Hostname;

if (hostname() ne 'host1.lunarhosting.net') {
  exit 1;
}

my $to = 'JPY';
my $from = 'USD';

my $agent = new LWP::UserAgent;

my $request = new HTTP::Request 'POST','http://www.oanda.com/convert/classic';
$request->content_type('application/x-www-form-urlencoded');

my $url = url("http:");

my %form = ( value => '1', exch => $from, expr=> $to);

$url->query_form(%form);
$request->content($url->equery);

my @result = $agent->request($request)->as_string;

open(FH, ">/www/kna-pacific.com/options/icb/quote");

print FH @result;

close(FH);
