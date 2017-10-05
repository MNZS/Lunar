package Lunar::Hosts;

## $Id: Hosts.pm,v 1.5 2003/08/13 18:07:16 root Exp $

use strict;
use warnings;

BEGIN {
  use Exporter ();
  our ($VERSION, @ISA, @EXPORT, @EXPORT_OK, %EXPORT_TAGS);

  # set the version for version checking
  $VERSION     = 1.00;

  @ISA         = qw(Exporter);
  @EXPORT      = qw(
			&getHosts 
  );

  %EXPORT_TAGS = ( );

  @EXPORT_OK   = @EXPORT;

}

## Returns a list of Lunar Hosting nodes as well as their attributes
sub getHosts {
  my $subset = shift;

  my $server 		= 'servers';
  my $cisco  		= 'routers';
  my $snmpServer 	= 'Wl7d0w%!';
  my $snmpCisco 	= 'monitor';

  my %servers = (
    	host1 => {
		hardware 	=> $server,
		community 	=> $snmpServer,
		os		=> '7.3',
	},

	host2 => {
		hardware 	=> $server,
		community 	=> $snmpServer,
		os		=> '7.3',
	},
	
	name1 => {
		hardware 	=> $server,
		community 	=> $snmpServer,
		os		=> '7.3',
	},
	
	name2 => {
		hardware 	=> $server,
		community 	=> $snmpServer,
		os		=> '8.0',
	},
  );

  my %cisco = (
	gateway => {
		hardware	=> $cisco,
		community	=> $snmpCisco,
	},

	backbone => {
		hardware	=> $cisco,
		community	=> $snmpCisco,
	}
  ); 

  if ($subset =~ /linux|server|redhat/i) {
    return %servers;
  } elsif ($subset =~ /router|switch|cisco/i) {
    return %cisco;
  } else {
    return (%servers, %cisco);
  }
}

1;
