#!/usr/bin/perl -w

# $Id: snmpMemLoad.pl,v 1.29 2003/08/14 21:49:32 root Exp $

# This script polls a remote server using SNMP for the machine's
# swap and real memory values and adds the value to an RRD database.
# Then graphs the last 8 hours of 5 minute averages as well as
# the last 24 hour period.

# This script requires that you have the RRDtool installed
# on your system as well as the RRDtool perl modules compiled.
# Read the RRD documentation on how to install.

# The RRDTool and all of its installation directions are found at:
# http://people.ee.ethz.ch/~oetiker/webtools/rrdtool/index.html

# The images created are in the .GIF format. 
# 8 Hour graph is created as memload-8.gif
# 24 Hour graph is created as memload-24.gif

use strict;
use RRDs;
use Sys::Hostname;
use Net::SNMP;
use Lunar::Hosts;
use Lunar::Restrict;

## only run on name1 and name2
&limitHost('^name');

my $memTotalSwap 	= '.1.3.6.1.2.1.25.2.3.1.5.102';
my $memUsedSwap 	= '.1.3.6.1.2.1.25.2.3.1.6.102';
my $memTotalReal 	= '.1.3.6.1.2.1.25.2.3.1.5.101';
my $memUsedReal 	= '.1.3.6.1.2.1.25.2.3.1.6.101';

## define our remote hosts
my %nodes = &getHosts('linux');

#            NO FURTHER EDITING SHOULD BE REQUIRED            #
###############################################################

my %rrd = (
	'real_trend' => {
		'total'	=> $memTotalReal,
		'used'	=> $memUsedReal,
		'desc' 	=> 'Physical Memory',
		},
	'swap_trend' => {
		'total'	=> $memTotalSwap,
		'used' 	=> $memUsedSwap,
		'desc' 	=> 'Swap Memory',
 		},
);

my $end = time();

for my $host(sort keys %nodes) {

  ## define the working directory
  ## this should be the area where your .rrd file exists
  ## it should be an absolute path begining with a /
  my $rrd_dir = "/usr/local/mrtg/$nodes{$host}->{hardware}/$host/mem";

  ## define the image directory
  ## this should be your web accessible directory 
  ## it should be an absolute path begining with a /
  my $img_dir = $rrd_dir;

  for my $rrd(keys %rrd) {
    &test_if_complete($rrd_dir,$rrd);
  }
 
  for my $rrd(keys %rrd) {
    my $avg = &get_latest_avg($host,$rrd,'used');
    &update_rrd($rrd_dir,$avg,$rrd);
    &make_graph('8',$host,$rrd_dir,$rrd);
    &make_graph('24',$host,$rrd_dir,$rrd);
    &make_graph('168',$host,$rrd_dir,$rrd);
  }
}

#                       SUB-ROUTINES			      #
###############################################################

sub test_if_complete {

  my $dir = shift;
  my $rrd = shift;
  $rrd .= '.rrd';

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
You can define this value by editing the 
\$img_dir variable in this script.
This value should be an absolute path but
not include a trailing slash.

IMG

exit 1;

} elsif ( ! -d $dir ) {
  mkdir($dir) or die "Can't create the RRD Directory: $!\n";

} elsif ( ! -e "$dir/$rrd" ) {

print <<CREATE;

Hang on, your RRD database is being created!
This will only need to be done once, so you
shouldn't see this messsage again.

CREATE

RRDs::create("$dir/$rrd",
             "DS:memfree:GAUGE:600:U:U",
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
  my $rrd = shift;
  my $type = shift;

  my $snmp = Net::SNMP->session(
		-hostname	=> $host,
		-version	=> '1',
		-community	=> $nodes{$host}->{community}, );

  my $num = $snmp->get_request( -varbindlist => [$rrd{$rrd}->{$type}] );

  my $avg = $num->{$rrd{$rrd}->{$type}};

  $snmp->close;

  return $avg;

}

sub update_rrd {

  my $dir = shift;
  my $avg = shift;
  my $rrd = shift;
  $rrd .= '.rrd';

  RRDs::update("$dir/$rrd","N:$avg");
  my $ERR=RRDs::error;
  die "ERROR while updating $rrd: $ERR\n" if $ERR;
}

sub getTotalMem {
  my $host = shift;
  my $rrd = shift;

  my $snmp = Net::SNMP->session(
                -hostname       => $host,
                -version        => '1',
                -community      => $nodes{$host}->{community}, );
                                                                                                                             
  my $num = $snmp->get_request( -varbindlist => [$rrd{$rrd}->{'total'}] );
                                                                                                                             
  my $totalMem = $num->{$rrd{$rrd}->{'total'}};

  $snmp->close;

  return $totalMem;
}
 
sub make_graph {

  my $interval = shift;
  my $hostname = shift;
  my $dir = shift;
  my $rrd = shift;

  my $totalMem = &getTotalMem($hostname,$rrd);

  my $db = $rrd . '.rrd';

  my $print_hour = $interval / 8;

  my $start = $end - ($interval * 3600);

  my $graph = "$dir/$rrd" . "-free-$interval.gif";

  RRDs::graph("$graph",
              "--start","$start",
              "--end","$end",
              "--title","$rrd{$rrd}{'desc'} Used for $hostname over past $interval hours",
              "--vertical-label","5 Minute Interval",
              "-x","MINUTE:60:HOUR:$print_hour:HOUR:$print_hour:0:%k",
              "-l","0",
#              "--units-exponent","0",
              "DEF:mycpu=$dir/$db:memfree:AVERAGE",
              "AREA:mycpu#999999:5 Minute Average", 
              "HRULE:$totalMem#FF3300:Total Memory = $totalMem", );

  my $ERR=RRDs::error;
  die "ERROR while graphing $rrd: $ERR\n" if $ERR;

}

exit 0;
