#!/usr/bin/perl -w

use strict;
use Sys::Hostname;

# MasterRef
# $Id: urchin_mkconfig.pl,v 1.9 2003/05/12 22:47:15 root Exp $

# script used to create an Urchin config file based on the contents
# of include files for various hosted domains. the include files can
# be manually configured by clients on a per domain basis

if (hostname() !~ /^host/) {
  exit 1;
}

## global variables
my $opt = "/etc/hosting-options";
my $dir = "/usr/local/urchin";
my $cfg = "$dir/config";
my $inc = "/include";

## get list of options
chdir $opt
  or die "Cant change directory to options dir : $!\n";
my @options = glob("*")
  or die "Cant read options directory : $!\n";

## per server license
my %license = ( 
		'host1.lunarhosting.net' => 'EFFPM-8MVXT-FAU5A-4TBKK',
		'host2.lunarhosting.net' => 'VFHH4-7VF4E-3J8S9-K1B4E',
);

my %serial = ( 	
  		'host1.lunarhosting.net' => '1337-3337-7462-6218',
	 	'host2.lunarhosting.net' => '7733-1737-1836-6218',
);

## place hostname into variable
my $hostname = hostname();

## open the urchin config file
open(FH, ">$cfg")
  or die "Cant open the Urchin config file : $!\n";

## print out global configs
print FH <<CFG;
#=======================================================================
#                  Urchin Dedicated 3 Config File
#=======================================================================

## licensing
#U3-DED A8ZB-RZWV-BG4E-1616
SerialNumber:	$serial{$hostname}
LicenseCode:	$license{$hostname}

## global configuration
ProcessEcommerce:       off
ProcessDNS:             on
ProcessBrowsers:        on
ResolverIP:             208.16.140.132
Visitor_Timeout:        86400
RestartCommand:         /usr/local/apache/bin/apachectl graceful
#SystemReport:          on
#SystemDirectory:    /www/systemreport/

#=======================================================================

CFG

## print urchin configurations per client 
for my $i (@options) {
  next if ($i eq ".");
  next if ($i eq "..");
  if (-e "$i/urchin") {

print FH <<CFG;
## $i
<Report>
  ReportName:\t\t$i 
  ReportDomains:\t$i, www.$i
  ReportDirectory:\t/www/$i/urchin/
  FilterOut:\t\tdefault\\.ida|\\.exe|robots\\.txt|favicon\\.ico|\\.cfm
  LogDestiny:\t\tarchive	
  #LogDestiny:\t\tdont touch
  TransferFormat:\tcombined
  TransferLog:\t\t/var/log/www/www-xfer.$i
  TransferFormat:\tcombined
  TransferLog:\t\t/var/log/www/www-error.$i
CFG

  ## add miva processing if applicable
  if (-e "/www/$i/pub/mivadata/elf.log") {
    print FH "  ProcessEcommerce:\ton\n";
    print FH "  TransferFormat:\telf\n";
    print FH "  TransferLog:\t/www/$i/pub/mivadata/elf.log\n";
  }

print FH "</Report>\n\n";

  }
}
