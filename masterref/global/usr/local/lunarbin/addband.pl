#!/usr/bin/perl -w

# $Id: addband.pl,v 1.1 2003/04/02 19:08:41 root Exp $

use strict;
use Getopt::Long;
use Mail::Mailer;
use DBI;
use Sys::Hostname;

# Only run on hosting servers
if (hostname() !~ /^host/) {
  exit 1;
}

## print options
my $summary;
my $print;
my $domain;

GetOptions (
                'summary'	=> \$summary,
		'print'		=> \$print,
		'domain=s'	=> \$domain,
           );


my %monthly;

## mysql options
my $username = "";
my $password = "";
my $hostname = hostname();
my $table = "";

## get list of domains to act upon
my @domainlist = ();

if ($domain) {
  chomp $domain;

  push @domainlist, $domain;

} else {

  ## move to www directory
  chdir("/www")
    or die "Cant change to hosting directory : $!\n";
  
  @domainlist = glob("*");

}

for my $domain(@domainlist) {

  chomp $domain;

  ## test for hidden directories
  next if ($domain eq ".");
  next if ($domain eq "..");

  ## test for symlink
  next if ( -l "/www/$domain" );

  ## skip northgate
  next if ($domain eq "northgateamusement.org");

  ## test to ensure that directory is of the correct name structure
  next unless ($domain =~ /^(?:[\w\-]+\.)?(?:[\w\-])+\.\w{2,3}$/);

  ## if there is no current bandwidth, set to 0
  my $current = "0";

  ## if client uses urchin
  if (-e "/etc/hosting-options/$domain/urchin") {

    ## if there is a current bandwidth value
    if (-e "/etc/hosting-options/$domain/bandwidth") {

      ## open the current bandwidth total
      open(FH, "/etc/hosting-options/$domain/bandwidth")
        or warn "Cant reading current bandwidth value for $domain : $!\n";

      ## put total into variable
      $current = <FH>;

      chomp $current;
 
      ## close the current bandwidth total file
      close(FH);

    ## endif
    }

  ## endif
  }

  ## test for if log file exists
  if (-e "/var/log/www/www-xfer.$domain") {

    ## open the current logfile
    open(FH, "/var/log/www/www-xfer.$domain")
      or warn "Cant open logfile for $domain : $!\n";

    ## total the day's traffic
    my $usage;
    while(<FH>) {
    
      ## skip hacker probes
      next if (/cmd\.exe/);

      ## skip if field is not a number
      next if ((split(/ /, $_))[9] !~ /^\d+$/);

      ## increment day's usage by the field
      $usage += (split(/ /, $_))[9];

    ## end while
    }
  
    ## add the current total and the day's usage
    my $newtotal = $current + $usage;
   
    ## if monthly summary...
    if ($summary) {

      ## put newtotal into hash for the month
      #$monthly{$domain} = $newtotal;

      ##wipe clean the current total file
      open(FH, ">/etc/hosting-options/$domain/bandwidth")
        or warn "Cant wipe out bandwidth file for monthly summary for $domain : $!\n";

      print FH "0";

      close(FH);

    ## if just printing to stdout
    } elsif ($print) {
      print "$domain -> $newtotal\n";

    ## if not the monthly summary...
    } else {
      ## put the new total into the domain's flat file
      open(FH, ">/etc/hosting-options/$domain/bandwidth")
        or warn "Cant open bandwidth file for $domain for writing : $!\n";

      print FH $newtotal;

      close(FH);

    ## endif
    }

  ## end if
  }

## end for
}

## if montly summary, send out the email
#&total if ($summary);

## subroutines

sub total {

my $from_address = 'hosting@lunarmedia.net';
my $to_address = 'hosting@lunarmedia.net';
my $subject = "Monthly Usage Totals for hosting customers";

  my $mailer = Mail::Mailer->new();
  $mailer->open({ From    => $from_address,
                  To      => $to_address,
                  Subject => $subject,
               });

  #print $mailer "\nThe grand monthly total thus far is: $total\n\n";

  print $mailer "In order from highest usage to lowest:\n\n";

  my %rev_monthly = reverse %monthly;

  for my $i(sort {$b<=>$a} keys %rev_monthly) {
    print $mailer "$rev_monthly{$i} : $i\n";
  }

  $mailer->close();
}

