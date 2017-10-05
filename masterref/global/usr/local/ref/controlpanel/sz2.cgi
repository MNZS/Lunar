#!/usr/bin/perl -w

# $Id: sz2.cgi,v 1.2 2002/03/26 14:23:43 root Exp root $

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
<font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>DISCUSSION BOARD</b>&nbsp; 
<!-- CATEGORY LINKS -->
<a href="$self#1">Messages/Categories</a> | <a href="$self#2">Read Only</a> | <a href="$self#3">Adding Messages</a>
<br>
<!-- MAIN BODY -->
To view the discussion board administration, login to the administration Web page as described above.
The addition of discussion group to a Web site provides the capability for
viewers to submit topics for discussion, search for topics, and view existing
topics. 
<p>
From the Discussion area, the administrator can modify categories and topics, as well as, prune messages from the current site.<p>
Click Add Category to add categories the viewer can select when creating
a topic.
<a name="1"><p><b>Messages and Categories</b><br></a>
Click Administer Messages and Categories to delete or edit the categories
and messages. After clicking on Administer Messages and Categories the
Delete and Change options are displayed. This is only available to you, the 
regular users are not able to do these tasks. You are now on the "actual" page
and are directly editing the discussion board. That is why the look has changed.<p>Click<b> <b>Delete</b></b> to delete that row’s category or topic.<p>Click <b>Prune</b> to delete messages within a category that are past a certain date, not the category itself.<p>
Click <b><b>Change</b></b> to modify the category or topic.<p><b>WARNING: There is no confirmation when you delete a category or topic. If
you delete a category, all the topics within the category are
automatically deleted.</b><p><font face="verdana,arial" color="#ffffcc" size="1"><a href="$self#top">back
          to the top</a></font><p>
<a name="2"><b>Read Only</b><br>
You can set your category to read only. This prevents the users of your site  from adding subjects to your discussion board. There is a bug in ShopZone. You can click on the <b>change</b> button, and there is a drop down box that says <b>Read Only</b> The drop down box appears empty, however, you can still choose it. You should select the first "area" for YES and the second for NO.  Click on <b>Update</b> to save.  To make sure you have done it correctly go back to the main list (hit <b>refresh</b> if you just hit the back button) to see if Read Only has been added in italics next to your category.<p>
<font face="verdana,arial" color="#ffffcc" size="1"><a href="$self#top">back
          to the top</a></font><p>
<a name="3"><b>Adding Message</b><br>
You can add a message as long as it is not a <b>read only</b> category. If you need to change that, please see the tutorial above.  You can add a message by clicking on the <b>Add a Subject</b> link, or from the actual web site itself. You must fill in all fields for it to go through. You should use info\@yourdomainname.com when you are adding from the store. Your entry will show up as the Administrator.
<p><font face="verdana,arial" color="#ffffcc" size="1"><a href="$self#top">back
          to the top</a></font><p></font>                            

   						</td>
   					</tr>
   				</table>
   			</td>
   		</tr>
   	</table>
   </body>
</html>
REST
