#!/usr/bin/perl -w

# $Id: whitelist.cgi,v 1.37 2003/03/19 19:05:10 root Exp $

use strict;
use Rcs;
use POSIX qw(strftime);
use Cwd;

## cgi.pm parameters
use CGI;
use CGI::Carp qw(fatalsToBrowser carpout);
$CGI::DISABLE_UPLOADS = 1;
$CGI::POST_MAX = 1024;
my $path = $ENV{'PATH'};
$ENV{'PATH'} = '/usr/bin';
my $val = &createCGIHash;

## globals to be used in html
my ($domain, $images, $self) = &defineGlobals;

## define files to be edited
my $workdir   = '/etc/mail/spamassassin';
my $whitelist = 'whitelist.cf';
my $rcsdir    = "$workdir/RCS";

## create a layout
if ($val->{action}) {
  &validateInfo;
} elsif ($val->{directions}) {
  &showDirections;
} else {
  &showSubmit('0');
}

## subroutines ###############################

sub validateInfo {
  my $attempt = $val->{email};
  chomp $attempt;
  if ($attempt =~ /^[a-z0-9\.\-]+\@(?:[a-z0-9\-]+\.)?(?:[a-z0-9\-]+\.)?[a-z0-9\-]+\.[a-zA-Z]{2,6}$/) {
    &checkForExisting;
  } else {
    &showSubmit('format');
  }
}

sub checkForExisting {
  my %existing;

  open(FH,"$workdir/$whitelist")
    or die "Can't open whitelist!\n";
  
  while (my $i = <FH>) {
    next if $i =~ /^\#/;
    chomp $i;
    $i = (split(/\t/,$i))[-1]; 
    $existing{$i} = '1';
  }

  if ($existing{$val->{email}}) {
    &showSubmit('existing');
  } else {
    &addAddress;
  }
}

sub addAddress {
  ## set up local time format for RCS log entry
  my $time = strftime("Local Date: %Y/%m/%d\nLocal Time: %T",localtime);

  ## create message entry for rcs ci argument
  my $entry = qq|-mAddition: $val->{email}\nAdded by: $ENV{REMOTE_USER}\n$time|;

  ## create new rcs object
  my $rcs = Rcs->new;

  ## check out the whitelist
  $rcs->bindir('/usr/bin');
  $rcs->workdir($workdir);
  $rcs->rcsdir($rcsdir);
  $rcs->file($whitelist);
  $rcs->co('-l');

  ## add email to whitelist
  open(FH,">>$workdir/$whitelist");
  print FH "whitelist_from\t$val->{email}\n";
  close(FH);

  ## check the whitelist in
  $rcs->bindir('/usr/bin');
  $rcs->workdir($workdir);
  $rcs->rcsdir($rcsdir);
  $rcs->file($whitelist);
  $rcs->ci('-u', "$entry");

  $val->{email} = '';

  &showSubmit('success');
}

sub createCGIHash {
  my $query = new CGI;
  $query = CGI->new();
  my %formdata;
  my @formfields = $query->param;
  for my $field(@formfields) {
    $formdata{$field} = $query->param($field);
  }
  return \%formdata;
}

sub defineGlobals {
  my $domain = (split(/\//, cwd()))[-3];
  $domain =~ /^((?:[\w\-]+\.)?(?:[\w\-]+\.)(?:\w{2,3}\.)?(?:\w{2,4}))$/;
  $domain = $1 || 'UNKNOWN';

  my $images = "images";

  $0 = (split(/\//, $0))[-1];
  my $self = "$0";

  return ($domain, $images, $self);
}

sub htmlHeader {
print <<HTML;
Content-type: text/html\n\n
<html>
<head>
    <title>
      Spam Administration
    </title>
<SCRIPT LANGUAGE = "JavaScript"><!--
function startndnav(url) {
//alert (remoteWin);
        remoteWin = window.open(url,'ndnav','toolbar=0,top=10,left=25,directories=0,status=0,menubar=0,scrollbars=no,resizable=no,width=394,height=450');
     remoteWin.location.href = url;
        if (remoteWin.opener == null)
        remoteWin.opener = self;
        if (window.focus)
                remoteWin.focus();
     }

// -->
</SCRIPT>
</head>

<!-- BEGIN BODY DEFINES -->
  <BODY BGCOLOR="#99CC99" TEXT="black" LINK="#cc3300" ALINK="#669999" VLINK="#cc3300">
    <base href="https://www.$domain/my/">
HTML
}

sub htmlFooter {
print <<HTML
   </body>
</html>
HTML
}

sub showDirections {
&htmlHeader;
print <<HTML;
<table width="375" cellspacing="0" cellpadding="0" border="0">
 <tr>
  <td><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>Directions:</b><p>
You can add your the e-mail addresses of people that you know won't send you spam to a list of "trusted users" so that Spam Assassin won't tag them as offending e-mail.<p>
Simply type into the form the e-mail address that you would like to add to the list exactly as it appears in the message sent to you. Typically an e-mail address looks something like this: name\@domain.com<p>
After you have the address exactly as you would like it, click the submit button. If the e-mail address isn't already in the safe list, it will be immediately added and your friend's e-mail will arrive unchecked by Spam Assassin.
  </td>
 </tr>
</table><p>

<table width="375" cellspacing="0" cellpadding="0" border="0">
 <tr>
  <td align="right"><font face="verdana" size="1"><a href="$self"><b><< Back to Administration</b></a></font></td>
 </tr>
</table>
HTML
&htmlFooter;
}

sub showToggle {

}

sub showSubmit {
  my $routine = shift;

&htmlHeader;

print <<INTRODUCTION;
<!-- \$Id: whitelist.cgi,v 1.37 2003/03/19 19:05:10 root Exp $ -->
<table width="375" border="0" cellspacing="0" cellpadding="0">
 <tr>
  <td><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>Add a friend's e-mail to the list of Trusted Users.</b></font></td>
 </tr>
</table>
<p>
INTRODUCTION

## various errors or success message
my $start = '<b><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1" color="#cc3300">';
my $end = '</font></b><p>';
my $error = q|I'm sorry, but the e-mail address you've submitted does not appear to be in the correct format. Please try again.|;
my $duplicate = q|I'm sorry, but the e-mail address you've submitted appears to already be present in the list of Trusted Users.|;
my $success = q|Success! The e-mail address you've submitted has been added to the list of Trusted Users.|;

print "$start$error$end"
  if ($routine eq 'format');

print "$start$duplicate$end"
  if ($routine eq 'existing');

print "$start$success$end"
  if ($routine eq 'success');

print <<FORM;
<table width="375" cellspacing="0" cellpadding="0" border="0">
 <tr>
  <td valign="middle"><form method="post" action="$self">Trusted E-Mail:&nbsp;
  <input name="email" value="$val->{email}" maxlength="64"></td>
 </tr>
</table><p>

<table width="375" cellspacing="0" cellpadding="0" border="0">
 <tr>
  <td valign="middle" width="50%"><input type="hidden" name="action" value="on"></td>
  <td valign="middle" width="50%"><input type="image" value="Submit" border="0"
src="images/submitbutton.gif"></td>
 </tr>
</table><p>

<table width="375" cellspacing="0" cellpadding="0" border="0">
 <tr>
  <td valign="middle" width="50%"></td>
  <td valign="middle" width="50%"><b><font color="cc3300" face="verdana" size="1"><a href="$self?directions=1">directions</a> | <a href="javascript:window.close()">close window</b></font></a></td>
</table>
</form>
FORM

&htmlFooter;

}
