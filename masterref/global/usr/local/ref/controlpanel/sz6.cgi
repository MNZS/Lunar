#!/usr/bin/perl -w

# $Id: sz6.cgi,v 1.2 2002/03/26 14:23:43 root Exp root $

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
<img src="$images/trans158.gif" width="1" height="195" border="0" alt=""><div align="center"><br><a href="http://www.lunarhosting.net/
terms.htm"><font face=Verdana,Geneva,Arial,Helvetica,sans-serif size=-2>Acceptable Usage Policy
</a><br><a href="http://www.lunarhosting.net/privacy.htm">Privacy Statement</a></font>
<p><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="#FFFF99">Version: $rcs</font><p>
</div><img src="$images/trans158.gif" width="1" height="195" border="0" alt=""></font><br>
</td><td><img src="$images/trans10.gif" width="10" height="10" border="0" alt=""></td>
<td valign="top">
<table width="500" border="0" cellspacing="0" cellpadding="0">
<tr><td align="right"><a href="http://www.lunarhosting.net"><img src="$images/portalogo.gif"  border="0" alt="L
unar Media Inc."></a>&nbsp;<p></td>
</tr>
<tr>
<td>&nbsp;<p>
<!-- *********** -->

<font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>START SITE ADMINISTRATION </b><br>The administrative Web pages are located within a secure area. You should have been sent a URL to login to your Administration area.  You may want to bookmark this page. <p> Please enter your user name and password. Your user name is always <b>admin</b>. You should have an email that was sent you containing your administration password.<p><a name="top">
<b>PAYMENT METHODS</b><br>The Payments administration allows you to add/delete/modify the different payment methods you offer in your store.
After logging in, click once on "STORE ADMIN" and then click on PAYMENTS. 
<p>

You will see a list of payment methods you already have established. You may delete any of these options by clicking on Delete. You can not undo this delete. To add a new payment method, click on <b>"Add new payment method"</b> Type in the payment type such as Discover. Note: This text will show up on your order form during checkout.  If it is a credit card that you are adding, the check mark in the box that says validate, just makes sure the credit card has a valid sequence of numbers. It doesn't actually verify the number is an active account. If you add a payment method such as check, personal check, money order, you want to uncheck this box.<p><font face="verdana,arial" color="#ffffcc" size="1"><a href="$self#top">back
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
