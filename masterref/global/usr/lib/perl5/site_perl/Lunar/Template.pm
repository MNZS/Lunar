#package Lunar::PackageName;

## $Id: Template.pm,v 1.2 2003/08/11 05:26:32 root Exp $

use strict;
use warnings;

BEGIN {
  use Exporter ();
  our ($VERSION, @ISA, @EXPORT, @EXPORT_OK, %EXPORT_TAGS);

  # set the version for version checking
  $VERSION     = 1.00;

  @ISA         = qw(Exporter);
  @EXPORT      = qw(
			#&subroutineName
  );

  %EXPORT_TAGS = ( );

  @EXPORT_OK   = @EXPORT;

}

## add subroutine here



## needed for module completion
1; 
