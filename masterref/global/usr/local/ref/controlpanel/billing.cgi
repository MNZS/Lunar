#!/usr/bin/perl -w
 
# $Id: template.cgi,v 1.2 2002/04/08 11:37:35 root Exp root $

## universal modules
use strict;
use POSIX qw(strftime);
use Cwd;
use Fcntl ':flock';
use File::Copy;

## specific modules for this script

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
  $formdata{$field} = uc($formdata{$field});
  $formdata{$field} =~ s/^(.{1,50})?.*/$1/g;
}

## taint environmentals
delete @ENV{qw(IFS CDPATH ENV BASH_ENV)};
$ENV{'PATH'} = "/usr/bin:/usr/local/bin";

## universal variables
my $domain = (split(/\//, cwd()))[-2];
my $rcs = (qw$Revision: 1.2 $)[-1];
my $images = "controlpanel/images";
$0 = (split(/\//, $0))[-1];
my $self = "controlpanel/$0";

## specific variables for this script

my $billing_file = "/etc/hosting-options/$domain/billing";

## actions

if ($formdata{modify} eq "ON") {

  open(FH,">$billing_file");

  my $line = $formdata{company_name};
  $line .= "^$formdata{first_name}";
  $line .= "^$formdata{last_name}";
  $line .= "^$formdata{suffix}";
  $line .= "^$formdata{street1}";
  $line .= "^$formdata{street2}";
  $line .= "^$formdata{city}";
  $line .= "^$formdata{state}";
  $line .= "^$formdata{zipcode}";
  $line .= "^$formdata{country}";
  $line .= "^$formdata{phone}";
  $line .= "^$formdata{fax}";

  print FH $line;

  close(FH);

} else {

  open(FH,"$billing_file");

  my $billing_info = <FH>;

  $formdata{company_name} = (split(/\^/,$billing_info))[0];
  $formdata{first_name} = (split(/\^/,$billing_info))[1];
  $formdata{last_name} = (split(/\^/,$billing_info))[2];
  $formdata{suffix} = (split(/\^/,$billing_info))[3];
  $formdata{street1} = (split(/\^/,$billing_info))[4];
  $formdata{street2} = (split(/\^/,$billing_info))[5];
  $formdata{city} = (split(/\^/,$billing_info))[6];
  $formdata{state} = (split(/\^/,$billing_info))[7];
  $formdata{zipcode} = (split(/\^/,$billing_info))[8];
  $formdata{country} = (split(/\^/,$billing_info))[9];
  $formdata{phone} = (split(/\^/,$billing_info))[10];
  $formdata{fax} = (split(/\^/,$billing_info))[11];

  close(FH);

}


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
</a>-->&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="mailto:support\@lunarhosting.net">
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
	
	require 'toc.lib';
	
print<<REST;
	
	<!--******* END TOC *******-->
<img src="$images/trans158.gif" width="1" height="195" border="0" alt=""><div align="center"><br><a href="http://www.lunarhosting.net/terms.htm"><font face=Verdana,Geneva,Arial,Helvetica,sans-serif size=-2>Acceptable Usage Policy
</a><br><a href="http://www.lunarhosting.net/privacy.htm">Privacy Statement</a></font>
<p><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="#FFFF99">Version: $rcs</font><p>
</div><img src="$images/trans158.gif" width="1" height="195" border="0" alt=""></font><br>
</td><td><img src="$images/trans10.gif" width="10" height="10" border="0" alt=""></td>
<td valign="top">

<table width="500" border="0" cellspacing="0" cellpadding="0">
<tr><td align="right"><a href="http://www.lunarhosting.net"><img src="$images/portalogo.gif" border="0" alt="L
unar Hosting Inc."></a>&nbsp;<p></td>
</tr>

  <tr>
    <td>
<!-- *********** -->   						              
<font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1">The following form should be used to update billing information for your business' account with Lunar Media.</font>
<p>
<font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1">Please note that Lunar Hosting will use <b>info\@$domain</b> for all e-mail correspondance. If for any reason you prefer a different address be used, please email <a href="mailto:support\@lunarhosting.net">support\@lunarhosting.net</a> to make the change request.</font>
<p>
<font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1">This information is considered confidential and will not be released to any third parties. Lunar Hosting will use this information only for purposes of contacting clients for billing purposes or for periodic announcements concerning new products and service upgrades.</font>
<p>

<form action="$self" method="post">
<table width="450" cellpadding="0" cellspacing="2" border="0">
 <tr>
  <input name="modify" type="hidden" value="on">
  <td><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>Company Name:</b></font> </td><td><input name="company_name" type="text" size="35" maxlength="40" value="$formdata{company_name}"></td>
 </tr>
 <tr>
  <td><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>First Name:</b></font> </td><td><input name="first_name" type="text" size="35" maxlength="40" value="$formdata{first_name}"></td>
 </tr>
 <tr>
  <td><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>Last Name:</b></font> </td><td><input name="last_name" type="text" size="35" maxlength="40" value="$formdata{last_name}"></tr>
 </tr>
 <tr>
  <td><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>Suffix:</b></font> </td><td><input name="suffix" type="text" size="35" maxlength="40" value="$formdata{suffix}"></td>
 </tr>
 <tr>
  <td><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>Street Address:</b></font> </td><td><input name="street1" type="text" size="35" maxlength="40" value="$formdata{street1}"></td>
 </tr>
 <tr>
  <td><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>Street Address:</b></font> </td><td><input name="street2" type="text" size="35" maxlength="40" value="$formdata{street2}"></td>
 </tr>
 <tr>
  <td><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>City:</b></font> </td><td><input name="city" type="text" size="35" maxlength="40" value="$formdata{city}"></td>
 </tr>
 <tr>
  <td><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>State:</b></font></td><td><input name="state" type="text" size="35" maxlength="40" value="$formdata{state}"></td>
 </tr>
 <tr>
  <td><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>Zip Code:</b></font></td><td><input name="zipcode" type="text" size="35" maxlength="40" value="$formdata{zipcode}"></td>
 </tr>
 <tr>
  <td><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>Country:</b></font></td><td><input name="country" type="text" size="35" maxlength="40" value="$formdata{country}"></td>
 </tr>
 <tr>
  <td><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>Telephone:</b></font></td><td><input name="phone" type="text" size="35" maxlength="40" value="$formdata{phone}"></td>
 </tr>
 <tr>
  <td><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>Fax:</b></font></td><td><input name="fax" type="text" size="35" maxlength="40" value="$formdata{fax}"></td>
 </tr>
 <tr>
  <td colspan="2" align="center"><input type="submit" value="Update Information"></td>
 </tr>
</table>
</form>



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
