#!/usr/bin/perl -w

# $Id: sz4.cgi,v 1.2 2002/03/26 14:23:43 root Exp root $

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
<a name="top">
<font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>START SITE ADMINISTRATION </b><br>The administrative Web pages are located within a secure area. You should have been sent a URL to login to your Administration area.  You may want to bookmark this page. <p> Please enter your user name and password. Your user name is always <b>admin</b>. You should have an email that was sent you containing your administration password.<p>
<b>ORDER ADMINISTRATION</b> <a href="https://www.$domain/$self#1">Viewing an Order</a> | <a href="$self#2">Order Search</a> | <a href="$self#3">Order Detail</a>
<br>You should be familiar with the shopping process on your site. If you haven't already, please place a few orders to see how your store functions. If you have CyberCash or other automated credit card processing software connected to your cart, you can keep another payment option, such as personal check, available while you do testing. This allows you to skip the credit card section of the ordering process, and still submit the order without being charged.
<p>
You should receive an email message notifying you of an order that has been placed. If you have done the test order, you may also receive a email message as a receipt  of the order you have just placed. Normally, you would just receive the ORDER NOTIFICATION email.  
<a name="1"><p><b>Viewing an Order</b><br></a>
You can click on the link directly from the ORDER NOTIFICATION email, or login into your administration as described above.  Once you have logged into your admin area, click on <b>STORE ADMIN</b> and then<b>ORDER ADMIN</b> link from the list of links on the right.  If you have had orders placed today, the orders will be listed on this page. If you would like to view all of the orders placed to date, click on the link towards the bottom that says <b>View all orders</b>. <p><font face="verdana,arial" color="#ffffcc" size="1"><a href="$self#top">back
          to the top</a></font><p>
<a name="2"><b>Order Search</b><br>
You can limit the orders displayed in several ways. You can search by date by clicking the box that says "DATE SEARCH". In the From and To Fields, enter the start date you want to begin searching by(FROM) and the end date you want to stop searching by (TO). For example: FROM:2001, Jul 12 TO 2001, July 20.  Then click on New Search.<p>
You can also search by specific fields. If you want to search all orders made by people with the last name Jones, or living in the state of Florida,  you can. You can do this by selecting the type of field you want to search <b>BY</b>, and enter what you are searching for in the <b>FOR</b> field. Then click New Search. If you want to save the search, the next time you come to the Order Admin page, it will display in this fashion. 
<p>
<font face="verdana,arial" color="#ffffcc" size="1"><a href="$self#top">back
          to the top</a></font><p>
<a name="3"><b>Order Detail</b><br>
Once you click on the order you would like to view, you will come to the <b>ORDER DETAIL</b> page. There are two ways to view this order detail. You can click on <b>VIEW</b> and it will display the order which can not be edited. If you are in view mode, the link at the top will change to <b>UPDATE</b>. When you are in update mode, you can edit the fields by clicking in the text fields and changing information. By clicking <b>DELETE</b>, you will delete the order. By clicking on the arrows at the top of the page, you can move to the next order on your list.  You can select the <b>" view a printer friendly version"</b> and print out your order from this page by choosing PRINT from your browser.  
<p><font face="verdana,arial" color="#ffffcc" size="1"><a href="$self/#top">back
          to the top</a></font><p>
<br></font>
<!--***********-->

</td>
</tr>
</table>
</td></tr></table>
<p>
</body>
</html>
REST
