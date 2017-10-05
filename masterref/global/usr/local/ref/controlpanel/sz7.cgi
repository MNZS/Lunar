#!/usr/bin/perl -w

# $Id: sz7.cgi,v 1.2 2002/03/26 14:23:43 root Exp root $

use strict;
use Cwd;

my $workdir = `pwd`;
my @path = split(/\//, $workdir);
my $domain=$path[2];
my $rcs = (qw$Revision: 1.2 $)[-1];
my $images = "controlpanel/images";

$0 = (split(/\//, $0))[-1];
my $self = "controlpanel/$0";

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
<!-- MAIN TITLE -->
<font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>SHIPPING RATES</b>&nbsp; 
<!-- CATEGORY LINKS -->
<br>
<!-- MAIN BODY -->
By defining your shipping rates, you will establish what amount will be charged to each order. There is more than one way to display shipping rates.  After logging into the Administration page, click on "Store Admin" and then <b>"Shipping Rates"</b> from the menu on the left.
<p><b>NOTE:It is best to discuss adding new payment methods with your web developer to ensure that it is properly set up.</b>
All shipping rates will be displayed on your screen. Click on the shipping rate you wish to modify.
<p>You will see the following displayed:<br>
<b>Name:</b> This is the shipping rate title the user will see. If you have multiple shipping rates, they will need to choose the shipping rate they wish to use. For example, the default is Standard Shipping. You would set up a new shipping rate for FedEx or UPS.  <br>
<b>Description:</b> This is optional, it is just a text description of the option. For instance, you could be FedEx in the name field, and Next Day or 2nd Day in the description.<br>
<b>Shipping Policy:</b>If you want to create a standard "help page" you can do that here. The default is set into this page.<br>
<b>Shipping Charge Per Order:</b> This is where you can add any charges to every order. This will be charged for every order when <i>THIS SPECIFIC SHIPPING</i> is selected. <br>
<b>Options:</b>This is where you can add an additional charge option. For example, if you want to charge an extra amount for delivery to a residence, you would enter the description "Deliver to Residence" and enter the dollar amount in the text box. You can also specify a percent increase here.<br>
<b>Tiered Shipping Charges:</b> This is where you can enter the exact amounts you want to charge based on price, quantity or weight. You can do this in percent or in dollar amounts.  If you need additional assistance in this area, please <a href="mailto:support\@lunarhosting.net"><b>contact us</b></a>, and we will be glad to assist you.
<br>
<a href="$self#top">back
          to the top</a></font><p>                            

   						</td>
   					</tr>
   				</table>
   			</td>
   		</tr>
   	</table>
   </body>
</html>
REST
