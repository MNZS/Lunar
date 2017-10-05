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
}

## taint environmentals
delete @ENV{qw(IFS CDPATH ENV BASH_ENV)};
$ENV{'PATH'} = "/bin";

## universal variables
my $domain = (split(/\//, cwd()))[-3];
my $rcs = (qw$Revision: 1.2 $)[-1];
my $images = "controlpanel/images";
$0 = (split(/\//, $0))[-1];
my $self = "controlpanel/$0";

## specific variables for this script

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
	
	require './toc.lib';
	
print<<REST;
	
	<!--******* END TOC *******-->
<img src="$images/trans158.gif" width="1" height="195" border="0" alt=""><div align="center"><br><a href="http://www.lunarhosting.net/terms.htm"><font face=Verdana,Geneva,Arial,Helvetica,sans-serif size=-2>Acceptable Usage Policy
</a><br><a href="http://www.lunarhosting.net/privacy.htm">Privacy Statement</a></font>
<p><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="#FFFF99">Version: $rcs</font><p>
</div><img src="$images/trans158.gif" width="1" height="195" border="0" alt=""></font><br>
</td><td><img src="$images/trans10.gif" width="10" height="10" border="0" alt=""></td>
<td valign="top">

<table width="500" border="0" cellspacing="0" cellpadding="0">
<tr><td align="right"><a href="http://www.lunarhosting.net"><img src="$images/portalogo.gif" border="0">
</a>&nbsp;<p></td>
</tr>

  <tr>
    <td>
<!-- *********** -->   						              

<!-- TEMPLATE
&nbsp;&nbsp;&nbsp;<a href="controlpanel/faq/"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-2">QUESTION?</font></a><br>
-->

<!-- Tech Support -->
<font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-1"><b>Technical Support</b><br>
&nbsp;&nbsp;&nbsp;<a href="controlpanel/faq/sitedown.cgi"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-2">My website is down! Who do I call?</font></a><br>
&nbsp;&nbsp;&nbsp;<a href="controlpanel/faq/support.cgi"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-2">My question isn't in the FAQ What do I do next?</font></a><br>

<p>
<!-- Billing -->

<!--
<font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-1"><b>Billing</b><br>
&nbsp;&nbsp;&nbsp;<a href="controlpanel/faq/"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-2">How do I update my billing address information?</font></a><br>
&nbsp;&nbsp;&nbsp;<a href="controlpanel/faq/"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-2">Are there any fees to upgrade/downgrade my plan?</font></a><br>
&nbsp;&nbsp;&nbsp;<a href="controlpanel/faq/"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-2">How will I be billed for my website?</font></a><br>
&nbsp;&nbsp;&nbsp;<a href="controlpanel/faq/"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-2">What forms of payment are available?</font></a><br>
&nbsp;&nbsp;&nbsp;<a href="controlpanel/faq/"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-2">How can I cancel my account?</font></a><br>
&nbsp;&nbsp;&nbsp;<a href="controlpanel/faq/"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-2">What is your account suspension policy?</font></a><br>
&nbsp;&nbsp;&nbsp;<a href="controlpanel/faq/"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-2">I have a specific question about my bill, who should I contact?</font></a><br>
-->

<p>
<!-- Statistics -->
<font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-1"><b>Site Statistics</b></font><br>
&nbsp;&nbsp;&nbsp;<a href="controlpanel/faq/offerstats.cgi"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-2">Do you offer Site Statistic information?</font></a><br>
&nbsp;&nbsp;&nbsp;<a href="controlpanel/faq/availstats.cgi"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-2">What statistics are available?</font></a><br>
&nbsp;&nbsp;&nbsp;<a href="controlpanel/faq/coststats.cgi"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-2">Does statistic information cost extra each month?</font></a><br>

<p>
<!-- Email -->
<font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-1"><b>E-Mail</b></font><br>
&nbsp;&nbsp;&nbsp;<a href="controlpanel/faq/outlook.cgi"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-2">How do I configure Outlook Express to send and receive mail from Lunar Hosting?</font></a><br>
<!--
&nbsp;&nbsp;&nbsp;<a href="controlpanel/faq/"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-2">How do I configure Eudora to send and receive mail from Lunar Hosting?</font></a><br>
&nbsp;&nbsp;&nbsp;<a href="controlpanel/faq/"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-2">How do I configure Netscape Mail to send and receive mail from Lunar Hosting?</font></a><br>
-->
&nbsp;&nbsp;&nbsp;<a href="controlpanel/faq/groups.cgi"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-2">How can I configure an e-mail address to have multiple recipients?</font></a><br>
&nbsp;&nbsp;&nbsp;<a href="controlpanel/faq/emailchange.cgi"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-2">I've made changes in my e-mail settings but they don't seem to have taken effect?</font></a><br>

<p>
<!-- FTP -->
<font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-1"><b>FTP</b></font><br>
&nbsp;&nbsp;&nbsp;<a href="controlpanel/faq/ftp.cgi"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-2">How can I update my website using FTP?</font></a><br>
&nbsp;&nbsp;&nbsp;<a href="controlpanel/faq/cuteftp.cgi"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-2">How can I use GlobalScape's CuteFTP to update my website?</font></a><br>
&nbsp;&nbsp;&nbsp;<a href="controlpanel/faq/anonftp.cgi"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-2">Do you support Anonymous FTP?</font></a><br>
&nbsp;&nbsp;&nbsp;<a href="controlpanel/faq/bandftp.cgi"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-2">Do my FTP transfers count towards my total allowed bandwidth for the month?</font></a><br>

<p>
<!-- Connectivity -->
<font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-1"><b>Server Administration and Network Connectivity</b><br>
&nbsp;&nbsp;&nbsp;<a href="controlpanel/faq/maintenance.cgi"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-2">What is your policy concerning maintenance being done to servers?</font></a><br>
&nbsp;&nbsp;&nbsp;<a href="controlpanel/faq/notification.cgi"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-2">Will I be notified prior to work being done on servers?</font></a><br>

<p>
<!-- Policies -->
<font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-1"><b>Company Policies</b></font><br>
&nbsp;&nbsp;&nbsp;<a href="controlpanel/faq/spam.cgi"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-2">What are your policies concerning spam?</font></a><br>
&nbsp;&nbsp;&nbsp;<a href="controlpanel/faq/aup.cgi"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-2">What is your Acceptable Use Policy?</font></a><br>
<!--
&nbsp;&nbsp;&nbsp;<a href="controlpanel/faq/availability.cgi"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-2">What is your policy concerning Downtime?</font></a><br>
-->

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
