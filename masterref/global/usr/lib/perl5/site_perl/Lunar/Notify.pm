package Lunar::Hosts;

## $Id: Notify.pm,v 1.3 2003/08/12 15:55:46 root Exp $

use strict;
use warnings;
use Mail::Mailer;

BEGIN {
  use Exporter ();
  our ($VERSION, @ISA, @EXPORT, @EXPORT_OK, %EXPORT_TAGS);

  # set the version for version checking
  $VERSION     = 1.00;

  @ISA         = qw(Exporter);
  @EXPORT      = qw(
			&notifyAdmins
  );

  %EXPORT_TAGS = ( );

  @EXPORT_OK   = @EXPORT;

}

## Pages Lunarhosting Administrators
sub notifyAdmins {
  my $subject = shift;
  my $action  = shift;

  my $to;

  if ($action eq 'warn') {
    $to = 'warn-pager';
  } else {
    $to = 'emergency-pager';
  }

  my $mailer = Mail::Mailer->new();
  $mailer->open({
	To      => $to,
	Subject => "$subject",
	From    => 'alarm@lunarhosting.net',
  });
  $mailer->close;

}

1;
