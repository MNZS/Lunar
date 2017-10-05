#!/usr/bin/perl -w
 
# $Id: account.cgi,v 1.1 2003/04/10 00:02:32 root Exp $

use strict;
use POSIX qw(strftime);
use Cwd;

my $domain= (split(/\//,cwd()))[-2];
my $rcs = (qw$Revision: 1.1 $)[-1];
my $images = "controlpanel/images";

$0 = (split(/\//, $0))[-1];
my $self = "controlpanel/$0";

###

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
  <tr>
    <td align="right"><a href="http://www.lunarhosting.net"><img src="$images/portalogo.gif"  border="0" alt="Lunar Media Inc."></a>&nbsp;<p></td>
  </tr>

  <tr>
    <td>
<!-- *********** -->   						              
    &nbsp;<p>
<p>


<!-- Monthly Header -->
<table width=400 cellpadding=5 cellspacing=0 border=0>
  <tr>
    <td align=left bgcolor="#000000"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size=-1 color="#FFFF99"><b>&nbsp;Current
 Totals for $month</b></font></td>

  </tr>
</table>

<p>

<!-- Disk Utilization -->
<table width="400" cellpadding="0" cellspacing="0" border="0">
  <tr>
   <td bgcolor="#000000">
    <table width=400 cellpadding=5 cellspacing=2 border=0>
     <tr>
      <td bgcolor="#CC3300" width="33%" rowspan=2 align="middle" bgcolor="#CC3300"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size=-1 color="#FFFF99"><b>Disk<br>Utilization</b></font></td>
      <td width="33%" bgcolor="FEF097" align="right" background="$images/yellowswatch.gif"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size=-2>Allowed:</font>&nbsp;</td>
      <td width="33%" bgcolor="FEF097" align="left" background="$images/yellowswatch.gif">&nbsp;<font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size=-2><b>$plan{$plan} MBytes</b></font></td>
     </tr>
     <tr>
      <td width="33%" bgcolor="FEF097" align="right" background="$images/yellowswatch.gif"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size=-2>Utilized:</font>&nbsp;</td>
      <td width="33%" bgcolor="FEF097" align="left" background="$images/yellowswatch.gif">&nbsp;<font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size=-2><b>$disk_usage $disk_suffix</b></font></td>
     </tr>
    </table>
   </td>
  </tr>
</table>

<p>

<!-- Bandwidth Utilization -->
<table width="400" cellpadding="0" cellspacing="0" border="0">
  <tr>
   <td bgcolor="#000000">
    <table width=400 cellpadding=5 cellspacing=2 border=0>
     <tr>
    <td width="33%" rowspan=2 align="middle" bgcolor="#CC3300"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size=-1 color=
"#FFFF99"><b>Bandwidth<br>Utilization</b></font></td>
    <td width="33%" align="right" bgcolor="FEF097" background="$images/yellowswatch.gif"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size=-2>Allowed:</font>&nbsp;</td>
    <td width="33%" align="left" bgcolor="FEF097" background="$images/yellowswatch.gif">&nbsp;<font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size=-2><b>$disk_plan{$plan} GBytes</b></font></td>
  </tr>
  <tr>
    <td width="33%" align="right" bgcolor="FEF097" background="$images/yellowswatch.gif"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size=-2>Utilized:</font>&nbsp;</td>
    <td width="33%" align="left" bgcolor="FEF097" background="$images/yellowswatch.gif">&nbsp;<font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size=-2><b>$usage $size</b></font></td>
  </tr>
</table>
</td>
</tr>
</table>

<p>

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