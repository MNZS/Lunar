#!/usr/bin/perl -w

# $Id: snmpDiskUsage.pl,v 1.7 2003/08/12 15:56:31 root Exp $

use strict;
use Net::SNMP;
use POSIX qw(strftime);
use Lunar::Hosts;
#use Lunar::Notify;
use Lunar::Restrict;

# Poll a remote server for a list of disk partitions and the amount
# of space used. If a partition is over a set threshold, page the
# appropriate administrator

&limitHost('^name');

my %nodes = &getHosts('linux');

my %snmpMIB = (
	type	=> '.1.3.6.1.2.1.25.2.3.1.2',
	desc	=> '.1.3.6.1.2.1.25.2.3.1.3',
	unit	=> '.1.3.6.1.2.1.25.2.3.1.4',
	size	=> '.1.3.6.1.2.1.25.2.3.1.5',
	used	=> '.1.3.6.1.2.1.25.2.3.1.6',
);

my %diskTable;

for my $node(keys %nodes) {
  my $index = 1;
  while($index) {
    ## Find our path statement
    my $snmp = Net::SNMP->session(
	-hostname	=> $node,
	-version	=> 1,
	-community	=> $nodes{$node}{'community'}, );
    my $mib = $snmpMIB{desc} . ".$index";
    my $query =  $snmp->get_request( -varbindlist => [$mib] );
    if ($snmp->error) {
      undef $index;
      next;
    }
    my $desc = $query->{$mib};
    $snmp->close;
    if ($desc) {
      $diskTable{$node}{$index}{'path'} = $desc;
      &getUnit($node,$index);
      &getSize($node,$index);
      &getUsed($node,$index);
      &getPrct($node,$index);
      $index++;
    } else {
      exit;
    }
  }
  &genHTML($node);
}

####

sub getImage {
  my $percent = shift;
  my $image;
  if ($percent > 79) {
    $image = 'alarm.jpg';
  } elsif ($percent > 64) {
    $image = 'warn.jpg';
  } else {
    $image = 'safe.jpg';
  }
  $image = '<img src="images/' . $image . '">';
  return $image;
}

sub genHTML {
  my $node = shift;
  open (HTML,">/usr/local/mrtg/$node.disk.html")
    or die "Can't open HTML doc for writing : $!\n"; 
  print HTML "<html>\n";
  print HTML "  <head>\n";
  print HTML "    <title>Disk Utilization</title>\n";
  print HTML "    <body>\n";
  my $time = strftime("%X %D",localtime); 
  print HTML uc($node) . ".LUNARHOSTING.NET<br>Last updated: $time<p>\n";
  for my $j(keys %{$diskTable{$node}}) {
    my $image = &getImage($diskTable{$node}{$j}{'prct'});
    print HTML "&nbsp;&nbsp;PATH: $diskTable{$node}{$j}{'path'} ";
    print HTML "($diskTable{$node}{$j}{'prct'}% utilized)&nbsp;$image<br>\n";
    print HTML "&nbsp;&nbsp;USED/CAPACITY: $diskTable{$node}{$j}{'used'}/$diskTable{$node}{$j}{'size'}<br>\n";
    print HTML "<p>";
  }
  print HTML "  </body>\n</html>";
}

sub getUnit {
  my $node = shift;
  my $index = shift;
  my $snmp = Net::SNMP->session(
	-hostname       => $node,
	-version        => 1,
	-community      => $nodes{$node}{'community'}, );
  my $mib = $snmpMIB{unit} . ".$index";
  my $query =  $snmp->get_request( -varbindlist => [$mib] );
  my $result = $query->{$mib};
  $result = substr($result,0,1); 
  $diskTable{$node}{$index}{'unit'} = $result;

}

sub getSize {
  my $node = shift;
  my $index = shift;
  my $snmp = Net::SNMP->session(
        -hostname       => $node,
        -version        => 1,
        -community      => $nodes{$node}{'community'}, );
  my $mib = $snmpMIB{size} . ".$index";
  my $query =  $snmp->get_request( -varbindlist => [$mib] );
  my $result = $query->{$mib};
  $diskTable{$node}{$index}{'size'} = $result * $diskTable{$node}{$index}{'unit'};
}

sub getUsed {
  my $node = shift;
  my $index = shift;
  my $snmp = Net::SNMP->session(
        -hostname       => $node,
        -version        => 1,
        -community      => $nodes{$node}{'community'}, );
  my $mib = $snmpMIB{used} . ".$index";
  my $query =  $snmp->get_request( -varbindlist => [$mib] );
  my $result = $query->{$mib};
  $diskTable{$node}{$index}{'used'} = $result * $diskTable{$node}{$index}{'unit'};
}

sub getPrct {
  my $node = shift;
  my $index = shift;
  if ( ($diskTable{$node}{$index}{'used'} == 0) ||
       ($diskTable{$node}{$index}{'size'} == 0) ) {
    $diskTable{$node}{$index}{'prct'} = 0;
  } else {
    $diskTable{$node}{$index}{'prct'} = $diskTable{$node}{$index}{'used'} / $diskTable{$node}{$index}{'size'};
    if ($diskTable{$node}{$index}{'prct'} =~ /^0\.\d+/) {
      $diskTable{$node}{$index}{'prct'} =~ /^0\.(\d{2}).+$/;
      $diskTable{$node}{$index}{'prct'} = $1;
      $diskTable{$node}{$index}{'prct'} = 0
        if $1 == '00';
    } elsif ($diskTable{$node}{$index}{'prct'} =~ /^1/) {
      $diskTable{$node}{$index}{'prct'} = '100';
    }
  }
}
