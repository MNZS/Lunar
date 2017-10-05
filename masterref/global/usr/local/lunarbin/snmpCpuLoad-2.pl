#!/usr/bin/perl -w

# $Id: snmpCpuLoad.pl,v 1.23 2003/04/15 15:59:37 root Exp $

# This script polls a remote server using SNMP for the machine's
# 5 minute CPU load average and adds the value to an RRD database.
# Then graphs the last 8 hours of 5 minute averages as well as
# the last 24 hour period.

# This script requires that you have the RRDtool installed
# on your system as well as the RRDtool perl modules compiled.
# Read the RRD documentation on how to install.

# The RRDTool and all of its installation directions are found at:
# http://people.ee.ethz.ch/~oetiker/webtools/rrdtool/index.html

# The images created are in the .GIF format. 
# 8 Hour graph is created as sysload-8.gif
# 24 Hour graph is created as sysload-24.gif

use strict;
use RRDs;
use Sys::Hostname;
use Net::SNMP;

## only run on name1 and name2
if (hostname() !~ /^name/) {
  exit 1;
}

my $serverCommunity = 'Wl7d0w%!';
my $routerCommunity = 'monitor';
my $serverOid = '.1.3.6.1.4.1.2021.10.1.3.2';
my $routerOid = '.1.3.6.1.4.1.9.2.1.58.0';

## define our remote hosts
my %nodes = ( 
	'host1' => {
		'hardware' => 'servers',
		'oid' => "$serverOid",
  		'community' => "$serverCommunity",
		'threshold' => '3',
		},
	'host2' => {
                'hardware' => 'servers',
                'oid' => "$serverOid",
                'community' => "$serverCommunity",
		'threshold' => '3',
                },
	'name1' => {
                'hardware' => 'servers',
                'oid' => "$serverOid",
                'community' => "$serverCommunity",
		'threshold' => '3',
                },
	'name2' => {
                'hardware' => 'servers',
                'oid' => "$serverOid",
                'community' => "$serverCommunity",
		'threshold' => '3',
                },
	'gateway' => {
                'hardware' => 'routers',
                'oid' => "$routerOid",
                'community' => "$routerCommunity",
		'threshold' => '40',
                },
);

#            NO FURTHER EDITING SHOULD BE REQUIRED            #
###############################################################

my $rrd = 'cpu_trend.rrd';
my $end = time();

for my $host(keys %nodes) {

  ## 
  my $alarm = 'off';

  ## define the working directory
  ## this should be the area where your .rrd file exists
  ## it should be an absolute path begining with a /
  my $rrd_dir = "/usr/local/mrtg/$nodes{$host}->{hardware}/$host/cpu";

  ## define the image directory
  ## this should be your web accessible directory 
  ## it should be an absolute path begining with a /
  my $img_dir = $rrd_dir;

  &test_if_complete($rrd_dir);

  my $avg = &get_latest_avg($host);

  if (!$avg) {
    $avg = '0';
    $alarm = 'on';
  }

  &update_rrd($rrd_dir,$avg);

  &make_graph('8',$host,$rrd_dir);

  &make_graph('24',$host,$rrd_dir);

  if ($alarm eq 'on') {
    &testForLife("$host");
  } else {
    &testForHighCpu;
  }

}

#                       SUB-ROUTINES			      #
###############################################################

sub test_if_complete {

  my $dir = shift;

if ( !$dir ) {

print <<RRD;

You need to define your RRD repository!
This is the directory on your server where
your .rrd database will reside. It should
be outside of web accessible space.

You can define this value by editing the
\$rrd_dir variable in this script.
This value should be an absolute path but
not include a trailing slash.

RRD

exit 1;

} elsif ( !$dir ) {

print <<IMG;

You need to define your Image repository!
This should be a directory that is accesible
via the web.

You can define this value by editing the 
\$img_dir variable in this script.
This value should be an absolute path but
not include a trailing slash.

IMG

exit 1;

} elsif ( ! -e "$dir/$rrd" ) {

print <<CREATE;

Hang on, your RRD database is being created!
This will only need to be done once, so you
shouldn't see this messsage again.

CREATE

RRDs::create("$dir/$rrd",
             "DS:sysload:GAUGE:600:U:U",
             "RRA:AVERAGE:0.5:1:288" );
my $ERR=RRDs::error;
die "ERROR while creating $dir/$rrd: $ERR\n" if $ERR;

print <<DONE;

Congratulations! Your RRD database has been
created! You should now be able to start 
adding data and creating graphs. 
Try running this script by hand now to make
sure that no errors occur.
To automate data collection, you can add an
entry to your crontab that should look something
like this

*/5 * * * *	/path/to/this/script >/dev/null 2>&1

DONE

exit 0;

}

## end of subroutine
}

sub get_latest_avg {
  my $host = shift;

  my $snmp = Net::SNMP->session(
		-hostname	=> $host,
		-version	=> '1',
		-community	=> $nodes{$host}->{community}, );

  my $num = $snmp->get_request( -varbindlist => [$nodes{$host}->{oid}] );

  my $avg = $num->{$nodes{$host}->{oid}};

  return $avg;

}

sub update_rrd {

  my $dir = shift;
  my $avg = shift;

  RRDs::update("$dir/$rrd","N:$avg");
  my $ERR=RRDs::error;
  die "ERROR while updating $rrd: $ERR\n" if $ERR;
}

sub make_graph {

  my $interval = shift;
  my $hostname = shift;
  my $dir = shift;

  my $print_hour = $interval / 8;

  my $start = $end - ($interval * 3600);

  RRDs::graph("$dir/sysload-$interval.gif",
              "--start","$start",
              "--end","$end",
              "--title","System Load for $hostname over past $interval hours",
              "--vertical-label","5 Minute Average",
              "-x","MINUTE:60:HOUR:$print_hour:HOUR:$print_hour:0:%k",
              "-l","0",
              "--units-exponent","0",
              "DEF:mycpu=$dir/cpu_trend.rrd:sysload:AVERAGE",
              "AREA:mycpu#999999:5 Minute Average", );
#              "HRULE:1#FF3300:Threshold", );

  my $ERR=RRDs::error;
  die "ERROR while graphing $rrd: $ERR\n" if $ERR;

}

sub testForHighCpu {

}

sub testForLife {

}
exit 0;
