#!/usr/bin/perl -w

## $Id: password.cgi,v 1.2 2003/04/10 18:16:48 root Exp $

## modules
use strict;
use Authen::PAM;
use Passwd::Linux qw(modpwinfo mgetpwnam);
use Crypt::PasswdMD5;
use POSIX qw(strftime);
use Cwd;
use String::Random;

## taint environmentals
delete @ENV{qw(IFS CDPATH ENV BASH_ENV)};
$ENV{'PATH'} = "/bin";

## cgi.pm
use CGI;
use CGI::Carp qw(fatalsToBrowser carpout);
$CGI::DISABLE_UPLOADS = 1;
$CGI::POST_MAX = 1024;
my $query = new CGI;
$query = CGI->new();

my %formdata;
my @formfields = $query->param;

for my $field(@formfields) {
  $formdata{$field} = $query->param($field);
}

## script variables
my $domain = (split(/\//, cwd()))[-3];
my $rcs = (qw$Revision: 1.2 $)[-1];
my $images = "controlpanel/images";

$0 = (split(/\//, $0))[-1];
my $self = "controlpanel/$0";

## html
print <<STARTHTML;
Content-type: text/html\n\n
<HTML>
  <HEAD>

  <TITLE>Password Management</TITLE>

    <SCRIPT LANGUAGE="JavaScript">
    <!--
    window.onerror = null;

    function targetwindow(url) {
     var root;
      if (parent.opener.closed) {
        root=window.open('','opener','toolbar=yes,location=yes,status=yes,menubar=yes,scrollbars=yes,resizable=yes,copyhistory=no');
        root.location.href = url;
    
      } else { 
        parent.opener.top.location.href = url;
      }
    }

    function done() {
      window.close()
    }
    // -->

    </SCRIPT>

  </HEAD>


<BODY BGCOLOR="#99CC99" TEXT="black" LINK="#cc3300" ALINK="#669999" VLINK="#cc3300">
STARTHTML

## create the body 
if ($formdata{instructions}) {
  &content('instructions');

} elsif ($formdata{click}) {
  &check_pass();

} else {
  &content('none');

}

## end html
print <<ENDHTML;
    <p>
  </BODY>
</HTML>
ENDHTML

## subroutines

## generate content of page
sub content {

  ## find out if new flags should be used
  my $routine = shift;

  ## successful change of password 
  if ($routine eq "success") {

print <<SUCCESS;
<table width="375" cellspacing="0" cellpadding="0" border="0">
 <tr>
  <td><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>Your password has been changed!</b><p>Although your password has been updated on the system, it may take up to 10 minutes for it to propogate to all services offered by Lunar Media.<p>We recommend that you log out of your control panel and then log back in to ensure that the change has been accepted. If you are unable to access  services using your new passphrase, please <a href= "mailto: support\@lunarhosting.net">e-mail</a> support.</font><p></td>
 </tr>
 <tr>
  <td align="left"><font color="cc3300" face="verdana" size="1"><b><a href="javascript:window.close()">close window</b></font></a></td>
 </tr>
</table>
SUCCESS

  ## error processing
  } elsif ($routine eq "instructions") {

print <<INSTRUCTIONS;
<table width="375" cellspacing="0" cellpadding="0" border="0">
 <tr>
  <td><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>Directions:</b><p>
If you know your current password, you can use this form to change it to something new. Its recommended that you change your password once every few months to further limit any attempts by hackers to guess your current passphrase.<br>Your password should be between 6 and 8 characters long and should make use of both upper and lowercase letters and should try to include at least one number.
</font>
  </td>
 </tr>
</table><p>

<table width="375" cellspacing="0" cellpadding="0" border="0">
 <tr>
  <td><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1">&nbsp;<b>1. Enter your current password.<p>&nbsp;2. Enter your desired new password.<p>&nbsp;3. Repeat this new password.<p>&nbsp;4. Click Submit.</b><p><b>Note:</b> Passwords will not be visible. Stars will appear in place of characters. All changes are immediate. If you have problems with your account please <a href="mailto:support\@lunarhosting.net">e-mail</a> support.</font>
  </td>
 </tr>
</table><p>

<table width="375" cellspacing="0" cellpadding="0" border="0">
 <tr>
  <td align="right"><font face="verdana" size="1"><a href="https://www.$domain/$self"><b>Back to Password Change</b></a></font></td>
 </tr>
</table>
INSTRUCTIONS

  ## error processing
  } else {

print <<INTRODUCTION;
<table width="375" border="0" cellspacing="0" cellpadding="0">
 <tr>
  <td><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>Use this form to change your current password.</b></font></td>
 </tr>
</table>
<p>
INTRODUCTION

print qq|<b><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1" color="#cc3300">It does not appear that your new passwords match!</font></b><p>|
  if ($routine eq "no_match");

print qq|<b><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1" color="#cc3300">Your current password is incorrect!</font></b><p>|
  if ($routine eq "bad_pass");

print qq|<b><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1" color="#cc3300">That username is not allowed!</font></b><p>|
  if ($routine eq "no_allow");

print qq|<b><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1" color="#cc3300">It appears that your new password is incorrect in format. The phrase should be up to 8 characters, and may include letters and numbers with no white space.</b></font><p>|
  if ($routine eq "bad_new_pass");

print <<FORM;

<table width="375" cellspacing="0" cellpadding="0" border="0">
 <tr>
  <td valign="middle" width="50%"><form method="post" action="https://www.$domain/$self"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1">Username:&nbsp;</td>
  <td valign="left" width="50%"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1">&nbsp;<b>$ENV{REMOTE_USER}</b></font><input type="hidden" name="username" value="$ENV{REMOTE_USER}"></td>
 </tr>
</table><p>

<table width="375" cellspacing="0" cellpadding="0" border="0">
 <tr>
  <td valign="middle" width="50%"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1">Current Password:&nbsp;</font></td>
  <td valign="middle" width="50%"><input type="password" name="current_password" value="$formdata{current_password}" maxlength="32"></td>
 </tr>
</table><p>

<table width="375" cellspacing="0" cellpadding="0" border="0">
 <tr>
  <td valign="middle" width="50%"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1">New Password:&nbsp;</font></td>
  <td valign="middle" width="50%"><input type="password" name="new_password" value="$formdata{new_password}" maxlength="32"></td>
 </tr>
</table><p>

<table width="375" cellspacing="0" cellpadding="0" border="0">
 <tr>
  <td valign="middle" width="50%"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1">Repeat Password:&nbsp;</font></td>
  <td valign="middle" width="50%"><input type="password" name="repeat_password" value="$formdata{repeat_password}" maxlength="32"></td>
 </tr>
</table><p>

<table width="375" cellspacing="0" cellpadding="0" border="0">
 <tr>
  <td valign="middle" width="50%"><input type="hidden" name="click" value="on"></td>
  <td valign="middle" width="50%"><input type="image" value="Submit" border="0" src="images/submitbutton.gif"></td>
 </tr>
</table><p>

<table width="375" cellspacing="0" cellpadding="0" border="0">
 <tr>
  <td valign="middle" width="50%"></td>
  <td valign="middle" width="50%"><b><font color="cc3300" face="verdana" size="1"><a href="https://www.$domain/$self?instructions=1">directions</a> | <a href="javascript:window.close()">close window</b></font></a></td>
</table>
</form>
FORM

  ## end of if/else routine
  }

}

## check existing password
sub check_pass {

  ## verify field settings before getting into PAM
  if ($formdata{new_password} ne $formdata{repeat_password}) {
    &content('no_match');
  
  } elsif ((mgetpwnam($ENV{REMOTE_USER}))[2] < 504 ) {
    &content('no_allow');

  } elsif ($formdata{new_password} !~ /^[\w]{4,32}$/) {
    &content('bad_new_pass');

  } else {
  
    my $exec = '/usr/bin/sudo ';
    $exec .= '/usr/local/nobody/noverify ';
    $exec .= "--username $ENV{REMOTE_USER} ";
    $exec .= "--password $formdata{current_password} ";

    my $response = system("$exec");

    my $answer = $response >> 8;

    if ($answer) { 
      &content('bad_pass');
  
    } else {
      &modify_pass;
    
    }
  }
}

## encrypt new password
sub modify_pass {

  ## create the salt
  my $random = new String::Random;
  my $salt = $random->randpattern("ss");

  ## encrypt the new password with md5
  my $newpass = unix_md5_crypt($formdata{new_password}, $salt);

  my $exec = '/usr/bin/sudo ';
  $exec .= '/usr/local/nobody/nopasswd ';
  $exec .= "--username $ENV{REMOTE_USER} ";
  $exec .= "--password '$newpass' ";

  system("$exec");

 
  ## return the success page
  &content('success');

}

## pre-defined function from Authen::PAM
sub my_conv_func {

  chomp $ENV{REMOTE_USER};
  chomp $formdata{current_password};

  my @res;
  while ( @_ ) {
      my $code = shift;
      my $msg = shift;
      my $ans = "";


      $ans = $ENV{REMOTE_USER} if ($code == PAM_PROMPT_ECHO_ON() );
      $ans = $formdata{current_password} if ($code == PAM_PROMPT_ECHO_OFF() );


      push @res, (PAM_SUCCESS(),$ans);
  }
  push @res, PAM_SUCCESS();
  return @res;
}

sub check_url {

  my $referer_ok;

  if ($ENV{'HTTP_REFERER'}) {
 
    if ($ENV{'HTTP_REFERER'} =~ m#^https?://(?:www\.)?$domain/controlpanel#i) {

      &bad_referer('nomatch');

    }

  } else {

    &bad_referer('noref');

  }

}

sub bad_referer {

  my $reason = shift;

  if ($reason eq "nomatch") {

print <<"MATCH";
Content-type: text/html

<html>
 <head>
  <title>Bad Referrer - Access Denied</title>
 </head>
 <body bgcolor=#FFFFFF text=#000000>

  $ENV{'HTTP_REFERER'}<br>
  no match!

 </body>
</html
MATCH

  } else {

print <<"MATCH";
Content-type: text/html

<html>
 <head>
  <title>Bad Referrer - Access Denied</title>
 </head>
 <body bgcolor=#FFFFFF text=#000000>

  $ENV{'HTTP_REFERER'}<br>
  no ref!

 </body>
</html>
MATCH

  }

exit 1;
}
