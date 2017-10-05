#!/usr/bin/perl -w
 
# $Id: options.cgi,v 1.3 2002/03/26 14:36:25 root Exp root $

## universal modules
use strict;
use POSIX qw(strftime);
use Cwd;
#use File::Copy;
use File::NCopy qw(copy);

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
my $domain = (split(/\//, cwd()))[-2];
my $rcs = (qw$Revision: 1.3 $)[-1];
my $images = "controlpanel/images";
$0 = (split(/\//, $0))[-1];
my $self = "controlpanel/$0";

## specific variables for this script

## actions taken based on form input

## counter addition
if ($formdata{add} eq "counter") {
  ## create the lock file to show counter is installed
  open(FH, ">/etc/hosting-options/$domain/counter")
    or die "Cant open counter file for $domain : $!\n";
  close(FH);

  ## read in counter template and and write out to client bin 
  open(FH, "/usr/local/ref/options/counter.cgi")
    or die "Cant open counter.cgi ref file : $!\n";
  open(NH, ">/www/$domain/cgi-bin/counter.cgi")
    or die "Cant open counter.cgi bin file : $!\n";
    while(<FH>) {
      my $line = $_;
      $line =~ s/HOSTING_DOMAIN/$domain/;
      print NH $line
    }
  close(NH);
  close(FH);

  ## make new script executable
  chmod 0755, "/www/$domain/cgi-bin/counter.cgi";

  ## finish creating adjunct files
  open(FH, ">/www/$domain/options/counter.txt")
    or die "Cant open counter.txt file : $!\n";
    print FH "1";
  close(FH);

## banner rotation addition
} elsif ($formdata{add} eq "banner") {
  ## create and lock the file to show banner rotate is installed
  open(FH, ">/etc/hosting-options/$domain/banner")
    or die "Cant open banner file for $domain : $!\n";
  close(FH);

## date addition
} elsif ($formdata{add} eq "date") {
  ## create and lock the file to show date script is installed
  open(FH, ">/etc/hosting-options/$domain/date")
    or die "Cant open date file for $domain : $!\n";
  close(FH);

  ## place new script into cgi-bin
  copy("/usr/local/ref/options/date.cgi","/www/$domain/cgi-bin/");  

  ## chmod to correct permissions
  my $mode = 0700;
  chmod $mode, "/www/$domain/cgi-bin/date.cgi"
    or die "Cant chmod date script for $domain : $!\n";

## time addition
} elsif ($formdata{add} eq "time") {
  ## create and lock the file to show date script is installed
  open(FH, ">/etc/hosting-options/$domain/time")
    or die "Cant open date file for $domain : $!\n";
  close(FH);

  ## place new script into cgi-bin
  copy("/usr/local/ref/options/time.cgi","/www/$domain/cgi-bin/");

  ## chmod to correct permissions
  my $mode = 0700;
  chmod $mode, "/www/$domain/cgi-bin/time.cgi"
    or die "Cant chmod time script for $domain : $!\n";

## search engine addition
} elsif ($formdata{add} eq "search") {
  ## create and lock the file to show search script is installed
  open(FH, ">/etc/hosting-options/$domain/search")
    or die "Cant open search file for $domain : $!\n";
  close(FH);

  ## copy the search directory structure into the options dir
  copy \1,"/usr/local/ref/options/search","/www/$domain/options/";

  ## create a valid conf.pl file
  open(FH, "/www/$domain/options/search/conf.pl")
    or die "Cant open conf.pl : $!\n";
  
  my @config = <FH>;

  close(FH);

  ## write out a new conf.pl file
  open(FH, ">/www/$domain/options/search/conf.pl")
    or die "Cant open conf.pl for writing : $!\n";

  for my $i(@config) {
    $i =~ s/DOMAIN/$domain/;
    print FH $i;
  }

  close(FH);

  ## create a valid search.cgi file
  open(FH, "/usr/local/ref/options/search.cgi")
    or die "Cant open search.cgi for read : $!\n";
  
  my @search = <FH>;

  close(FH);

  ## write out a new search.cgi file
  open(FH, ">/www/$domain/cgi-bin/search.cgi")
    or die "Cant open search.cgi for writing : $!\n";
  
  for my $i(@search) {
    $i =~ s/DOMAIN/$domain/;
    print FH $i;
  }

  close(FH);

  ## assign correct permissions
  my $mode = 0700;
  chmod $mode, "/www/$domain/cgi-bin/search.cgi";

}

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
    <td>

<!-- *********** -->   						              
REST

## script option setup tables

##
## Banner Rotation
##
print <<BANNER;
<!-- banner rotation setup -->

<p>
<table width="450" cellpadding="0" cellspacing="0" border="0">
 <tr>
  <td colspan="2"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>banner-rotation.cgi</b></font></td>
 </tr>
 <tr>
  <td width="5%">&nbsp;</td>
  <td><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2">Use this option to install a utility that allows you to
display a different banner in an area of your website with each new visit. You can display up to four banners in the rotation,
each having its own corresponding url.<p>Once you have your banner rotation script installed, you can add the following code to
any document within your website having .shtml as its suffix.</font>
<p><center><font face="Verdana,Geneva,Arial,Helvetica,sans-seri
f" size="-2">&lt;!--#include virtual="cgi-bin/banner-rotation.cgi"--&gt;</font></center></td>
 </tr>
</table>
BANNER

if (-e "/etc/hosting-options/$domain/banner") {
print <<BANNER;
<p>
<table width="450" cellpadding="0" cellspacing="0" border="0">
 <tr>
  <td align="center"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="#cc3300"><b>This option is installed for your website</b></font><p><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="#
000000">Be sure to </font><a href="https://www.$domain/controlpanel/banner-config.cgi"><font face="Verdana,Geneva,Arial,Helvetica,sa
ns-serif" size="-2" color="#cc3300">configure</font></a> <font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="#00
0000">your script with your specific images!</font></td>
 </tr>
</table>
<p>
BANNER

} else {

print <<BANNER
<p>
<table width="450" cellpadding="0" cellspacing="0" border="0">
 <tr>
  <td align="center"><a href="https://www.$domain/$self?add=banner"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2
" color="#cc3300"><b>Install</b></font></a> <font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="#cc3300"><b>banner-rotation.cgi now!</b></font></td>
 </tr>
</table>
<p>
BANNER

}

## 
## Counter 
##

print <<REST;
<!-- *** text counter setup -->

<table width="450" cellpadding="0" cellspacing="0" border="0">
 <tr>
  <td colspan="2"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>counter.cgi</b></font></td>
 </tr>
 <tr>
  <td width="5%">&nbsp;</td>
  <td><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2">Use this option to install a text counter on your web site's
pages. By selecting this, you will be able to view how many times your site has been visited. Since the counter is text based, you
will be able to modify the text using standard html tags. This will allow you to display it using a myriad of tags, or even hide it
by setting the text color to the same as the background.<p>Once you have your counter installed, you can add the following code to a
ny document within your web site having .shtml for its suffix:</font><p><center><font face="Verdana,Geneva,Arial,Helvetica,sans-seri
f" size="-2">&lt;!--#include virtual="cgi-bin/counter.cgi"--&gt;</font></center></td>
 </tr>
</table>
REST

if (-e "/etc/hosting-options/$domain/counter") {
print <<COUNTER;
<p>
<table width="450" cellpadding="0" cellspacing="0" border="0">
 <tr>
  <td align="center"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="#cc3300"><b>This option is installed for your website</b></font></td>
 </tr>
</table>
<p>
COUNTER

} else {

print <<COUNTER;
<p>
<table width="450" cellpadding="0" cellspacing="0" border="0">
 <tr>
  <td align="center"><a href="https://www.$domain/$self?add=counter"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2
" color="#cc3300"><b>Install</b></font></a> <font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="#cc3300"><b>counter.cgi now!</b></font></td>
 </tr>
</table>
<p>
COUNTER

}


print <<REST;
<!-- *** date setup -->
<table width="450" cellpadding="0" cellspacing="0" border="0">
 <tr>
  <td colspan="2"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>date.cgi</b></font></td>
 </tr>
 <tr>
  <td width="5%">&nbsp;</td>
  <td><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2">Use this script to add the current date to your website. The date format can be in one of a myriad of styles, which can specified within your webpage html. Click <a href="https://www.$domain/controlpanel/date-howto.cgi">here</a> to learn how to choose your format.<p></font></td>
 </tr>
</table>
REST

if (-e "/etc/hosting-options/$domain/date") {
print <<EOT;
<p>
<table width="450" cellpadding="0" cellspacing="0" border="0">
 <tr>
  <td align="center"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="#cc3300"><b>This option is installed for your website</b></font></td>
 </tr>
</table>
<p>
EOT

} else {

print <<EOT;
<p>
<table width="450" cellpadding="0" cellspacing="0" border="0">
 <tr>
  <td align="center"><a href="https://www.$domain/$self?add=date"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2
" color="#cc3300"><b>Install</b></font></a> <font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="#cc3300"><b>
date.cgi now!</b></font></td>
 </tr>
</table>
<p>
EOT

}

#
# FormMail 
#
print <<REST;
<!-- *** formmail setup -->
<table width="450" cellpadding="0" cellspacing="0" border="0">
 <tr>
  <td colspan="2"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>formmail.cgi</b></font></td>
 </tr>
 <tr>
  <td width="5%">&nbsp;</td>
  <td><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2">Use this option to deliver end user input submitted from a form on your website to your e-mail inbox. Click <a href="http://www.lunarhosting.net/tutaddform.htm" target="_new">here</a> for directions on how to use this cgi script.
 </tr>
</table><p>
<table width="450" cellpadding="0" cellspacing="0" border="0">
 <tr>
  <td align="center"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="#cc3300"><b>This option is installed for your website</b></font></td>
 </tr>
</table>
<p>
REST

#
# Search
#
print <<REST;
<!-- *** search setup -->
<table width="450" cellpadding="0" cellspacing="0" border="0">
 <tr>
  <td colspan="2"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>search.cgi</b></font></td>
 </tr>
 <tr>
  <td width="5%">&nbsp;</td>
  <td><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2">Use this script to add a Search Engine to your website. Allow visitors to search through your webpages to find exactly what they are looking for. Search.cgi can be configured with custom results pages to blend in seemlessly with your website.
 </tr>
</table>
<p>
REST

if (-e "/etc/hosting-options/$domain/search") {
print <<EOT;
<p>
<table width="450" cellpadding="0" cellspacing="0" border="0">
 <tr>
<td align="center"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="#cc3300"><b>This option is installed for your website</b></font><p><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="#
000000">Be sure to </font><a href="https://www.$domain/controlpanel/search-howto.cgi"><font face="Verdana,Geneva,Arial,Helvetica,sa
ns-serif" size="-2" color="#cc3300">customize</font></a> <font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="#00
0000">your script settings!</font></td>
 </tr>
</table>
<p>
EOT

} else {

print <<EOT;
<p>
<table width="450" cellpadding="0" cellspacing="0" border="0">
 <tr>
  <td align="center"><a href="https://www.$domain/$self?add=search"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2
" color="#cc3300"><b>Install</b></font></a> <font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="#cc3300"><b>
search.cgi now!</b></font></td>
 </tr>
</table>
<p>
EOT

}

#
# Time
#

print <<REST;
<!-- *** time setup -->
<table width="450" cellpadding="0" cellspacing="0" border="0">
 <tr>
  <td colspan="2"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>time.cgi</b></font></td>
 </tr>
 <tr>
  <td width="5%">&nbsp;</td>
  <td><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2">Use this script to add the current time to your website. The
time format can be in one of a myriad of styles, which can specified within your webpage html. Click <a href="https://www.$domain/co
ntrolpanel/time-howto.cgi">here</a> to learn how to choose your format.<p></font></td>
 </tr>
</table>
<p>
REST

if (-e "/etc/hosting-options/$domain/time") {
print <<EOT;
<p>
<table width="450" cellpadding="0" cellspacing="0" border="0">
 <tr>
  <td align="center"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="#cc3300"><b>This option is installed for your website</b></font></td>
 </tr>
</table>
<p>
EOT

} else {

print <<EOT;
<p>
<table width="450" cellpadding="0" cellspacing="0" border="0">
 <tr>
  <td align="center"><a href="https://www.$domain/$self?add=time"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2
" color="#cc3300"><b>Install</b></font></a> <font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="#cc3300"><b>
time.cgi now!</b></font></td>
 </tr>
</table>
<p>
EOT

}

print <<REST;
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
