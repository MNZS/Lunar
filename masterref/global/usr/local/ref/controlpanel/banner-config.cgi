#!/usr/bin/perl -w
 
# $Id: banner-config.cgi,v 1.2 2002/03/26 14:23:43 root Exp root $

## universal modules
use strict;
use POSIX qw(strftime);
use Cwd;

## specific modules for this script

## cgi.pm parameters
use CGI;
#use CGI::Carp qw(fatalsToBrowser carpout);
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
my $rcs = (qw$Revision: 1.2 $)[-1];
my $images = "controlpanel/images";
$0 = (split(/\//, $0))[-1];
my $self = "controlpanel/$0";

## specific variables for this script
my %rotate;

## actions taken based on form input
if ($formdata{action} eq "go") {

  ## assign hash structure values
  $rotate{$formdata{image_one}}	 	= $formdata{url_one} 
    if ($formdata{image_one});
  $rotate{$formdata{image_two}} 	= $formdata{url_two} 
    if ($formdata{image_two});
  $rotate{$formdata{image_three}} 	= $formdata{url_three} 
    if ($formdata{image_three});
  $rotate{$formdata{image_four}}	= $formdata{url_four} 
    if ($formdata{image_four});

  ## create the new banner-rotate.cgi script

  ## open template file for creation
  open(FH, "/usr/local/ref/options/banner-rotation.cgi")
    or die "Cant open CGI template file : $!\n";

  ## open destination file for writing
  open(NH, ">/www/$domain/cgi-bin/banner-rotation.cgi")
    or die "Cant open new CGI banner file : $!\n";

  ## start reading the template
  while(<FH>) {

    ## print until the beginning of the dynamic stuff
    print NH if 1../^\#\# START/ and !/^\#\# START/;

  }

  ## close the file
  close(FH);
  
  ## run is used to create array structure
  my $run = "0";

  ## each of the keys and their urls are put into arrays
  for my $i(keys %rotate) {
    print NH "\$mypic\[$run\] = \"$i\";\n";
    print NH "\$myurl\[$run\] = \"$rotate{$i}\";\n\n";
    ++$run
  }

  ## open template file for creation
  open(FH, "/usr/local/ref/options/banner-rotation.cgi")
    or die "Cant open CGI template file : $!\n";

  ## print the rest of the template out
  while(<FH>) {
    print NH if /^\#\# END/..0 and !/^\#\# END/;

  }

  ## close files
  close(FH);
  close(NH);

  ## add appropriate perms to new file
  my $mode = 0700;
  chmod $mode, "/www/$domain/cgi-bin/banner-rotation.cgi";

} elsif (-e "/www/$domain/cgi-bin/banner-rotation.cgi") {
  
  ## open the config file to get the current banner values
  open(FH, "/www/$domain/cgi-bin/banner-rotation.cgi")
    or die "Cant open banner config file : $!\n";

  while(my $line = <FH>) {

    if ($line =~ /^\$mypic\[0\]/) {
      $line =~ s/^\$mypic\[0\] = \"(.*)\"\;$/$1/;
      $formdata{image_one} = $line;

    } elsif ($line =~ /^\$myurl\[0\]/) {
      $line =~ s/^\$myurl\[0\] = \"(.*)\"\;$/$1/;
      $formdata{url_one} = $line;

    } elsif ($line =~ /^\$mypic\[1\]/) {
      $line =~ s/^\$mypic\[1\] = \"(.*)\"\;$/$1/;
      $formdata{image_two} = $line;
  
    } elsif ($line =~ /^\$myurl\[1\]/) {
      $line =~ s/^\$myurl\[1\] = \"(.*)\"\;$/$1/;
      $formdata{url_two} = $line;

    } elsif ($line =~ /^\$mypic\[2\]/) {
      $line =~ s/^\$mypic\[2\] = \"(.*)\"\;$/$1/;
      $formdata{image_three} = $line;

    } elsif ($line =~ /^\$myurl\[2\]/) {
      $line =~ s/^\$myurl\[2\] = \"(.*)\"\;$/$1/;
      $formdata{url_three} = $line;

    } elsif ($line =~ /^\$mypic\[3\]/) {
      $line =~ s/^\$mypic\[3\] = \"(.*)\"\;$/$1/;
      $formdata{image_four} = $line;

    } elsif ($line =~ /^\$myurl\[3\]/) {
      $line =~ s/^\$myurl\[3\] = \"(.*)\"\;$/$1/;
      $formdata{url_four} = $line;

    }

  }

  ## close file
  close(FH);

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
<tr><td align="right"><a href="http://www.lunarhosting.net"><img src="$images/portalogo.gif"  border="0" alt="Lunar Media Inc."></a>&nbsp;<p></td>
</tr>

  <tr>
    <td>
REST

if ($formdata{action} eq "go") {
  print qq|<center><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1" color="#000000"><b>Your changes were accepted!</b></font></center>|;

} else {
  print qq|<center><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1" color="#000000"><b>Your current settings for banner-rotation.cgi</b></font></center>|;

} 

print <<REST;

<!-- *********** -->   						              

<!-- begin form -->
<form method="post" action="https://www.$domain/$self">

<!-- banner one -->
<table width="450" cellspacing="0" cellpadding="0" border="0">
 <tr>
  <td bgcolor="#000000">
   <table width="450" cellspacing="3" cellpadding="0" border="0">
    <tr>
     <td bgcolor="#009999">
      <table width="450" cellspacing="4" cellpadding="2" border="0">
       <tr>
        <td bgcolor="#009999" width="30%"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1" color="#000000"><b>Banner One</b></font></td>
        <td bgcolor="#009999" width="70%"></td>
       </tr>
        <td bgcolor="#99CC99" width="30%"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>Image:</b></font>&nbsp;</td>
        <td bgcolor="#99CC99" width="70%"><input type="text" name="image_one" value="$formdata{image_one}" size="30"></td>
       </tr>
       <tr>
        <td bgcolor="#99CC99" width="30%"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>URL:</b></font>&nbsp;</td>
        <td bgcolor="#99CC99" width="70%"><input type="text" name="url_one" value="$formdata{url_one}" size="30"></td>
       </tr>
      </table>
     </td>
    </tr>
   </table>
  </td>
 </tr>
</table>

<p>

<!-- banner two -->
<table width="450" cellspacing="0" cellpadding="0" border="0">
 <tr>
  <td bgcolor="#000000">
   <table width="450" cellspacing="3" cellpadding="0" border="0">
    <tr>
     <td bgcolor="#009999">
      <table width="450" cellspacing="4" cellpadding="2" border="0">
       <tr>
        <td bgcolor="#009999" width="30%"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1" color="#000000"><b>Banner Two</b></fo
nt></td>
        <td bgcolor="#009999" width="70%"></td>
       </tr>
        <td bgcolor="#99CC99" width="30%"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>Image:</b></font>&nbsp;</td>
        <td bgcolor="#99CC99" width="70%"><input size="30" type="text" value="$formdata{image_two}" name="image_two"></td>
       </tr>
       <tr>
        <td bgcolor="#99CC99" width="30%"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>URL:</b></font>&nbsp;</td>
        <td bgcolor="#99CC99" width="70%"><input size="30" type="text" value="$formdata{url_two}" name="url_two"></td>
       </tr>
      </table>
     </td>
    </tr>
   </table>
  </td>
 </tr>
</table>

<p>

<!-- banner three -->
<table width="450" cellspacing="0" cellpadding="0" border="0">
 <tr>
  <td bgcolor="#000000">
   <table width="450" cellspacing="3" cellpadding="0" border="0">
    <tr>
     <td bgcolor="#009999">
      <table width="450" cellspacing="4" cellpadding="2" border="0">
       <tr>
        <td bgcolor="#009999" width="30%"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1" color="#000000"><b>Banner Three</b></fo
nt></td>
        <td bgcolor="#009999" width="70%"></td>
       </tr>
        <td bgcolor="#99CC99" width="30%"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>Image:</b></font>&nbsp;</td>
        <td bgcolor="#99CC99" width="70%"><input size="30" type="text" value="$formdata{image_three}" name="image_three"></td>
       </tr>
       <tr>
        <td bgcolor="#99CC99" width="30%"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>URL:</b></font>&nbsp;</td>
        <td bgcolor="#99CC99" width="70%"><input size="30" type="text" value="$formdata{url_three}" name="url_three"></td>
       </tr>
      </table>
     </td>
    </tr>
   </table>
  </td>
 </tr>
</table>

<p>

<!-- banner four -->
<table width="450" cellspacing="0" cellpadding="0" border="0">
 <tr>
  <td bgcolor="#000000">
   <table width="450" cellspacing="3" cellpadding="0" border="0">
    <tr>
     <td bgcolor="#009999">
      <table width="450" cellspacing="4" cellpadding="2" border="0">
       <tr>
        <td bgcolor="#009999" width="30%"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1" color="#000000"><b>Banner Four</b></fo
nt></td>
        <td bgcolor="#009999" width="70%"></td>
       </tr>
        <td bgcolor="#99CC99" width="30%"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>Image:</b></font>&nbsp;</td>
        <td bgcolor="#99CC99" width="70%"><input size="30" type="text" value="$formdata{image_four}" name="image_four"></td>
       </tr>
       <tr>
        <td bgcolor="#99CC99" width="30%"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>URL:</b></font>&nbsp;</td>
        <td bgcolor="#99CC99" width="70%"><input size="30" type="text" value="$formdata{url_four}" name="url_four"></td>
       </tr>
      </table>
     </td>
    </tr>
   </table>
  </td>
 </tr>
</table>

<p>

<input type="hidden" name="action" value="go">

<!-- submit button -->
<table width="450" cellspacing="0" cellpadding="0" border="0">
 <tr>
  <td align="center"><input type="image" src="https://www.$domain/$images/submitbutton.gif" value="submit"></td>
 </tr>
</table>

<!-- end of form -->
</form>

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
