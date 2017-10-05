#!/usr/bin/perl -w

use strict;
use Mail::Mailer;

# $Id: billing.pl,v 1.7 2003/09/17 14:44:49 root Exp $

## for new clients, be sure to add their relevent hash
## and then add it to the list of resellers

my %dhot = (
		total => "0",
		name  => "Donna's House of Type",
		id    => "dhot",
		disc  => ".14",
);

my %lunarmedia = (
		total => "0",
		name  => "Lunar Media Inc.",
		id    => "lunarmedia",
		disc  => ".11",
);

my %ilbbs = (
                total => "0",
                name  => "Interlink-BBS",
                id    => "ilbbs",
                disc  => ".14",
);

my %lunarhosting = (
		total => "0",
		name  => "Lunar Hosting",
		id    => "lunarhosting",
		disc  => "1",
);

my %carlberg = (
		total => "0",
		name  => "Carlberg Graphics",
		id    => "carlberg",
		disc  => "1",
);

my @resellers = (\%dhot, \%lunarmedia, \%lunarhosting, \%ilbbs, \%carlberg);

###################################################################
###################################################################

##############    NO MORE EDITING IS REQUIRED    ##################

###################################################################
###################################################################

my %plan = (             #  bandwidth     disk         price
                bronze => ["7000000000",  "175000000",  "35", ],
                silver => ["10000000000", "300000000", "50", ],
                gold   => ["15000000000", "600000000", "75", ],
);


opendir(DIR,"/etc/hosting-options")
  or die "can't open hosting-options\n";

my @domains = readdir(DIR);

for my $i(sort @domains) {

  next if ($i eq "..");
  next if ($i eq ".");

  next if ($i eq "lunarhosting.net");
  next if ($i eq "northgateamusement.org");

  next if (-e "/etc/hosting-options/$i/free");

  open(DISK,"/etc/hosting-options/$i/disk") 
    or warn "Can't open disk for $i : $!\n";

  my $disk = <DISK>;
  $disk =~ s/^(\d+)\s+\/.*$/$1/g;
  chomp $disk;
 
  close(DISK);

  open(BAND,"/etc/hosting-options/$i/bandwidth")
    or warn "Cant open bandwidth file for $i : $!\n";

  my $band = <BAND>;
  chomp $band;

  close(BAND);

  ## determine the plan they are on
  my $plan;

  if (($band > $plan{silver}[0]) || ( $disk > $plan{silver}[1])) {

    $plan = "gold";

  } elsif (($band > $plan{bronze}[0]) || ( $disk > $plan{bronze}[1])) {

    $plan = "silver";

  } else {

    $plan = "bronze";

  }

  ## place the domain into a hash with pricing
  if ( -e "/etc/hosting-options/$i/dhot" ) {

    $dhot{$i} = [$disk, $band, $plan, $plan{$plan}[2],];
    $dhot{total} = $dhot{total} + $plan{$plan}[2]
      unless ( $i =~ /^dhot.com$/ );

  } elsif ( -e "/etc/hosting-options/$i/lunarmedia" ) {

    $lunarmedia{$i} = [$disk, $band, $plan, $plan{$plan}[2],];
    $lunarmedia{total} = $lunarmedia{total} + $plan{$plan}[2]
      unless ( $i =~ /^lunarmedia.net$/ );

  } elsif ( -e "/etc/hosting-options/$i/ilbbs" ) {
                                                                                
    $ilbbs{$i} = [$disk, $band, $plan, $plan{$plan}[2],];
    $ilbbs{total} = $ilbbs{total} + $plan{$plan}[2]
      unless ( $i =~ /^ilbbs.com$/ );

  } elsif ( -e "/etc/hosting-options/$i/carlberg" ) {

    $carlberg{$i} = [$disk, $band, $plan, $plan{$plan}[2],];
    $carlberg{total} = $ilbbs{total} + $plan{$plan}[2];

  } else {

    $lunarhosting{$i} = [$disk, $band, $plan, $plan{$plan}[2],];
    $lunarhosting{total} = $lunarhosting{total} + $plan{$plan}[2]
      unless ( $i =~ /^lunarhosting.net$/ );

  }

}

for my $reseller(@resellers) {

  my $mailer = Mail::Mailer->new();

  $mailer->open({  	From	=> 'billing@lunarhosting.net',
			To	=> "invoice-$$reseller{id}\@lunarhosting.net",
			Subject => "Monthly Invoice from Lunar Hosting"
		  });

  print $mailer uc($$reseller{name}) . "\n\n";

  for my $domain(sort keys %$reseller) {

    next if ($domain eq "total");
    next if ($domain eq "name");
    next if ($domain eq "id");
    next if ($domain eq "disc");

    ## pretty up the disk usage
    my $disk_suffix;

    my $disk_length = length $$reseller{$domain}[0];

    if ( $disk_length < 4 ) {

      $disk_suffix = "Bytes";

    } elsif ( $disk_length < 7 ) {

      $disk_suffix = "KBytes";
      $$reseller{$domain}[0] = reverse $$reseller{$domain}[0];
      $$reseller{$domain}[0] =~ s/\d{3}(\d+)/$1/g;
      $$reseller{$domain}[0] = reverse $$reseller{$domain}[0];

    } elsif ( $disk_length < 10 ) {

      $disk_suffix = "MBytes";
      $$reseller{$domain}[0] = reverse $$reseller{$domain}[0];
      $$reseller{$domain}[0] =~ s/\d{6}(\d+)/$1/g;
      $$reseller{$domain}[0] = reverse $$reseller{$domain}[0];

    } else {

      $disk_suffix = "GBytes";
      $$reseller{$domain}[0] = reverse $$reseller{$domain}[0];
      $$reseller{$domain}[0] =~ s/\d{9}(\d+)/$1/g;
      $$reseller{$domain}[0] = reverse $$reseller{$domain}[0];

    }

    ## pretty up the bandwidth usage
    my $band_suffix;

    my $band_length = length $$reseller{$domain}[1];

    if ( $band_length < 4 ) {

      $band_suffix = "Bytes";

    } elsif ( $band_length < 7 ) {

      $band_suffix = "KBytes";
      $$reseller{$domain}[1] = reverse $$reseller{$domain}[1];
      $$reseller{$domain}[1] =~ s/\d{3}(\d+)/$1/g;
      $$reseller{$domain}[1] = reverse $$reseller{$domain}[1];

    } elsif ( $band_length < 10 ) {

      $band_suffix = "MBytes";
      $$reseller{$domain}[1] = reverse $$reseller{$domain}[1];
      $$reseller{$domain}[1] =~ s/\d{6}(\d+)/$1/g;
      $$reseller{$domain}[1] = reverse $$reseller{$domain}[1];

    } else {

      $band_suffix = "GBytes";
      $$reseller{$domain}[1] = reverse $$reseller{$domain}[1];
      $$reseller{$domain}[1] =~ s/\d{9}(\d+)/$1/g;
      $$reseller{$domain}[1] = reverse $$reseller{$domain}[1];

    }

    if ($domain =~ /^$$reseller{id}\.\w{2,3}/) {

      print $mailer uc($domain) . "\n";
      print $mailer "DISK: $$reseller{$domain}[0] $disk_suffix\n";
      print $mailer "BAND: $$reseller{$domain}[1] $band_suffix\n";
      print $mailer "PLAN: No Charge\n";
      print $mailer "\n";

      next;

    }

    print $mailer uc($domain) . "\n";
    print $mailer "DISK: $$reseller{$domain}[0] $disk_suffix\n";
    print $mailer "BAND: $$reseller{$domain}[1] $band_suffix\n";
    print $mailer "PLAN: $$reseller{$domain}[2]\t\t\t\t(\$$$reseller{$domain}[3].00)\n";
    print $mailer "\n";


  }

    print $mailer "Total(Prior to Discount):\t\t\$$$reseller{total}\n";
    print $mailer "Total(After Discount):\t\t\t\$" . ($$reseller{total} * $$reseller{disc}) . "\n\n";

  $mailer->close;

}
