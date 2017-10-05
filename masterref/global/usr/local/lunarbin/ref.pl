#!/usr/bin/perl -w

# $Id: ref.pl,v 1.2 2003/06/27 20:52:04 root Exp $

use strict;
use Getopt::Long;
use File::NCopy;

my $version;
my $panel;
my $cgibin;
my $help;
my $domain;
my $access;
my $bin;
my $webmail;
my $my;
my @webhost;

GetOptions (	
    		'version' 	=> \$version,
 		'panel' 	=> \$panel,
		'cgi-bin'	=> \$cgibin,
		'help' 		=> \$help,
		'domain=s'	=> \$domain,
		'access'	=> \$access,
		'bin'		=> \$bin,
		'webmail'	=> \$webmail,
		'my'		=> \$my,
	   );

my $rcs = (qw$Revision: 1.2 $)[-1];
my $dir = "/usr/local/ref/controlpanel";
my $www = "/www";
my $cgidir = "/usr/local/ref/cgi-bin";

chdir("$cgidir") 
  or die "Cant change directory to cgi-bin.\n";
my @cgi_bin = glob("*");
chdir("$dir") 
  or die "Cant change directory to the control panel.\n";
my @controlpanel = glob("*");

if ($domain) {
  push(@webhost, $domain);
} else {
  chdir("$www") 
    or die "Cant change directory to /www.\n";
  @webhost = glob("*");
}

if ($panel) {
  for my $i(@webhost) {
    unless (( -l "$www/$i")
           || ( $i eq "lost+found" )
           || ( $i eq "DEFUNCT" )
           || ( $i eq "TODAY")) {
      system("rm -rf $www/$i/controlpanel") 
        unless ( !-e "$www/$i/controlpanel" );
      system("cp -fRp $dir $www/$i");
      access("$i");
    }
  }
}

if ($cgibin) {
  for my $i(@webhost) {
    unless (( -l "$www/$i")
           || ( $i eq "lost+found" ) 
           || ( $i eq "DEFUNCT" ) 
           || ( $i eq "TODAY")) {
      system("cp -fRp /$cgidir/* $www/$i/cgi-bin/");
    }
  }
}

if ($access) {
  for my $i(@webhost) {
    unless (( -l "/www/$i" ) 
           || ( $i eq "lost+found" )) { 
      access($i);
    }
  }
}

if ($webmail) {
  for my $i (@webhost) {

    ## skip if the dir is a symlink
    next if ( -l "$www/$i" );

    ## skip the lost+found dir
    next if ( $i eq "lost+found" );

    ## remove the current webmail html directory
    system("rm -rf $www/$i/webmail/html")
      unless ( !-e "$www/$i/webmail/html");

    ## copy the new directory into place
    my $copy_file = File::NCopy->new (
          'recursive'     => 1,
          'preserve'      => 1,
          'force-write'   => 1,
    );

    $copy_file->copy("/ref/webmail/html","/www/$i/webmail");

    ## make the webmail config file domain specific
    my $substitute = "/usr/bin/perl -pi.orig -e";
    $substitute .= " 's/DOMAIN/$i/g'";
    
    my $conf = "/www/$i/webmail/html/w3mail.conf";
    my $login_file = "/www/$i/webmail/html/login.cgi";

    system("$substitute $conf");
    system("$substitute $login_file");

    symlink("/www/$i/webmail/html/login.cgi","/www/$i/webmail/html/index.cgi");

  }

}
   
if ($my) {

  for my $i(@webhost) {

    next if (-l "$www/$i");

    next if ($i eq "lost+found");

    system("rm -rf $www/$i/options/my")
      unless (!-e "$www/$i/options/my");

    system("cp -fRp /ref/options/my /www/$i/options");

    access("$i");

  }

} 
if ($bin) {

}

if ($help) {
  help();
}

if ($version) {
  print "\nThis is ref version $rcs\n\n";
}

sub help {
  print<<HELP;

NAME
	ref - copy tool for rcs controlled client web files.

SYNOPSIS
	Usage: ref [options]

DESCRIPTION
	Ref was written in order to allow administrators to copy 
  	updated versions of scripts, html and other files from a 
	single source repository to their respective locations within
	client directory structure for production purposes.
        The script automates the manual process which could prove
	tedious depending upon the number and files and clients.

COMMANDS
        --access
                generate a .htaccess file for the control panel directory
                struture of all hosting clients in /www

        --bin
                copy all scripts held within the control panel bin
                directory

        --cgi-bin
                place all rcs controlled files related to a client's
                public_html/cgi-bin/* into production.

        --domain <name>
                perform the copy of files strictly for the one domain
                listed as this flag's argument.
                the domain should be listed without hostname! e.g.

                  lunarhosting.net and not www.lunarhosting.net

	--help
		displays this menu

        --panel
                place all rcs controlled files related to client
                control panel into production for all clients having
                their root directories in /www/

VERSION
	This is ref version $rcs

HELP
}

sub access {
my $fqdn = shift;

my $fqdn_i = (split(/\./, $fqdn))[-2];
#my $fqdn_i = $fqdn;
#$fqdn_i =~ s/^(?:www\.)?((?:[\w\-]+\.)?(?:[\w\-]+))(?:\.\w{2,3})?(?:\w{2,4})$/$1/;

## create .htaccess for controlpanel
open(FH,">/www/$fqdn/controlpanel/.htaccess") or die "Cant open htaccess for $fqdn : $!\n";

print FH <<HTA;
AuthUserFile /www/$fqdn/options/passwd/adm-$fqdn
AuthName "Hosting Administration" 
AuthType Basic
require valid-user
HTA

close(FH);

## create .htaccess for webpublisher
open(FH, ">/www/$fqdn/webpublisher/.htaccess") or die "Cant open htaccess for webpub in $fqdn : $!\n";

print FH <<HTA;
AuthUserFile /www/$fqdn/options/passwd/adm-$fqdn
AuthName "Hosting Administration"
AuthType Basic
require valid-user
HTA

close(FH);

## create .htaccess for urchin
unless ($fqdn eq "lunarmedia.net") {
open(STATS,">/www/$fqdn/urchin/.htaccess")
  or die "Cant open htaccess for urchin in $fqdn : $!\n";

print STATS <<HTA;
AuthUserFile /www/$fqdn/options/passwd/pop-$fqdn
AuthName "Hosting Administration"
AuthType Basic
require valid-user
HTA

close(STATS);

}

## create .htaccess for my
open(MY,">/www/$fqdn/options/my/.htaccess")
  or die "Cant open htaccess for my in $fqdn : $!\n";

print MY <<HTA;
AuthUserFile /www/$fqdn/options/passwd/pop-$fqdn
AuthName "Configure Account"
AuthType Basic
require valid-user
HTA
close(MY);


}
