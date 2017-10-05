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

<!-- TEMPLATE
&nbsp;&nbsp;&nbsp;<a href="controlpanel/faq/"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-2">QUESTION?</font></a><br>
-->

<!-- QUESTION -->
<font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-1"><b>Q.</b> How do I filter spam from my inbox? </font>

<p> 
<!-- ANSWER -->
<font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#CC3300" size="-1"><b>A.</b> Mail being sent to your account is first processed by a powerful program called SpamAssassin. This application examines the message and tries to determine whether or not it should be considered unsolicited e-mail also known as Spam.<p>
When a message is found to be Spam, the e-mail is re-written with the subject line having "*****SPAM*****" prepended to it. This new pattern will allow you to set up filters in your local mail client so that this mail can be delivered to a seperate folder rather than your inbox.<p>
The capacities for sorting mail varies with each mail client available, however you should be able to set up a rule which tells your application "if the criteria set up within this rule matches this email, then take the following action".<p>
The action defined within a rule can include moving the e-mail to specific folder, deleting the email, playing a sound and more. Please note that if you set your action to delete an e-mail, its gone forever and cannot be retrieved. For filtering spam, we recommend moving e-mail to a new folder outside of your inbox. We suggest calling the folder "SPAM".<p>
Below are instructions for setting up filters on some of the more popular e-mail clients. If yours does not happen to be on the list, you may want to search on your favorite search engine for guides on setting up rules for your application.<p>
<b>Setting up Rules in Outlook Express 5</b><br>

Open Outlook Express.<p>

Under Tools in the menu bar, click Rules.<p>

Click New to create a new rule.<p>

You now have a dialog box which gives you choices for setting up your first rule. Set up your criteria and choose your action(s).<p>

You can have many criteria per rule. Just keep clicking Add Criteria to create new ones.<p>

Click Okay.<p>

<b>Setting up Rules in Outlook 2000 for Windows</b><br>

Open Outlook.<p>

Under Tools in the menu bar, choose Rules Wizard, then click on New to create a new rule.<p>

Click Check messages when they arrive.<p>

Select what to check for when the message arrives. Scroll through the choices and select the one to apply for this rule.<p>

Click Next to specify what to do with the message. Scroll through the choices and select the one to apply for this rule.<p>

Click Next for a screen where you can identify any exceptions.<p>

Click Next, specify a name for the rule and turn the rule on.<p>

<b>Setting up Mail Filters in Eudora</b><br>

Open Eudora.<p>

Under Tools in the menu bar, click on Mail Filter.<p>

Click New.<p>

In the Make Filter dialog box that will pop up, the Match section is where you can enter your criteria for the email you want to filter. You probably want to sort incoming mail, so check Incoming. Choose either "From contains", "Any recipient contains", or "Subject contains" and type in the specific text of what you are trying to filter (for example, check "From contains," and type in "Mom.")<p>

Fill in the Action section of the Make Filter dialog box. You'll probably want to send the filtered mails to a relevantly named mailbox (folder). Move the mouse over the arrow next to None and click. Choose from the list of all the various actions that the filter can do.<p>

You are not limited to one action - you can have your filter perform multiple actions. For example, you can transfer mail to a designated mailbox, and also set it to play a particular sound when mail's been moved there.<p>

Go to File and choose Save to save your changes, or close the Filters window and it will ask you to save your changes.<p>

<b>Setting up Message Filters in Netscape Messenger</b><br>

Open Netscape Messenger.<p>

Under Edit on the menu bar, click Message Filters.<p>

Click New to create a new filter. (This is also the window in which you may edit and delete existing filters, or change the order in which they are applied.)<p>

In the Filter Rules window, type a name for your filter.<p>

Choose the criteria to be used for your filter. Choose Match any of the following or Match all of the following depending on how inclusive you want the filter to be. On the next line, set your criteria.<p>

Choose the action you want to take on any incoming messages that match the filter. For moving them to a folder, you can specify an existing folder or create a new one by clicking New Folder.<p>

If you want, you can add a decription for your filter at the bottom.<p>

Click OK. You will return to the Message Filters window, to create more filters if you wish. When you are finished creating your filters, click OK again.<p>
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
