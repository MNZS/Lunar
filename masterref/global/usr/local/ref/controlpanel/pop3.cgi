#!/usr/bin/perl
 
# $Id: pop3.cgi,v 1.12 2003/07/05 18:25:43 root Exp $

## universal modules
use strict;
use POSIX qw(strftime);
use Cwd;
use Fcntl ':flock';
use File::Copy;

## specific modules for this script
use String::Random;
use Passwd::Linux qw(modpwinfo mgetpwnam);

## cgi.pm parameters
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

## taint environmentals
my $path = $ENV{'PATH'};
$ENV{'PATH'} = "/bin:/usr/bin:/usr/local/nobody";
delete @ENV{qw(IFS CDPATH ENV BASH_ENV)};
$path = $ENV{'PATH'};

## universal variables
my $domain = (split(/\//, cwd()))[-2];
$domain =~ /^((?:[\w\-]+\.)?(?:[\w\-]+\.)(?:\w{2,3}\.)?(?:\w{2,4}))$/;
$domain = $1;

my $rcs = (qw$Revision: 1.12 $)[-1];
my $images = "controlpanel/images";
$0 = (split(/\//, $0))[-1];
my $self = "controlpanel/$0";

## specific variables for this script
  my $popfile = "/etc/hosting-options/$domain/pop3";

  ## max number of accounts
  my %plan = ( bronze => "30", silver => "50", gold => "75", diamond => "250",);

  ## grab current plan
  open(FH, "/etc/hosting-options/$domain/plan");
  my $plan = <FH>;
  close(FH);

  chomp $plan;

### End of perl definitions ###

print<<START;
Content-type: text/html\n\n
<html>
<head>
    <title>
        Control Panel
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
<base href="https://www.$domain/">
</head>

<!-- BEGIN BODY DEFINES -->
   <body background="$images/portalback.gif" link="#000000" vlink="#000000" alink="#FFFF99" leftmargin="0" topmargin="0" marginheight="0" marginwidth="0"><img src="$images/trans10.gif" width="10" height="10" border="0" alt=""><br><img src="$images/trans10.gif" width="10" height="10" border="0" alt=""><br>
<!-- BEGIN TOP TABLE LINKS -->
   	<table width="693" border="0" cellspacing="0" cellpadding="0">
   		<tr><td><img src="$images/accountadministrationhead.gif" width="296" height="26" border="0" alt="Account Information"></td>
   			<td><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2"><a href="javascript:window.close()">
<b><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="#FFFF99">LOG OUT</font></b></a><!--&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="">
<b><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="#FFFF99">FAQ</font></b>
</a>-->&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="mailto:support\@lunarmedia.net">
<b><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="#FFFF99">SUPPORT</font></b>
</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="https://www.$domain/controlpanel/">
<b><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="#FFFF99">HOME</font></b>
</a></font></td></tr>
   	</table>
   	<table border="0" cellspacing="0" cellpadding="0">
   		<tr><td><img src="$images/trans1.gif" width="2" height="1" border="0" alt=""><br><img src="$images/trans1.gif" width="2" height="1" border="0" alt=""></td></tr>
   	</table>
   	<table border="0" cellspacing="0" cellpadding="0"><tr><td width="193" valign="top" bgcolor="#CC3300">&nbsp;<p>
   			<center><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="#FFFF99">Welcome!<br>www.$domain</font></center></div>

<!--******* SIDE TOC *******-->
START
	
	require './toc.lib';
	
print<<REST;
	
	<!--******* END TOC *******-->
<img src="$images/trans158.gif" width="1" height="195" border="0" alt=""><div align="center"><br><a href="http://www.lunarmedia.net/terms.htm"><font face=Verdana,Geneva,Arial,Helvetica,sans-serif size=-2>Acceptable Usage Policy
</a><br><a href="http://www.lunarmedia.net/privacy.htm">Privacy Statement</a></font>
<p><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="#FFFF99">Version: $rcs</font><p>
</div><img src="$images/trans158.gif" width="1" height="195" border="0" alt=""></font><br>
</td><td><img src="$images/trans10.gif" width="10" height="10" border="0" alt=""></td>
<td valign="top">

<table width="500" border="0" cellspacing="0" cellpadding="0">
<tr><td align="right"><a href="http://www.lunarmedia.net"><img src="$images/portalogo.gif" border="0" alt="Lunar Hosting Inc."></a>&nbsp;<p></td>
</tr>

  <tr>
    <td>
<!-- *********** -->   						              
REST

## add a new user
if ($formdata{action} eq "add") {

  &check_num;

} elsif ($formdata{action} eq "remove") {

  &check_data;

} elsif ($formdata{action} eq "modify") {
  
  &check_data;

} else {

  &show_current;

}

print <<REST;
<!-- *********** -->
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>

</body>
</html>
REST

exit 0;

## subroutines

sub show_current {

## open the list of current pop3 accounts
open(FH, "$popfile")
  or die "Cant open POP3 users list : $!\n";
flock(FH,2);
seek(FH,0,0);

my @pop_users = <FH>;

flock(FH,8);
close(FH);

my $current = scalar(@pop_users);
my $maximum = $plan{$plan};

## variables to create alternating table bgcolors
my $count="1";
my @bgcolor = ("junk", "#99CC99", "#009999");

## create our table
print <<REST;
<!-- First table to set border color -->
<table width="600" cellspacing="0" cellpadding="0" border="0">
 <tr>
  <td bgcolor="#000000">
   <table width=600 border="0" cellspacing="2" cellpadding="5">
    <tr>
     <td bgcolor="#000000" colspan="2"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#FFFF99" size="-1"><b>$current of a possible $maximum POP3 accounts configured for $domain</b></font></td>
    </tr>
REST

## if there are no addresses configured then
if ($#pop_users < 0) {
  print qq|<tr><td colspan="2" bgcolor="$bgcolor[$count]"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>There are currently no POP3 accounts configured.</b></font></td></tr>\n|;

## if there are addresses configured
} else {
  for my $i(sort @pop_users) {
    print qq|<tr><td bgcolor="$bgcolor[$count]" width="20%" align="center"><a href="https://www.$domain/$self?action=remove&username=$i"><img src="$images/delete.gif" border="0"></a>&nbsp;&nbsp;&nbsp;<a href="https://www.$domain/$self?action=modify&username=$i"><img src="$images/edit.gif" border="0"></a></td><td bgcolor="$bgcolor[$count]" valign="middle"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif"size="-1"><b>$i</b></font></td></tr>\n|;
    
    ## affect the counter to vary the cell bgcolor
    if ($count > 1) { $count-- } else { $count++ }

  ## end for
  }

## endif
}

## table for adding new users
print <<REST;
   </table>
  </td>
 </tr>
</table>
<p>
<!-- First table to set border color -->
<table width="600" cellspacing="0" cellpadding="0" border="0">
 <tr>
  <td bgcolor="#000000">
   <table width=600 border="0" cellspacing="2" cellpadding="5">
    <tr>
     <td bgcolor="#000000"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#FFFF99" size="-1"><b>Add a new user</b></font></td>
    </tr>
      <form method="post" action="https://www.$domain/$self">
      <td bgcolor="#99CC99" width="35%"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1">Username (4-8 characters):</font>&nbsp;</td>
      <td bgcolor="#99CC99"><input type="text" maxlength="16" length="20" name="username" value="$formdata{username}"></td>
    </tr>
    <tr>
      <td bgcolor="#99CC99"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1">Password (4-8 characters):</font>&nbsp;</td>
      <td bgcolor="#99CC99"><input type="password" maxlength="8" length="20" name="pwfirst" value="$formdata{pwfirst}"></td>
    </tr>
    <tr>
      <td bgcolor="#99CC99"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1">Repeat Password:</font>&nbsp;</td>
      <td bgcolor="#99CC99"><input type="password" maxlength="8" length="20" name="pwsecond" value="$formdata{pwsecond}"></td>
    </tr>
    <tr>
      <td bgcolor="#99CC99"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1">Real Name (Optional):</font>&nbsp;</td>
      <td bgcolor="#99CC99"><input type="text" maxlength="32" length="20" name="comment" value="$formdata{comment}"></td>
    </tr>
    <tr>
      <td bgcolor="#99CC99" colspan="2"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1">Administrator (Allows access to Control Panel)&nbsp;&nbsp;<input type="checkbox" name="adminrights" value="on"></font></td>
    </tr>
    <tr>
      <td bgcolor="#99CC99" colspan="2"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1">FTP Access (Allows user to update website)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input type="checkbox" name="ftprights" value="on"></font></td>
    </tr>
    <tr>
      <input type="hidden" name="action" value="add">
      <td bgcolor="#99CC99" colspan="2"><input type=submit></td>
    </tr>
    </form>
   </table>
  </td>
 </tr>
</table>
REST
 
## end show_current
}

sub check_num {

  open(FH, "$popfile")
  or die "Cant open POP3 users list : $!\n";
  flock(FH,2);
  seek(FH,0,0);

  my @pop_users = <FH>;

  flock(FH,8);
  close(FH);

  my $current = scalar(@pop_users);
  my $maximum = $plan{$plan};

  if ($current+1 > $maximum) {

    &gen_error('maximum');

  } else {

    &check_data;

  }
}

sub check_data {

  my $passBad;
  my $userBad;

  ## clean up user's name
  $formdata{username} =~ s/ //g;
  $formdata{username} =~ tr/A-Z/a-z/;
  $formdata{username} =~ s/[^a-z0-9\-\_]//g;
  $formdata{username} =~ /^([a-z0-9\-\_]{1,16}).*$/;
  $formdata{username} = $1;

  chomp $formdata{username};

  ## check to see if another user exists
  $userBad = &check_user($formdata{username});

  if ($formdata{action} eq "add") {

    ## clean up passwords
    $formdata{pwfirst} =~ s/ //g;
    $formdata{pwfirst} =~ /^(.{1,8}).*$/;
    $formdata{pwfirst} =~ $1;
    chomp $formdata{pwfirst};
    $formdata{pwsecond} =~ s/ //g;
    $formdata{pwsecond} =~ /^(.{1,8}).*$/;
    $formdata{pwsecond} = $1;
    chomp $formdata{pwsecond};

    ## check to see if the passwords submitted match
    $passBad = &check_pass("$formdata{pwfirst}","$formdata{pwsecond}");

  }

  if ($formdata{username} =~ /^\d/) {

    &gen_error('username');

  } elsif ($passBad) {

    &gen_error('password');

  } elsif ($userBad) {

    &gen_error('username');

  } elsif ($formdata{action} eq "add") {

    &add_user;

  } elsif ($formdata{action} eq "modify") {

    &modify_user;

  } elsif ($formdata{action} eq "remove") {

    &remove_user;

  } else { 
 
    exit 1;

  }

## end check_data
}

sub check_user {

  my $username = shift;

  chomp $username;

  ## check to see if the username exists on the system
  my $uid = getpwnam($username);

  if ($formdata{action} eq "add") {

    return "1" if (defined $uid);
  
  } elsif (($formdata{action} eq "remove") || ($formdata{action} eq "modify")) {

    return "1" if ($formdata{username} eq "root");

    return "1" if (!$uid);

    return "1" if ($uid < 503);

  }

}

sub check_pass {

  my $one = shift; chomp $one;
  my $two = shift; chomp $two;

  ## check for null passwords
  return "1" if (($one eq "") && ($two eq ""));

  ## check for non-matching passwords
  return "1" if ( $one ne $two );

}

sub add_user {
  my $exec = 'sudo /usr/local/nobody/nouseradd ';
  $exec .= '--add ';
  $exec .= "--webuser $ENV{REMOTE_USER} ";
  $exec .= "--username $formdata{username} ";
  $exec .= "--passwd $formdata{pwfirst} ";
  $exec .= "--comment '$formdata{comment}' ";
  $exec .= "--domain $domain ";
  ## ftp and admin rights
  if ($formdata{ftprights}) {
    $exec .= '--ftp ';
  }
  if ($formdata{adminrights}) {
    $exec .= '--admin ';
  }

  ## add the user
  system("$exec");

  ## place user in the file of pop users
  open(FH, ">>/etc/hosting-options/$domain/pop3")
    or die "POP3 file does not exist : $!\n";
  flock(FH,2);
  seek(FH,0,0);

  print FH "$formdata{username}\n";

  flock(FH,8);
  close(FH);

  print qq|<font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1" color="#CC3300"><b>The user was successfully added!</b></font><p>|;

  %formdata = ();

  &show_current;

}

sub remove_user {
  my $exec = '/usr/bin/sudo /usr/local/nobody/nouseradd ';
  $exec .= '--remove ';
  $exec .= "--username $formdata{username} ";
  $exec .= "--webuser $ENV{REMOTE_USER} ";
  $exec .= "--domain $domain";

  system("$exec");

  ## read in the list of users
  open(FH, "/etc/hosting-options/$domain/pop3")
    or die "POP3 file cant be opened : $!\n";
  flock(FH,2);
  seek(FH,0,0);

  my @users = <FH>;

  flock(FH,8);
  close(FH);

  ## print list back in except for selected user
  open(FH, ">/etc/hosting-options/$domain/pop3")
    or die "POP3 file cant be opened : $!\n";
  flock(FH,2);
  seek(FH,0,0);

  for my $i(@users) {

    chomp $i;

    print FH "$i\n" unless ($i eq $formdata{username});

  }

  flock(FH,8);
  close(FH);

  print qq|<font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-1"><b>The user was successfully removed!</b></font><p>|;

  %formdata= ();

  &show_current;

}

sub gen_error {
  my $reason = shift;

  if ($reason eq "username") {

    print qq|<font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-1"><b>That username is not available. Please select another.<p></b></font>|;

  } elsif ($reason eq "password") {

    print qq|<font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-1"><b>It does not appear that your passwords match. Please try again.</b></font><p>|;

  } elsif ($reason eq "maximum") {

    print qq|<font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-1"><b>I'm afraid you have reached your maximum number of allowed POP3 accounts.<br>Please upgrade your service plan to allow for additional acccounts.</b></font><p>|;

  } else {

    print qq|<font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-1"><b>Its appears that you are passing incorrect data to the application.<br>Please try again.</b></font><p>|;

  }

  &show_current;

}

sub modify_user {

if ($formdata{hint} eq "recover") {

  &recover_passwd;

} else {

  print <<HTML;

<!-- First table to set border color -->
<table width="300" cellspacing="0" cellpadding="0" border="0">
 <tr>
  <td bgcolor="#000000">
   <table width=300 border="0" cellspacing="2" cellpadding="5">
    <tr>
    <form action="https://www.$domain/$self" method="post">
     <td bgcolor="#99CC99" width="50%"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#000000">Username:</font></td>
     <input type="hidden" name="action" value="modify"><input type="hidden" name="hint" value="recover">
     <input type="hidden" name="username" value="$formdata{username}">
     <td bgcolor="#99CC99" width="50%"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#000000"><b>$formdata{username}</b></font></td>
    </tr>
    <tr>
     <td bgcolor="#99CC99" width="50%"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#000000">Password:</font></td>
     <td bgcolor="#99CC99" width="50%"><input type="password" maxlength="8" length="5" name="password"></td>
    </tr>
   </table>
  </td>
 </tr>
</table>
<p>
<input type="submit">
</form>
HTML

}

}

sub recover_passwd {

  ## clean up user's name
  $formdata{username} =~ s/ //g;
  $formdata{username} =~ tr/A-Z/a-z/;
  $formdata{username} =~ s/[^a-z0-9\-\_]//g;
  $formdata{username} =~ /^([a-z0-9\_\-]{1,16}).*$/;
  $formdata{username} = $1;

  chomp $formdata{username};

  ## check to see if another user exists
  my $userBad = &check_user($formdata{username});

  ## clean up passwords
  $formdata{password} =~ s/ //g;
  $formdata{password} =~ /^(.{1,8}).*$/;
  $formdata{password} =~ $1;
  chomp $formdata{password};

  ## check to see if the passwords submitted match
  if (length($formdata{password}) < 1) {

    &gen_error('password');


  } elsif ($userBad) {

    &gen_error('username');

  } else {

    ## create password

    ## generate random characters
    my $random = new String::Random;

    ## salt the passwd
    my $salt = $random->randpattern("ss");

    ## encrypt the password
    my $crypt = crypt($formdata{password}, $salt);
    
    my $exec = '/usr/bin/sudo ';
    $exec .= '/usr/local/nobody/nopasswd ';
    $exec .= "--username $formdata{username} ";
    $exec .= "--password $crypt ";

    system("$exec");

    print qq|<font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-1"><b>The password for $formdata{username} was successfully changed!</b></font><p>|;
    %formdata = ();

    &show_current;

  }

}

