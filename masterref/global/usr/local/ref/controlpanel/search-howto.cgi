#!/usr/bin/perl -w
 
# $Id: search-howto.cgi,v 1.2 2002/03/26 14:23:43 root Exp root $

## universal modules
use strict;
use POSIX qw(strftime);
use Cwd;
use Fcntl ':flock';
use File::Copy;

## specific modules for this script

## cgi.pm parameters
use CGI;
#use CGI::Carp qw(fatalsToBrowser carpout);
$CGI::DISABLE_UPLOADS = 0;
#$CGI::POST_MAX = 24000;
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
my $rcs = (qw$Revision: 1.2 $)[-1];
my $images = "controlpanel/images";
$0 = (split(/\//, $0))[-1];
my $self = "controlpanel/$0";

## specific variables for this script
my $error;


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
<tr><td align="right"><a href="http://www.lunarhosting.net"><img src="$images/portalogo.gif"  border="0" alt="L
unar Media Inc."></a>&nbsp;<p></td>
</tr>

  <tr>
    <td>
<!-- *********** -->   						              
REST

## error statements
if ($error) {
  print qq|<p><font color="#cc3300" face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>I am sorry, but only HTML files under 10K in size are supported.<br>Please try uploading another file to update your templates.</b></font><p>|;

} elsif (!$error && ($formdata{mod} eq "on")) {
  print qq|<p><font color="#cc3300" face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>Your template was updated!</b></font><p>|;

}

print <<REST;
<font face=Verdana,Geneva,Arial,Helvetica,sans-serif color="#000000" size="-1"><b>What is Searchable?</b></font><br>
<font face=Verdana,Geneva,Arial,Helvetica,sans-serif color="#000000" size="-1">By default, this script will index all files ending in .htm, .html and .shtml in your /public_html/ directory and all of its subdirectories. The indexing will occur once a day at 4am U.S. Central Timezone. Any changes made to your pages, or any new pages added during the course of the day will not show up in any searches until the following day. If there is an immediate need to update your search engine, please send an email making the request to <a href="mailto:support\@lunarhosting.net"><b>support\@lunarhosting.net</b></a>.</font>

<p>

<font face=Verdana,Geneva,Arial,Helvetica,sans-serif color="#000000" size="-1"><b>Adding a Search Box to your Website</b></font><br>
<font face=Verdana,Geneva,Arial,Helvetica,sans-serif color="#000000" size="-1">To create the html form used by visitors to submit queries to your search engine, you can add the following html to any of your website's pages:<p></font>
<font face=Verdana,Geneva,Arial,Helvetica,sans-serif color="#000000" size="-2">
&lt;FORM method="GET" action="http://www.$domain/cgi-bin/search.cgi"&gt;<br>
&lt;INPUT type="hidden" name="p" value="1"&gt;<br>                                                                                  
&lt;INPUT type="hidden" name="lang" value="en"&gt;<br>                                                                              
&lt;INPUT type="text" name="q"&gt;<br>                                                                                              
&lt;INPUT type="submit" value="Search"&gt;<br>                                                                                      
&lt;/FORM&gt;<br>
</font>

<p>
<font face=Verdana,Geneva,Arial,Helvetica,sans-serif color="#000000" size="-1"><b>Creating Custom Results Pages</b></font><br>
<font face=Verdana,Geneva,Arial,Helvetica,sans-serif color="#000000" size="-1">Search.cgi has two templates which are available for customization. Each allows you to individualize the look of the results page from a search. The first template allows you to change the format of the page resulting from a search which provided no matches, the second, when matches were found.<br>
A default after page is provided when search.cgi is installed. It is recommended that you use these default pages become accustomed to how the templates are set up and how the special tags within the html coding is used to create the search results.<p>

You can download each of the templates for customization from the following links:<p>

&nbsp;&nbsp;&nbsp;- <a href="https://www.$domain/controlpanel/match.html"><font face=Verdana,Geneva,Arial,Helvetica,sans-serif color="#000000" size="-1"><b>match.html</b></font></a><br>
&nbsp;&nbsp;&nbsp;- <a href="https://www.$domain/controlpanel/no_match.html"><font face=Verdana,Geneva,Arial,Helvetica,sans-serif color
="#000000" size="-1"><b>no_match.html</b></font></a><p>

To update your search engine with your customized match.html and no_match.html templates, simply FTP the new files to your website and place them in the directory called "search". 

          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>

</body>
</html>
REST

sub upload_image {

  ## declare a max size for the uploaded file
  my $max_length = "10000";

  ## pull the file in a variable
  my $fh = $query->upload('upload');

  ## determine current file's length
  my $length;
  while (<$fh>) {
    $length += length($_);
  }

  ## take action based on type
  if (($length < $max_length) && ($fh =~ /.html?$/i)) {
    
    ## hash of file names to write to
    my %destination = ( 'match' => "match.html", 'no_match' => "no_match.html");

    ## open the file to be written
    open(HTML, ">/www/$domain/options/search/templates/$destination{$formdata{filename}}")
      or die "Cant open HTML file for writing : $!\n";

    ## if file is smaller than the max_length print contents to the correct html file. 
    while(<$fh>) {
      print HTML "$_\n"; 
    }
 
    close(HTML); 

  ## otherwise set error for later notification within html
  } else {

    $error = "on";

  }

}
