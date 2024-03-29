#!/usr/bin/perl -w
 
# $Id: template.cgi,v 1.2 2002/05/14 11:47:05 root Exp root $

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


<table width="550" border="0" cellspacing="0" cellpadding="0"><tr>
<td><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-1"><b><font color="Black">FTP TUTORIAL USING CUTE FTP 5.0 XP</font></b><p><b>This complimentary tutorial is meant to cover the basics to upload files such as images, PDF and HTML files to your web site using a program called Cute FTP which is one of several FTP programs. We do not support this product other than this tutorial. If you would like for us to upload files for you, please contact us for an estimate. If you have any questions about functionality or installation, please refer to Globalscape's  <a href="http://www.globalscape.com/support/manuals.shtml"><b>Online Manual Section</b></a> web site.</b><p>
</td></tr>
<tr><td><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-1"><b>SET UP</b><br>
<b><font color="Black">1. DOWNLOAD CUTE FTP</font></b><br>
You can do this  from their web site</b> <a href="http://www.globalscape.com"><b>www.globalscape.com</a></b>.
Currently this is under MOVE. Click on the link to <b>Cute FTP</b>, select your language, enter your email address, and click <b>CONTINUE</b>. Fill out the short form.
This program is Shareware, which means you can download and use it, but you are expected to purchase it if you continue to use it after 30 days. You can purchase it from their web site if you choose to buy it. If you want to use another FTP program, that is okay, but the step by step instructions are meant for Cute FTP 5.0 XP program. </p></td></tr><tr><td><p>
<font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-1"><b><font color="Black">2.  INSTALL </b></font><br>
We must assume you know how to install a new program on your computer. Restart your computer if preferred.</p>
<p></td></tr></table>
<table width="550" border="0" cellspacing="0" cellpadding="0"><tr><td><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-1"><font color="Black"><b>3. LAUNCH THE PROGRAM</b></font><br>
Once you start FTP it will ask you for a serial number or to begin your trial, choose one. </p>
<p></td></tr>
<tr><td valign="top"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-1"><font color="Black"><b>4. ENTER WEB SITE NAME:</b></font><br>
A screen will appear:<p>This is where you can type in the name of your web site so you can identify it from any other sites you may be maintaining.  For now, we will call it My Web Site. Click <b>NEXT</b>.</font></td><td>
<div align="center"><img src="$images/ftp1.jpg" alt="" width="288" height="223" border="0"></div></p></td></tr></table>
<p>
<table width="550" border="0" cellspacing="0" cellpadding="0"><tr><td valign="top"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-1"><font color="Black"><b>5.  ENTER HOST ADDRESS:</b></font><br>Enter ftp.$domain here. Click on <b>NEXT</b>.<p></td><td>
<div align="center"><img src="$images/ftp2.jpg" alt="" width="288" height="222" border="0"></div></td></tr></table>
<p>
<table width="550" border="0" cellspacing="0" cellpadding="0"><tr><td valign="top"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-1"><font color="Black"><b>6.  ENTER USER NAME/PASSWORD:</b></font><br><br>
By default, this should be the same user name and password you use to access your control panel unless you have an alternative account set up through us. Enter your user name and password, and click in the box that says "mask password" box if you want to make it more secure.(Recommended) Click <b>NEXT</b>.</td><td><div align="center"><img src="$images/ftp3.jpg" alt="" width="288" height="223" border="0"></div></td></tr></table>
<table width="550" border="0" cellspacing="0" cellpadding="0"><tr><td><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-1"><font color="Black"><b>7.  SKIP THE NEXT SCREEN</b></font><br>Click <b>NEXT.  Click <b>FINISH</b> on the next screen to complete your set up</b>.<p></td></tr>

<tr><td><hr><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-1"><b>FTP</b><br>
1. The first time you set this up, it will automatically connect. The next time you launch the program click on the button that looks like the one below.<p>
<img src="$images/ftp4.jpg" alt="" width="135" height="74" border="0"><p></td></tr>
<tr><td><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-1">2.  A screen will appear(if not go to General FTP Sites until you see My Web Site): Click <b>CONNECT</b>.
<div align="center"><img src="$images/ftp5.jpg" alt="" width="360" height="321" border="0"></div><p>
</p></td></tr>
<tr><td><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-1">3. You should be connected. If you connected correctly, you will see a screen that looks like this:
<img src="$images/ftp6.jpg" alt="" width="504" height="381" border="0"><br>
The left side is your computer files and the right is a list of your web folders and files on the server. By default you should put all images and PDF files in your Public HTML folder. To open a folder simply double click on it. </td></tr></table><p></p>
<table width="550" border="0" cellspacing="0" cellpadding="0">
<tr><td valign="top" width="155"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-1"><b>To move up a directory:</b><br><img src="$images/ftp7.jpg" alt="" width="135" height="63" border="0">
</td><td ><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-1"><b>If you are idle for a while and get disconnected</b>, you can easily reconnect by clicking the reconnect button.<br><img src="$images/ftp8.jpg" alt="" width="135" height="74" border="0"></td></tr></table>
<p></p>
<table width="550" border="0" cellspacing="0" cellpadding="0">
<tr><td valign="top"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-1"><b>4. To upload/download:</b> Make sure you are in the directory you want to upload to and/or download to. You can simply double click the item you want to move to the other side. <p>If you wanted to upload image.gif  from your computer to the server, locate the image so you can see it in the left window. You double click on it, and the file will be uploaded to the directory you are in on the right side. Make sure you are IN the folder you want to be in! You can select multiple files by holding down the CTRL button when you select a file to upload. If you have multiple files, it may be easier to drag the files with your mouse to the other side instead of double clicking to upload. They both will work! <p>

To disconnect, you simply go to<b> FILE- DISCONNECT</b>.</p><br>
</td></tr></table>

</font>


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
