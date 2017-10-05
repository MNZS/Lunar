#!/usr/bin/perl -w

# $Id: tlc.pl,v 1.1 2003/04/02 19:08:41 root Exp $

# This script takes the 5 minute averages from /proc/loadavg
# seen within an hour and adds the value to an RRD database.
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

## define our hostname and format as we would like it
my $hostname = hostname();
$hostname = (split(/\./,$hostname))[0];

## define the working directory
## this should be the area where your .rrd file exists
## it should be an absolute path begining with a /
my $rrd_dir = "/usr/local/trends";

## define the image directory
## this should be your web accessible directory 
## it should be an absolute path begining with a /
my $img_dir = "/usr/local/trends";

#            NO FURTHER EDITING SHOULD BE REQUIRED            #
###############################################################

my $VERSION = '1.1';

my $end	= time();
my $avg_file = '/proc/loadavg';
my $rrd = 'cpu_trend.rrd';

&test_if_complete();

my $avg = &get_latest_avg();

&update_rrd();

&make_graph('8');

&make_graph('24');

#                       SUB-ROUTINES			      #
###############################################################

sub test_if_complete {

if ( !$rrd_dir ) {

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

} elsif ( !$img_dir ) {

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

} elsif ( ! -e "$rrd_dir/$rrd" ) {

print <<CREATE;

Hang on, your RRD database is being created!
This will only need to be done once, so you
shouldn't see this messsage again.

CREATE

RRDs::create("$rrd_dir/$rrd",
             "DS:sysload:GAUGE:600:U:U",
             "RRA:AVERAGE:0.5:1:288" );
my $ERR=RRDs::error;
die "ERROR while creating $rrd_dir/$rrd: $ERR\n" if $ERR;

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
  ## grab our latest 5 minute load average
  open(FH,$avg_file)
    or die "Can't open $avg_file : $!\n";

  my $avg = (split(/ /,<FH>))[1]; chomp $avg;

  close(FH);

  return $avg;

}

sub update_rrd {

  RRDs::update("$rrd_dir/$rrd","N:$avg");
  my $ERR=RRDs::error;
  die "ERROR while updating $rrd: $ERR\n" if $ERR;
}

sub make_graph {

  my $interval = shift;

  my $print_hour = $interval / 8;

  my $start = $end - ($interval * 3600);

  RRDs::graph("$img_dir/sysload-$interval.gif",
              "--start","$start",
              "--end","$end",
              "--title","System Load for $hostname over past $interval hours",
              "--vertical-label","5 Minute Average",
              "-x","MINUTE:60:HOUR:$print_hour:HOUR:$print_hour:0:%k",
              "-l","0",
              "--units-exponent","0",
              "DEF:mycpu=$rrd_dir/cpu_trend.rrd:sysload:AVERAGE",
              "AREA:mycpu#999999:5 Minute Average",
              "HRULE:1#FF3300:Threshold", );
  my $ERR=RRDs::error;
  die "ERROR while graphing $rrd: $ERR\n" if $ERR;

}

exit 0;
