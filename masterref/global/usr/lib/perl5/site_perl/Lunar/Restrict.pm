package Lunar::Restrict;

## $Id: Restrict.pm,v 1.4 2003/08/11 05:47:37 root Exp $

use strict;
use warnings;
use Sys::Hostname;

BEGIN {
  use Exporter ();
  our ($VERSION, @ISA, @EXPORT, @EXPORT_OK, %EXPORT_TAGS);

  # set the version for version checking
  $VERSION     = 1.00;

  @ISA         = qw(Exporter);
  @EXPORT      = qw(
			&limitHost
  );

  %EXPORT_TAGS = ( );

  @EXPORT_OK   = @EXPORT;

}

##
sub limitHost {
  my $regex = shift;

  if (hostname() !~ /$regex/) {
    exit 1;
  }
}

## needed for module completion
1; 
