#!/usr/bin/perl -w

# $Id: sz3.cgi,v 1.2 2002/03/26 14:23:43 root Exp root $

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
<body background="$images/portalback.gif" link="black" vlink="#99CC99" alink="#FFFF99" leftmargin=0 topmargin=0 marginheight=0 marginwidth=0>
<img src="$images/trans10.gif" width="10" height="10" border="0" alt=""><br><img src="$images/trans10.gif" width="10" height="10" border="0" alt=""><br>
<table width="693" border="0" cellspacing="0" cellpadding="0"><tr><td><img src="$images/accountadministrationhead.gif" width="296" height="26" border="0" alt="Account Information"></td><td><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2"><b><a href="javascript:window.close()"><b><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="#FFFF99">LOG OUT</font></b></a><!--&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="">FAQ</a>-->&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="mailto:support\@lunarhosting.net"><b><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="#FFFF99">SUPPORT</font></b></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="https://www.$domain/controlpanel/"><b><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="#FFFF99">HOME</font></b></a></b></font></td></tr></table>
<table border="0" cellspacing="0" cellpadding="0"><tr><td><img src="$images/trans1.gif" width="2" height="1" border="0" alt=""><br><img src="$images/trans1.gif" width="2" height="1" border="0" alt=""></td></tr></table>
<table border="0" cellspacing="0" cellpadding="0"><tr>
<td width="193" valign="top" bgcolor="#CC3300">&nbsp;<p>



<center><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="#FFFF99"><b>Welcome!<br>www.$domain</b></font></center></div>

<!--******* SIDE TOC *******-->
START


require 'toc.lib';

print<<REST;

<!--******* END TOC *******-->
<img src="$images/trans158.gif" width="1" height="195" border="0" alt=""><div align="center"><br><a href="http://www.lunarhosting.net/terms.htm"><font face=Verdana,Geneva,Arial,Helvetica,sans-serif size=-2 color="#FFFF99" size="-2">Acceptable Usage Policy</font></a><br> <a  href="http://www.lunarhosting.net/privacy.htm"><font face=Verdana,Geneva,Arial,Helvetica,sans-serif size=-2 color="#FFFF99" size="-2">Privacy Statement</font></a><p>
<font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="#FFFF99">Version: $rcs</font><p></div><img src="$images/trans158.gif" width="1" height="195" border="0" alt=""></font><br></td>

<td><img src="$images/trans10.gif" width="10" height="10" border="0" alt=""></td>

<td valign="top">
<table width="500" border="0" cellspacing="0" cellpadding="0"><tr><td align="right"><a href="http://www.lunarhosting.net"><img src="$images/portalogo.gif"  border="0" alt="Lunar Media Inc."></a></td></tr><tr><td><p>
<!-- *********** -->
<a name="top">
<font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>START SITE ADMINISTRATION </b><br>The administrative Web pages are located within a secure area. You should have been sent a URL to login to your Administration area.  You may want to bookmark this page. <p> Please enter your user name and password. Your user name is always <b>admin</b>. You should have an email that was sent you containing your administration password.<p>
<b>DATABASE DRIVEN FORMS</b>
<br>The Form Web pages provide the capability for viewers to enter text in form
fields and submit the information to be added to a database. Administration of a Form Web page allows the Web site administrator to
make changes to the Form Web site database.
<p><b>NOTE:This tutorial is only meant for sites that have had a form installed on an existing web site utilizing ShopZone's software.</b> This is a form that stores information in a database. It is not the same as a basic form that sends information to you via email only. If you currently have a ShopZone site, please <a href="mailto:info\@lunarhosting.net"><b>email us</b></a> if you would like us to add a form, or additional forms, to your site.<p>
Log into your site administration as described above.
Your form name has a unique title to your web site. You should have this information if you have a form on your web site. For example, it may be<b><i> Mailing List</i></b> or <b><i>Newsletter</i></b>.
<a name="1"><p><b>Messages and Categories</b><br></a>
From the Form Web Site Administration Web page the administrator can
add, view, and search for Form database records. In addition, the database
records can be saved to a text database file.<p>The records that have been added to the Form database for the current date
are listed at the top of the Web page. Click <b>View all Records</b> to show all of
the Form records.<p>
Click on the record to display the content of the record. You can then change any information, and click on <b>Update Record</b>.  Click on <b>Delete</b> to
remove the record from the Form database.<p><b>WARNING: There is no confirmation when you delete a record. If you delete a
record, you cannot undo the deletion.</b><p>
Click <b>Add New Record</b> to add a record to the Form database. Enter the
Form fields and click <b>Add Record</b>.
To search for specific records, enter the search criteria and click <b>New
Search</b>. To keep the same search criteria, but change one option, make the
changes and click <b>Refine Search</b>.<p><font face="verdana,arial" color="#ffffcc" size="1"><a href="$self#top">back
          to the top</a></font><p>
<br></font>
<!--***********-->

</td>
</tr>
</table>
</td></tr></table>
</body>
</html>
REST
