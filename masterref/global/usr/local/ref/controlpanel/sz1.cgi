#!/usr/bin/perl -w

# $Id: sz1.cgi,v 1.2 2002/03/26 14:23:43 root Exp root $

use strict;
use Cwd;

my $workdir = `pwd`;
my @path = split(/\//, $workdir);
my $domain=$path[2];
my $rcs = (qw$Revision: 1.2 $)[-1];
my $images = "controlpanel/images";

$0 = (split(/\//, $0))[-1];
my $self = "controlpanel/$0";

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
   <body background="$images/portalback.gif" link="#000000" vlink="#000000" alink="#FFFF99" leftmargin="0" topmargin="0" marginheight="0" marginwidth="0"><img src="$images/trans10.gif" width="10" height="10" border="0" alt=""><br><img src="$images/trans10.gif" width="10" height="10" border="0" alt=""><br>
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
<tr><td align="right"><a href="http://www.lunarhosting.net"><img src="$images/portalogo.gif"  border="0" alt="Lunar Media Inc."></a>&nbsp;<p></td>
</tr>
<tr>
<td>&nbsp;<p>

<!-- *********** -->   						              
<a name="top">
<font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>START SITE ADMINISTRATION </b><br>The administrative Web pages a
re located within a secure area. You should have been sent a URL to login to your Administration area.  You may want to bookmark thi
s page. <p> Please enter your user name and password. Your user name is always <b>admin</b>. You should have an email that was sent
you containing your administration password.<p>
<font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>SITE STATISTICS</b>&nbsp;<a href="$self#1">
Hits
</a>|<a href="$self#2">
Pages
</a>|<a href="$self#3">
Hosts
</a><br>Web pages collect information about the number of visitors to
the Web site, the number of visitors to each Web page, and the number of
visitors to the host. The term "hit" refers to a viewer accessing a Web page or
Web site.
<p>To view the statistics, login to the administration Web page as described above.
The Site Administration Web page is displayed.
<p>Click on the Site Statistics button.
The Site Statistics Web page is displayed.<a name="1">
<p>   						                            <b>Hits</b><br>
</a>From the Site Statistics  click Hits. The Hits detail Web page is
displayed.
<p>The Hits Detail by Day section lists the number of viewers that accessed the
Web site on a daily basis. The section expands to a maximum of 30 days.
After 30 days the oldest hits are deleted and replaced with the newest.
<p>The Hits Detail by Month section lists the number of viewers that accessed
the Web site on a monthly basis. The section expands to a maximum of 12
months. After 12 months the oldest hits are deleted and replaced with the
newest.
<p>   						                               
   						                               <font face="verdana,arial" color="#ffffcc" size="1"><a href="$self#top">
back
          to the top
</a></font>
<p><a name="2">
   						                                          <b>Pages</b><br>From the Site Statistics click Pages. The Pages Detail Web
page is displayed.
<p>The Pages Hits Detail by Day section lists the number of viewers that
accessed each Web page on a daily basis. The section maintains the hit
count for a maximum of 30 days. After 30 days the oldest hits are deleted
and replaced with the newest.
<p>The Pages Hits Detail by Month section lists the number of viewers that
accessed the Web site on a monthly basis. The section maintains the hit
count for a maximum of 12 months. After 12 months the oldest hits are
deleted and replaced with the newest.
<p>   						                                             
   						                                             <font face="verdana,arial" color="#ffffcc" size="1"><a href="$self#top">
back
          to the top
</a></font>
<p><a name="3">
   						                                                        <b>Hosts</b><br>The Hosts Web page lists the number of accesses to the Web site IP address
for the last 24 hours, last 30 days, or year to date.
<p>The Hosts Hits by Month section lists the number of viewers that accessed
the host for each month. The section expands to a maximum of 12 months.
After 12 months the oldest hits are deleted and replaced with the newest.
<p>The Hosts Hits Year to Date section lists the total number of viewers to the
host for the current year. The counter is reset to zero at the beginning of the
year.
<p>   						                                                           
   						                                                           <font face="verdana,arial" color="#ffffcc" size="1"><a href="$self#top">
back
          to the top
</a></font>
<p>   						                                                                      NOTE: If you would like to have a more in depth site analysis, we suggest you sign up with a monthly service such as<a href="http://www.sitetracker.com">
www.sitetracker.com
</a>or<a href="http://www.mycomputer.com">
www.mycomputer.com
</a>   						                                                                             Once
   						                                                                             you sign up, we can insert the code into your site.
   						                                                 </font>                            
   						                                                                             
   						                                                                             
   						                                                                             <!--***********-->
   						</td>
   					</tr>
   				</table>
   			</td>
   		</tr>
   	</table>
   </body>
</html>
REST
