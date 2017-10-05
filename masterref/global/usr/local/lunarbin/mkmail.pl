#!/usr/bin/perl -w

# $Id: mkmail.pl,v 1.5 2003/05/07 10:47:12 root Exp $

use strict;
use Sys::Hostname;
use File::Copy;

#definitions and declarations
my $each;
my $inc = "/etc/mail/include";
my $vtmp = "/etc/mail/.virtusertable.tmp";
my $vbak = "/etc/mail/.virtusertable.bak";
my $atmp = "/etc/mail/.aliases.tmp";
my $abak = "/etc/mail/.aliases.bak";
my $vrun = "/etc/mail/virtusertable";
my $arun = "/etc/aliases";
my $equ = "equivalents";


############# EQUIVALENCIES ##############

## get our list of hosting domains
my @host_domains;
if (-d "/etc/hosting-options") {
  opendir(HOST_DIR, "/etc/hosting-options")
    or die "Cant open hosting-options directory\n";
  @host_domains = readdir HOST_DIR;
  closedir(HOST_DIR);
}

## check to see if there is an equivalencies file
if ($#host_domains > 0) {
  for my $client(@host_domains) {

    chomp $client;

    next if ( $client eq "." );
    next if ( $client eq ".." );

    if (-e "/etc/hosting-options/$client/equivalents") {

      ## stick the list of equivalents into an array
      open(EF, "/etc/hosting-options/$client/equivalents")
        or die "Problem with $client eqiv file\n\n";

      my @equiv = <EF>;

      close(EF);

      ## for each equivalent domain create a mirror of the production
      for my $equiv(@equiv) {

        chomp $equiv;

        ## open the current list of virtusers for master domain
        open(FH, "/etc/mail/include/virtuser/virt.$client")
          or die "virt.$client does not exist!\n\n";

        my @production = <FH>;

        close(FH);

        ## open the new mirror virtuser file
        open(MIRROR, ">/etc/mail/include/virtuser/virt.$equiv")
          or die "cant open the mirror file virt.$equiv";

    
        for my $i(@production) {

          $i =~ s/$client/$equiv/;

          print MIRROR $i;

        }

        close(MIRROR);

      }
    }
  }
}
      
#test to see if temp file exists. empty contents
if ( -e $atmp ) {
  unlink $atmp;
}

if ( -e $vtmp ) {
  unlink $vtmp;
}

#get list of include files
opendir VDH, "$inc/virtuser" or die "Cant open virtuser include directory $!\n";

my @vcontents = readdir VDH;

closedir VDH;

opendir ADH, "$inc/aliases" or die "Cant open aliases include directory $!\n";

my @acontents = readdir ADH;
 
closedir ADH;

if ($#acontents > 0) {
  #i sort the contents so that they will be alphabetically listed in
  #the final production file
  @acontents = sort @acontents;
  #change into the aliases include directory
  chdir "$inc/aliases"
    or die "Cant change to aliases include directory $!\n";
  #write contents of include files into the tmp aliases
  open AWF, ">>$atmp" or die "Cant open aliases temp file $!\n";
  for $each(@acontents) {
    next if ( $each eq "." );
    next if ( $each eq ".." );
    open FH, $each or die "Cant open aliases include file $!\n";
    print AWF "\#\#\# $each \#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\n";
    print AWF <FH>;
    close FH;
  }
  close AWF;
  #copy the production virtusertable file to backup
  rename $arun, $abak;
  #move the tmp file into production
  rename $atmp, $arun;
}

if ($#vcontents > 0) {
  #i sort the contents so that they will be alphabetically listed in
  #the final production file
  @vcontents = sort @vcontents;
  #change into the virtuser include directory
  chdir "$inc/virtuser" 
    or die "Cant change to virtuser include directory $!\n";
  #write contents of include files into the tmp virtusertable
  open VWF, ">>$vtmp" or die "Cant open virtuser temp file $!\n";
  for $each(@vcontents) {
    next if ( $each eq "." );
    next if ( $each eq ".." );
    open FH, $each or die "Cant open virtuser include file $!\n";
    print VWF "\#\#\# $each \#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\n";
    print VWF <FH>;
    close FH;
  }
  close VWF;
  #copy the production virtusertable file to backup
  rename $vrun, $vbak;
  #move the tmp file into production
  rename $vtmp, $vrun;
}

## stop sendmail
system("/etc/rc3.d/S80sendmail stop");

## build the new virtuser and access tables
copy("/etc/mail/include/access/global-config","/etc/mail/access")
  if (hostname() =~ /^host/);

if (hostname() !~ /^name2/) {
  my @sendmail_files = qw(virtusertable access);
  for my $i(@sendmail_files) {
    system(`makemap hash /etc/mail/$i < /etc/mail/$i`);
  }
  ## make the new aliases
  system("/usr/bin/newaliases");

  ## start sendmail
  system(`/usr/sbin/sendmail -bd -q15m`);
} else {
  system("/etc/rc3.d/S80sendmail start");
}
