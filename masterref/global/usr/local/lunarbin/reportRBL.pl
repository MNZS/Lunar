#!/usr/bin/perl -w

use strict;
use RRDs;
use Sys::Hostname;
use Date::Manip;
use POSIX qw(strftime);

if (hostname() ne 'name2.lunarhosting.net') {
  exit 1;
}

my @nodes = qw(	host1 host2 );

my $rrd = 'rblReport.rrd';
my $mrtgDir = '/usr/local/mrtg/servers';
                                                                                
my $end = time();
                                                                                
my $targetDate =  &ParseDateDelta("1 day ago");
$targetDate = &UnixDate("$targetDate","%b %e");
                                                                                
for my $node(@nodes) {

  my %rbl = (	
     	  # 'listname as it appears in maillog' => {
  	  #	'placeholder for tally' => '0',
  	  #	'color for graph line' = '',
  	  #	}, 
  	  'dsbl' => {
	  	  'count' => '0',
		  'color' => '',
		  'id' => 'list.dsbl.org',
		  },
	  'multihop' => {
		  'count' => '0',
		  'color' => '',
		  'id' => 'multihop.dsbl.org',
		  },
	  'spamcop' => {
		  'count' => '0',
		  'color' => '',
		  'id' => 'bl.spamcop.net',
		  },
	  'spamhaus' => {
	  	  'count' => '0',
		  'color' => '',
		  'id' => 'sbl.spamhaus.org',
		  },
	  'ordb' => {
		  'count' => '0',
		  'color' => '',
		  'id' => 'relays.ordb.org',
		  },
	  'monkey' => {
		  'count' => '0',
		  'color' => '',
		  'id' => 'proxies.relays.monkeys.com',
		  },
  );

  my $rrd_dir = "$mrtgDir/$node/mail";
  my $img_dir = $rrd_dir;

  &test_if_complete($rrd_dir);

  my $scp = `which scp`; chomp $scp;
  $scp .= " $node:";
  $scp .= '/var/log/maillog ';
  $scp .= "/tmp/$node.maillog";

  system("$scp");

  open(LOG,"/tmp/$node.maillog")
    or die "Can't open $node.maillog : $!\n";
  while(my $line = <LOG>) {
    chomp $line;
    for my $rbl(keys %rbl) {
      next unless ($line =~ /^$targetDate/);
      if ($line =~ /$rbl{$rbl}{id}$/) {
        $rbl{$rbl}{count} = $rbl{$rbl}{count} + 1;
      }
    }
  }
  close(LOG);

  unlink("/tmp/$node.maillog") if (-e "/tmp/$node.maillog");
                                                                                
  &update_rrd($rrd_dir,\%rbl);
  &logStats($node,\%rbl);
  &make_graph('7',$node,$rrd_dir);
  &make_graph('28',$node,$rrd_dir);
}

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
                                                                                
return 1;

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
                                                                                
return 1;

} elsif ( ! -e "$dir/$rrd" ) {
                                                                                
print <<CREATE;
                                                                                
Hang on, your RRD database is being created!
This will only need to be done once, so you
shouldn't see this messsage again.
                                                                                
CREATE

RRDs::create("$dir/$rrd",
             "DS:spamcop:GAUGE:172800:U:U",
             "DS:spamhaus:GAUGE:172800:U:U",
             "DS:ordb:GAUGE:172800:U:U",
             "DS:dsbl:GAUGE:172800:U:U",
             "DS:multihop:GAUGE:172800:U:U",
             "RRA:AVERAGE:0.5:1:5000" );
             #"RRA:AVERAGE:0.5:1:365" );
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
                                                                                
0 6 * * *     /path/to/this/script >/dev/null 2>&1
                                                                                
DONE
                                                                                
return 1;
                                                                                
}
                                                                                
## end of subroutine
}

sub update_rrd {
                                                                                
  my $dir = shift;
  my $rbl = shift;

  RRDs::update("$dir/$rrd","N:$rbl->{'spamcop'}{'count'}:$rbl->{'spamhaus'}{'count'}:$rbl->{'ordb'}{'count'}:$rbl->{'dsbl'}{'count'}:$rbl->{'multihop'}{'count'}");
  my $ERR=RRDs::error;
  die "ERROR while updating $rrd: $ERR\n" if $ERR;
}

sub make_graph {
                                                                                
  my $interval = shift;
  my $hostname = shift;
  my $dir = shift;
  
  # 86400 = number of seconds in a day
  my $range = $interval * 86400;                                                                              
  my $start = $end - $range;

  RRDs::graph("$dir/spam-$interval.gif",
              "--start","$start",
              "--end","$end",
              "--title","Blacklist report for $hostname over $interval days",
              "--vertical-label","Messages Blocked",
         #     "-x","MINUTE:60:HOUR:$print_hour:HOUR:$print_hour:0:%k",
              "-l","0",
              "--units-exponent","0",
              "DEF:spamhaus=$dir/rblReport.rrd:spamhaus:AVERAGE",
              "DEF:spamcop=$dir/rblReport.rrd:spamcop:AVERAGE",
              "DEF:dsbl=$dir/rblReport.rrd:dsbl:AVERAGE",
              "DEF:ordb=$dir/rblReport.rrd:ordb:AVERAGE",
              "DEF:multihop=$dir/rblReport.rrd:multihop:AVERAGE",
              "LINE1:spamhaus#FF0000:sbl.spamhaus.org", 
              "LINE1:spamcop#00FF00:bl.spamcop.net", 
              "LINE1:dsbl#0000FF:list.dsbl.org", 
              "LINE1:ordb#000000:relays.ordb.org", 
              "LINE1:ordb#FFFF00:multihop.dsbl.org", 
  );

  my $ERR=RRDs::error;
  die "ERROR while graphing $rrd: $ERR\n" if $ERR;
                                                                                
}

sub showReport {
  my $node = shift;
  my $rbl = shift;

  print "RBL Statistics for $node\n";
  for my $i(keys %{$rbl}) {
    print "\t$rbl->{$i}{id} -> $rbl->{$i}{count}\n";
  }
  print "\n";
}                                                                                
sub logStats {
  my $node = shift;
  my $rbl = shift;

  open(LOG,'>>/var/log/rbl.log');
  print LOG strftime("%b %d",localtime);
  print LOG " - $node\n";
  for my $i (keys %{$rbl}) {
    print LOG "  $rbl->{$i}{id}($rbl->{$i}{count})\n";
  }
  print "\n";
  close(LOG);
}
exit 0;

