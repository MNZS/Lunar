#!/usr/bin/perl -w

# todo
#  - $ENV check on referer
#  - add client side scripting to autopopulate fields when 
#    modifying an alias/destination pair
#  - add file locking

# $Id: panel.cgi,v 1.4 2003/06/09 19:37:21 root Exp $

use strict;
#use warnings;
use Cwd;
use CGI;
use Fcntl ':flock';

##############################################################
###strict assignments
##############################################################

my $rcs = (qw$Revision: 1.4 $)[-1];

my $action;
my $add_alias;
my $add_destination;
my $add_tag;
my $buffer;
my $color;
my @current;
my @entries;
my $error;
my @existing;
my $field;
my $filename;
my %formdata;
my @formfields;
my @getpairs;
my $item;
my $key;
my $groupornot;
my $message;
my $mod_alias;
my $mod_destination;
my $n;
my $pair;
my @pair;
my @pairs;
my $query;
my $result;
my $return_alias;
my $return_destination;
my $selection;
my $tmpfile;
my $value;
my @values;

##############################################################
###parse form
##############################################################

$query = CGI->new();
@formfields = $query->param;

for $field(@formfields) {
  $formdata{$field} = $query->param($field);
}

##############################################################
###begin file definitions
##############################################################

my $domain = (split(/\//, cwd()))[-2];
$filename="/etc/mail/include/virtuser/virt.$domain";
$tmpfile="/etc/mail/include/virtuser/virt.$domain.tmp";

## referer checking
#&check_url;

##############################################################
### resellers

my $reseller;

#if (-e "/etc/hosting-options/$domain/reseller") {

  ## open the reseller file and take its contents as the company
  ## which is reselling lunarhosting service
#  open(FH, "/etc/hosting-options/$domain/reseller");

#  $reseller = <FH>; chomp $reseller;

#  close(FH);

#} else {

  $reseller = "lunarhosting.net";

#}

##############################################################
###add an address
##############################################################

$action = $formdata{action};

if ( $action eq "add" ) {
  $add_alias = lc($formdata{alias});
  $add_destination = lc($formdata{destination});
  $selection = $formdata{choice};

  if (($add_alias) && ($add_destination) && (!$selection)) {
    open MATCH, $filename or die $!;
    flock(MATCH,2);
    seek(MATCH,0,0);
      while (<MATCH>) {
        @existing = split(/\@/, $_);
        if ( $add_alias eq $existing[0] ) {
          $message = "That alias already exists!";
          $error=1;
        }
      }
    flock(MATCH,8);
    close(MATCH);

    ## remove spaces from the alias and destination
    $add_alias =~ s/ //g;
    $add_destination =~ s/ //g;

    if ( $add_alias =~ /[^\w\.\-\_]/ ) {
      $message = "I am sorry, you have entered an \"Illegal\" character in the Alias Field.<br>
           This field can only contain the following characters:<br>
           A-Z, a-z, 0-9, the dash (-), the underscore (_) and the period (.)<p>\n";
      $error=1;

    } elsif ( $add_destination !~ /\@/ ) {
      $message = "I am sorry, the destination address that you entered does not<br>
             appear to be valid. Please re-enter your information.";
      $error=1;

    } elsif ( $add_destination =~  tr/@// != 1 ) {
      $message = "I am sorry. At this time, only a single Destination can<br>
                  be specified for each Alias. If you would like to have<br>
                  multiple recipients, please send a request to <i><a href=
                  \"mailto:support\@$reseller\"><font color=#000000>
                  support\@$reseller</font></a></i>";
      $error=1;

    } elsif ( $error != 1 ) {
      open FILE, ">>$filename" or die $!;
      flock(FILE,2);
      seek(FILE,0,2);
        print FILE "$add_alias\@$domain\t$add_destination\n";
      flock(FILE,8);
      close(FILE);
      open FILE, "$filename" or die $!;
      flock(FILE,2);
      seek(FILE,0,0);
        @entries = <FILE>;
      flock(FILE,8);
      close(FILE);
      @entries = sort(@entries);
      open NEWFILE, ">>$tmpfile" or die $!;
      flock(NEWFILE,2);
      seek(NEWFILE,0,2);
        foreach $item(@entries) {
          print NEWFILE "$item";
        }
      flock(NEWFILE,8);
      close(NEWFILE);
      rename($tmpfile, $filename);
    }

  } elsif ($selection) {
    $message = "I am sorry, when adding a new Alias, you cannot select an existing one.";
    $error=1;

  } else {
      $message = "You must enter something.";
      $error=1;

  }

##############################################################
### modify an existing address
##############################################################

} elsif ( $action eq "mod" ) {
  $mod_alias = lc($formdata{alias});
  $mod_destination = lc($formdata{destination});
  $selection = $formdata{choice};
  if (!$selection) {
    $message = "You must select a record to modify.";
    $error=1;

  } elsif (!$mod_destination) {
    $message = "You must enter some data to update your selection.";
    $error=1;

  } elsif ( $mod_destination =~  tr/@// != 1 ) {      
    $message = "I am sorry. At this time, only a single Destination can<br>
                  be specified for each Alias. If you would like to have<br>
                  multiple recipients, please send a request to <i><a href=
                  \"mailto:support\@$reseller\"><font color=#000000>
                  support\@$reseller</font></a></i>";
    $error=1;

  } elsif ( $mod_destination !~ /\@/ ) {
      $message = "I am sorry, the destination address that you entered does not<br>
             appear to be valid. Please re-enter your information.";
      $error=1;

  } else {
    $selection--;
    open FILE, $filename or die $!;
    flock(FILE,2);
    seek(FILE,0,0);
      @entries=(<FILE>);
    flock(FILE,8);
    close(FILE);
    @current = split(/\t/, $entries[$selection]);
    $entries[$selection]= "$current[0]\t$mod_destination\n";
    open NEWFILE, ">>$tmpfile" or die $!;
    flock(NEWFILE,2);
    seek(NEWFILE,0,2);
      print NEWFILE @entries;
    flock(NEWFILE,8);
    close(NEWFILE);
    rename($tmpfile, $filename);
  }

##############################################################
### delete an existing address
##############################################################

} elsif ( $action eq "del" ) {
  $selection = $formdata{choice};
  if (!$selection) {
    $message = "You must select an entry to delete.<br>\n";
    $error = "1";
  } else {
    $selection--;
    open FILE, $filename or die $!;
    flock(FILE,2);
    seek(FILE,0,0);
      @entries =(<FILE>);
    flock(FILE,8);
    close(FILE);
    splice(@entries, $selection, 1, ());
    open NEWFILE, ">>$tmpfile" or die $!;
    flock(NEWFILE,2);
    seek(NEWFILE,0,2);
      print NEWFILE @entries;
    flock(NEWFILE,8);
    close(NEWFILE);
    rename ($tmpfile, $filename);
  }
}

##############################################################
### error control
##############################################################

if ( $error == 1 ) {
  $return_alias = $formdata{alias};
  $return_destination = $formdata{destination};
}


##############################################################
### html header
##############################################################

print <<begin_html;
Content-type: text/html\n\n
<html>
<head>
  <title>Control Panel</title>
  <SCRIPT LANGUAGE = "JavaScript">
<!--
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
<body background="controlpanel/images/portalback.gif" link="#FFFF99" vlink="#99CC99" alink="#FFFF99" leftmargin=0 topmargin=0 marginheight=0 marginwidth=0>
<img src="controlpanel/images/trans10.gif" width="10" height="10" border="0" alt=""><br><img src="controlpanel/images/trans10.gif" width="10" height="10" border="0" alt=""><br>
<table width="693" border="0" cellspacing="0" cellpadding="0"><tr><td><img src="controlpanel/images/accountadministrationhead.gif" width="296" height="26" border="0" alt="Account Information"></td><td><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2"><b><a href="javascript:window.close()">LOG OUT</a><!--&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="">FAQ</a>-->&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="mailto:support\@$reseller">SUPPORT</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="https://www.$domain/controlpanel/">HOME</a></b></font></td></tr></table>
<table border="0" cellspacing="0" cellpadding="0"><tr><td><img src="controlpanel/images/trans1.gif" width="2" height="1" border="0" alt=""><br><img src="controlpanel/images/trans1.gif" width="2" height="1" border="0" alt=""></td></tr></table>
<table border="0" cellspacing="0" cellpadding="0"><tr>
<td width="193" valign="top" bgcolor="#CC3300">&nbsp;<p>
<center><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="#FFFF99">Welcome!<br>www.$domain</font></center></div>
<!--******* BEGIN TOC *******-->
begin_html

require 'toc.lib';

print <<HTML;
<!--******* END TOC *******-->
<img src="controlpanel/images/trans158.gif" width="1" height="195" border="0" alt=""><div align="center"><br><a href="http://www.$reseller/terms.htm"><font face=Verdana,Geneva,Arial,Helvetica,sans-serif size=-2>Acceptable Usage Policy</a><br> <a  href="http://www.$reseller/privacy.htm">Privacy Statement</a></font><p>
<font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="#FFFF99">Version: $rcs</font><p></div><img src="controlpanel/images/trans158.gif" width="1" height="195" border="0" alt=""></font><br></td>

<td><img src="controlpanel/images/trans10.gif" width="10" height="10" border="0" alt=""></td>

<td valign="top">
<table width="500" border="0" cellspacing="0" cellpadding="0"><tr><td align="right"><form method=post action=https://www.$domain/controlpanel/panel.cgi><a href="http://www.$reseller"><img src="controlpanel/images/$reseller.gif"  border="0" alt="Lunar Media Inc."></a>&nbsp;<p></td></tr><tr><td>&nbsp;<p>
HTML

### error table
if ( $error == 1) {
  print "<!-- *********** -->\n<table width=\"500\" border=\"0\" cellspacing=\"3\" cellpadding=\"0\"><tr><td>$message<\/td><\/tr><\/table>";
}

print <<next_html;
<p>
<table width="500" border="0" cellspacing="3" cellpadding="0"><tr><td><img src="controlpanel/images/emailadmin.gif" width="293" height="21" border="0" alt="Email Account Administration"></td><td valign="bottom"><A HREF="javascript:parent.startndnav('directions.htm')"><img src="controlpanel/images/directions.gif" width="80" height="18" border="0" alt="Directions"></a></td></tr></table><table cellpadding=0 
              cellspacing=0 
              border=0 width=500 
              bgcolor=#000000>
			  <tr><td colspan="12" bgcolor="Black"><img src="controlpanel/images/trans2.gif" width="2" height="2" border="0" alt=""></td></tr>
<tr>
        <td width="2" bgcolor="Black"><img src="controlpanel/images/trans2.gif" width="2" height="2" border="0" alt=""></td><td width="498" colspan="10" bgcolor="#99CC99">
        <font face=Verdana,Geneva,Arial,Helvetica,sans-serif size=-1 color=#000000><b>Choose one:</b></font>&nbsp;&nbsp;
        <font color=#000000><font face=Verdana,Geneva,Arial,Helvetica,sans-serif size=-1><b>Add</b></font>
        </font>&nbsp;<input type=radio name=action value=add checked>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <font color=#000000><font face=Verdana,Geneva,Arial,Helvetica,sans-serif size=-1><b>Change Destination</b></font>&nbsp;
        <input type=radio name=action value=mod>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <font color=#000000><font face=Verdana,Geneva,Arial,Helvetica,sans-serif size=-1><b>Delete</b></font></font>&nbsp;<input type=radio name=action value=del>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        </td> <td width="2" bgcolor="Black"><img src="controlpanel/images/trans2.gif" width="2" height="2" border="0" alt=""></td></tr>
		<tr><td colspan="12" bgcolor="Black"><img src="controlpanel/images/trans2.gif" width="2" height="2" border="0" alt=""></td></tr></table>
		<table cellpadding=0 
              cellspacing=0 
              border=0 width=500 
              bgcolor=#000000>
		<tr>
        <td width="2" bgcolor="Black"><img src="controlpanel/images/trans2.gif" width="2" height="2" border="0" alt=""></td><td  align="center" bgcolor="Black" width="85"><font face=Verdana,Geneva,Arial,Helvetica,sans-serif size=-1 color=#ffffff><b>Select</b></font></td><td width="2" bgcolor="Black"><img src="controlpanel/images/trans2.gif" width="2" height="2" border="0" alt=""></td>
       <td bgcolor=#000000 align=middle width="150"><font face=Verdana,Geneva,Arial,Helvetica,sans-serif size=-1 color=#ffffff><b>Alias</b></font></td>
<td width="2" bgcolor="Black"><img src="controlpanel/images/trans2.gif" width="2" height="2" border="0" alt=""></td>
       <td width="250"  align="center" bgcolor="Black" colspan="6"><font face=Verdana,Geneva,Arial,Helvetica,sans-serif size=-1 color=#ffffff><b>Destination Email</b></font></td> <td width="2" bgcolor="Black"><img src="controlpanel/images/trans2.gif" width="2" height="2" border="0" alt=""></td></tr>
	      <tr><td colspan="12" bgcolor="Black"><img src="controlpanel/images/trans2.gif" width="2" height="2" border="0" alt=""></td></tr>
	</table>
next_html

##############################################################
### dynamic generate table displaying the current list of aliases
##############################################################

open FILE, "$filename" or die $!;
flock(FILE,2);
seek(FILE,0,0);
$n=1;
$result = $n/2;
while (<FILE>) {
  my $flag = "yes";
   @values = split (/\t/, $_);
   if ( $values[1] =~ /^group\-/ ) {
     $groupornot = "Configured as a <a href=\"https://www.$domain/controlpanel/mailgroup.cgi\"><font face=Verdana,Geneva,Arial,Helvetica,sans-serif size=-2 color=#000000>Mailing Group</font></a>"; 
     $flag = "no";

   } elsif ($values[1] =~ /^auto\-/ ) {
     $groupornot = "Configured as an <a href=\"https://www.$domain/controlpanel/responder.cgi\"><font face=Verdana,Geneva,Arial,Helvetica,sans-serif size=-2 color=#000000>Autoresponder</font></a>";
     $flag = "no";

   } else {
     $groupornot  = $values[1];

   }
   @pair = split(/\@/, $values[0]);
   $result = $n/2;
  if ( $result =~ /\./ ) {
    $color="#009999";
  } else {
    $color="#99CC99";
  }
  print <<start;
<table cellpadding=0 
              cellspacing=0 
              border=0 width=500 
              bgcolor=#000000>
 <tr>
 <td width="2" bgcolor="Black"><img src="controlpanel/images/trans2.gif" width="2" height="2" border="0" alt=""></td>
         <td width="85" align="center" bgcolor="$color">
start

if ($flag eq "yes") {
  print "<input type=radio value=$n name=choice ></td>";

} else {
  print "&nbsp;</td>";

}

print <<start;
<td width="2" bgcolor="Black"><img src="controlpanel/images/trans2.gif" width="2" height="2" border="0" alt=""></td>
         <td width="150" bgcolor=$color align=center><font face=Verdana,Geneva,Arial,Helvetica,sans-serif size=-1 size=-1><b>$pair[0]</b></font></td>
<td width="2" bgcolor="Black"><img src="controlpanel/images/trans2.gif" width="2" height="2" border="0" alt=""></td>
         <td width="250" align="center" bgcolor="$color"><font face=Verdana,Geneva,Arial,Helvetica,sans-serif size=-2>$groupornot
</font></td>
 <td width="2" bgcolor="Black"><img src="controlpanel/images/trans2.gif" width="2" height="2" border="0" alt=""></td>
         </tr></table>
		<table cellpadding=0 
              cellspacing=0 
              border=0 width=500 
              bgcolor=#000000>
		 		 <tr><td width="2"  bgcolor="Black"><img src="controlpanel/images/trans2.gif" width="2" height="2" border="0" alt=""></td></tr>
		 </table>
start
  $n++;
}
flock(FILE,8);
close(FILE);

### end of table
 
print "<tr>
        <td bgcolor=#000000 colspan=4 align=middle>&nbsp;
        <\/td>
        <\/tr>
        <tr>
        <td bgcolor=#99CC99 colspan=4 align=left>
        <table>
          <tr>
            <td align=right><font color=#000000><font face=Verdana,Geneva,Arial,Helvetica,sans-serif size=-1><b>Alias:<\/b><\/font><\/font>
            <\/td>
            <td><input type=text length=30 name=alias value=$return_alias><font color=#000000><font face=Verdana,Geneva,Arial,Helvetica,sans-serif size=-1>&nbsp;\@$domain<\/font><\/font>
            <\/td>
          <\/tr>
          <tr>
            <td><font color=#000000><font face=Verdana,Geneva,Arial,Helvetica,sans-serif size=-1><b>Destination:<\/b><\/font><\/font>
            <\/td>
            <td>
              <input type=text length=30 name=destination value=$return_destination>
            <\/td>
          <\/tr>
        <\/table>
        <\/td>
        <\/tr>
        <tr>
        <td bgcolor=#000000 colspan=4 align=middle><input type=submit value=Submit>&nbsp;&nbsp; <input type=reset value=\"Start Over\"><\/td>
        <\/tr>
       <\/tr>";

print "<\/table>\n<\/td>\n<\/tr>\n<\/table>\n";
print "<\/form>\n";

##############################################################
### html footer
##############################################################

print <<end_html;
</body>
</html>
end_html

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
