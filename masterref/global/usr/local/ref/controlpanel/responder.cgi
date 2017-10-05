#!/usr/bin/perl -w
 
# $Id: responder.cgi,v 1.2 2002/03/26 14:23:43 root Exp root $

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

if ($formdata{del} eq "on") {
  delete_data();

} elsif ($formdata{mod} eq "on") {
  &modify();

} elsif ($formdata{change} eq "on") {
  &execute();

} elsif ($formdata{new} eq "on") {
  &make_table();

} else {
  &list_current;

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

## subroutines

## list existing autoresponders
sub list_current {

## variables to create alternating table bgcolors
my $count="1";
my @bgcolor = ("junk", "#99CC99", "#009999");

## array of configured autoresponders
my @ar_addrs;

## create our table
print <<REST;
<!-- First table to set border color -->
<table width="600" cellspacing="0" cellpadding="0" border="0">
 <tr>
  <td bgcolor="#000000">
   <table width=600 border="0" cellspacing="2" cellpadding="5">
    <tr>
     <td bgcolor="#000000"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#FFFF99" size="-1"><b>Your current list of Autoresponders:<b></font></td>
    </tr>
REST

  ##first open the virtuser include file for the domain
  open(FH, "/etc/mail/include/virtuser/virt.$domain");
  flock(FH,2);
  seek(FH,0,0);
  while(<FH>) {
    ##stick the value into an array if its determined to be an autoresponder
    ##we take only the first portion of the file since the latter half is the destination
    push @ar_addrs, (split(/\t/, $_))[0]
      if (/auto\-/);
  }
  ## unlock the file
  flock(FH,8);
  ## close the file
  close(FH);

  if ($#ar_addrs < 0) {
    print qq|<tr><td bgcolor="$bgcolor[$count]"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>There are currently no auto-responders configured.</b></font></td></tr>\n|;
  
  } else {
    for my $i(sort @ar_addrs) {
      print qq|<tr><td bgcolor="$bgcolor[$count]" valign="bottom" width="75%"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>$i</b></font>&nbsp;&nbsp;&nbsp;<a href="https://www.$domain/$self?mod=on&responder=$i"><img src="https://www.$domain/$images/edit.gif" border="0"></a>&nbsp;&nbsp;&nbsp;<a href="https://www.$domain/$self?del=on&responder=$i"><img src="$images/delete.gif" border="0"></a></td></tr>\n|;
      if ($count > 1) { $count-- } else { $count++ }
    }
  }

print <<REST;
   </table>
  </td>
 </tr>
</table>
<p>
<center><a href="https://www.$domain/$self?new=on"><img src="$images/add.gif" border="0"></a></center>
REST
}

## edit autoresponder
sub modify {

## declare variables as a hash
my %args = %formdata;


## our files have the same naming structure as the alias, but the @
## is replaced with a .
$args{responderedited} = $args{responder};
$args{responderedited} =~ s/\@/\./g;

## the responder itself is the entire email address however we also
## need to pull just the email value minus the domain name
$args{responderuser} = (split(/\@/, $args{responder}))[0];

## set the name of our textfile holding the canned response
$args{text} = $args{responderedited}. "-txt";

## grab the additional recepients from the alias include file
open(FH, "/etc/mail/include/aliases/alias.$domain")
  or die "Cant open alias include file : $!\n";
## lock the file
flock(FH,2);
## seek
seek(FH,0,0);

while(<FH>) {
  ## skip until the line includes the alias we want
  next unless /^auto\-$args{responderuser}/;
  if (/\,/) {
    ## the extra recipients are comma seperated. the most we allow are two destinations
    my @rec = split(/\,/, $_);
    $args{recipient_one} = (split(/\@/,$rec[1]))[0];
    $args{recipient_two} = (split(/\@/,$rec[2]))[0];
  }
}
## unlock file
flock(FH,8);

close(FH);

## open the script file and pull out the existing configured fields
open(FH, "/usr/local/autoresponders/$args{responderedited}")
  or die "Cant open the script file : $!\n";
## lock file
flock(FH,2);
seek(FH,0,0);

while(<FH>) {
  if (/--from/) {
    ## here we grab the line with the email addr and strip is down to just the address
    ## itself removing even the domain and @ symbol
    $args{email} = $_;
    $args{email} =~ s/^--from\t//g;
    $args{email} =~ s/\t\\//g;
    $args{email} = (split(/\@/, $args{email}))[0];

  } elsif (/--subject/) {
    ## here we grab the subject line and strip it down to just what is between the quotes
    $args{subject} = $_;
    $args{subject} =~ s/--subject\t//g;
    $args{subject} =~ s/\t\\//g;
    $args{subject} =~ s/\"//g;
  }
}

flock(FH,8);
close(FH);

## pass gathered information on to the table creation routine
&make_table(\%args);

}

sub make_table {
my $args = shift;

## print out the error fields if required
if ($args->{error}) {
  my %errorphrase =	( "responder_syntax"	=> "E-mail addresses should not contain the \@ symbol.",
			  "duplicate"		=> "To: and From: fields should not match!",
			  "missing"		=> "Only the Valid Recipient fields are optional<br>Please ensure that all others have been completed.",
			);

  print qq|<font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1" color="#cc3300"><b>$errorphrase{$args->{error}}</b></font><p>|;

}

## print out the new html table with retrieved info in editable fields
print <<REST;
<!-- First table to set border color -->
<table width="600" cellspacing="0" cellpadding="0" border="0">
 <tr>
  <td bgcolor="#000000" width="600">
   <table width="600" border="0" cellspacing="2" cellpadding="5">
REST

## create the form
print qq|<form method="post" action="https://www.$domain/$self">|;

## header for the table
if ($formdata{new} eq "on") {
  print qq|<tr><td colspan="2"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#FFFF99" size="-1"><b>Autoresponder Address</b></font>&nbsp;<A HREF="javascript:parent.startndnav('https://www.$domain/controlpanel/responder-howto.htm')"><img src="$images/question.jpg"></a></td></tr>\n|;
  print qq|<tr><td bgcolor="#99CC99" width="20%"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#000000" size="-1"><b>To:</b></font></td><td bgcolor="#99CC99" width="80%"><input type="text" maxlength="32" size="20" name="responderuser" value="$args->{responderuser}">&nbsp;<font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#000000" size="-1"><b>\@$domain</b></font></td></tr></table></td></tr></table><p>\n|;

} else {
  print qq|<tr><td colspan="2"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#FFFF99" size="-1"><b>Current configuration for "$args->{responderuser}\@$domain"</b></font></td></tr></table></td></tr></table><p>\n|;
  print qq|<input type=hidden name="responderuser" value="$args->{responderuser}">\n|;

}

## second table for mail parameters
print <<REST;
<table width="600" cellspacing="0" cellpadding="0" border="0">
 <tr>
  <td bgcolor="#000000">
   <table width="600" border="0" cellspacing="2" cellpadding="5">
REST

## table header
print qq|<tr><td bgcolor="#000000" colspan="2"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#FFFF99" size="-1"><b>Return Mail</b>&nbsp;<A HREF="javascript:parent.startndnav('https://www.$domain/controlpanel/responder-howto.htm')"><img src="$images/question.jpg"></a></font></td></tr>\n|;

## specify the from field
print qq|<tr><td bgcolor="#99CC99" width="20%"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#000000" size="-1"><b>From:</b></font></td><td bgcolor="#99CC99" width="80%"><input length="20" maxlength="32" value="$args->{email}" type="text" name="email">&nbsp;<font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#000000" size="-1"><b>\@$domain</b></font></td></tr>\n|;

## specify the subject field
print qq|<tr><td bgcolor="#99CC99" width="20%"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#000000" size="-1"><b>Subject:</b></font></td><td bgcolor="#99CC99" width="80%"><input type="text" size="50" maxlength="60" value="$args->{subject}" name="subject"></td></tr>\n|;

## specify the body of text for the return email
open(FH, "/usr/local/autoresponders/$args->{text}")
  or die "Cant open Message Text file. : $!\n";

flock(FH,2);
seek(FH,0,0);

print qq|<tr><td bgcolor="#99CC99" colspan="2"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#000000" size="-1"><b>Message:</b><p><textarea cols="60" rows="20" name="text_body" maxlength="800">|;

## testing for troubleshooting
print "$args->{text_body}";

## print out the return email text
while(<FH>) {
  print;
}

flock(FH,8);
close(FH);

print qq|</textarea></font></td></tr></table></td></tr></table><p>\n|;

## third table
print <<REST;
<table width="600" cellspacing="0" cellpadding="0" border="0">
 <tr>
  <td bgcolor="#000000" width="600">
   <table width="600" border="0" cellspacing="2" cellpadding="5">
REST

## configure valid recipients
print qq|<tr><td bgcolor="#000000" colspan="2"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#FFFF99" size="-1"><b>Valid Recipients (optional)</b></font>&nbsp;<A HREF="javascript:parent.startndnav('https://www.$domain/controlpanel/responder-howto.htm')"><img src="$images/question.jpg"></a></td></tr>\n|;

## recipient one
print qq|<tr><td bgcolor="#99CC99" width="20%"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#000000" size="-1"><b>First<br>Recipient:</b></font></td><td bgcolor="#99CC99" width="80%"><input maxlength="32" type="text" size="20" name="recipient_one" value="$args->{recipient_one}">&nbsp;<font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#000000" size="-1"><b>\@$domain</b></font></td></tr>\n|;

## recipient two
print qq|<tr><td bgcolor="#99CC99" width="20%"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#000000" size="-1"><b>Second<br>Recipient:</b></font></td><td bgcolor="#99CC99" width="80%"><input type="text" maxlength="32" size="20" name="recipient_two" value="$args->{recipient_two}">&nbsp;<font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#000000" size="-1"><b>\@$domain</b></font></td></tr>\n|;

## end of table
print qq|</table></td></tr></table><p>\n|;

## create the hidden tag that will signal a change to be made
print qq|<input type="hidden" name="change" value="on">\n|;

## submit the form
print qq|<table width="600" cellpadding="0" cellspacing="0" border="0">\n|;
print qq|<tr><td width="100%" background="$images/yellowswatch.jpg" align="center"><input type="image" value="Submit" border="0" src="$images/submitbutton.gif"></td></tr></form>|;
print qq|</table>\n|;

print <<REST;
   </table>
  </td>
 </tr>
</table>
REST


}

## make the requested changes
sub execute {
  ## move %formdata into %args for passing to other subroutines
  my %args = %formdata;

  ## test to verify that no submitted email address have @
  if ( !$args{responderuser}   	||
       !$args{email}       	||
       !$args{text_body}   	||
       !$args{subject}     	) {

       $args{error} = "missing";
       $formdata{new} = "on";
       &make_table(\%args);

  ## ensure that we do not have any missing required fields
  } elsif ( $args{responderuser}	=~ /\@/ ||
            $args{email} 		=~ /\@/	||
            $args{recipient_one} 	=~ /\@/ ||
            $args{recipient_two}	=~ /\@/ ) {
    
            $args{error} = "responder_syntax";

            ## needs to be set in order for top table to have editable field
            $formdata{new} = "on";

	    ## pass the existing %formdata args back to table to correct errors
            &make_table(\%args);
  
  ## ensure that the To: and From: fields do not match
  } elsif ($args{responderuser} eq $args{email}) {

              $args{error} = "duplicate";
              $formdata{new} = "on";
              &make_table(\%args);

  ## make the requested changes
  } else {

    $args{responderuser} =~ s/ //g;
    $args{email} =~ s/ //g;
    $args{recipient_one} =~ s/ //g;
    $args{recipient_two} =~ s/ //g;

    my $virtfile = "/etc/mail/include/virtuser/virt.$domain";
    my $virttmp  = "/etc/mail/include/virtuser/virt.$domain.tmp";
    my $aliasfile = "/etc/mail/include/aliases/alias.$domain";
    my $aliastmp = "/etc/mail/include/aliases/alias.$domain.tmp";

    ## open the current list of virtusers
    open(FH, $virtfile)
      or die "Cant open VirtUser file : $!\n";
    flock(FH,2);
    seek(FH,0,0);
    
    ## put list of virtusers into array
    my @virtusers = <FH>;
  
    ## close file
    flock(FH,8);
    close(FH);

    ## open the tmp virtuser
    open(FH, ">$virttmp")
      or die "Cant open temp virtuser file : $!\n";
    flock(FH,2);
    seek(FH,0,2);

    ## write new info to tmp file 
    for my $i(@virtusers) {
       print FH $i
         if ($i !~ /^$args{responderuser}\@$domain/);
    }
 
    ## add new virtuser to tmp file
    print FH "$args{responderuser}\@$domain\tauto-$args{responderuser}\.$domain\n";

    ## close the tmpfile
    flock(FH,8);
    close(FH);

    ## sort the new list of virtusers
    open(FH, $virttmp);
    flock(FH,2);
    seek(FH,0,0);
    
    @virtusers = <FH>;

    flock(FH,8);
    close(FH);

    open(FH, ">$virttmp");
    flock(FH,2);
    seek(FH,0,2);

    print FH (sort @virtusers);

    flock(FH,8);
    close(FH);

    ## this is where the file gets moved into place
    move($virttmp, $virtfile);

    ## open the current alias file
    open(FH, $aliasfile)
      or die "Cant open Alias file : $!\n";
    flock(FH,2);
    seek(FH,0,0);

    ## put list of aliases into array
    my @aliases = <FH>;

    ## close file
    flock(FH,8);
    close(FH);

    ## open the tmp alias file
    open(FH, ">$aliastmp")
      or die "Cant open temp alias file : $!\n";
    flock(FH,2);
    seek(FH,0,2);

    ## write the current info into the tmp file
    for my $i(@aliases) {
      print FH $i 
        if ($i !~ /^auto\-$args{responderuser}\.$domain/);
    }

    ## add the new alias to the tmp file
    if ($args{recipient_one} && $args{recipient_two}) {
      print FH "auto\-$args{responderuser}\.$domain:\t\"|\/usr\/local\/autoresponders\/$args{responderuser}\.$domain\",$args{recipient_one}\@$domain,$args{recipient_two}\@$domain\n";

    } elsif ($args{recipient_one}) {
      print FH "auto\-$args{responderuser}\.$domain:\t\"|\/usr\/local\/autoresponders\/$args{responderuser}\.$domain\",$args{recipient_one}\@$domain\n";

    } elsif ($args{recipient_two}) {
      print FH "auto\-$args{responderuser}\.$domain:\t\"|\/usr\/local\/autoresponders\/$args{responderuser}\.$domain\",$args{recipient_two}\@$domain\n";

    } else {
      print FH "auto\-$args{responderuser}\.$domain:\t\"|\/usr\/local\/autoresponders\/$args{responderuser}\.$domain\"\n";

    }

    flock(FH,8);
    close(FH);

    ## sort the temp alias file
    open(FH, $aliastmp);
    flock(FH,2);
    seek(FH,0,0);

    @aliases = <FH>;
 
    flock(FH,8);
    close(FH);

    open(FH, ">$aliastmp");
    flock(FH,2);
    seek(FH,0,2);

    print FH (sort @aliases);

    flock(FH,8);
    close(FH);

    ## this is where the file gets moved into place
    move($aliastmp, $aliasfile);

    ## this is where the script body_text file gets written
    open(FH, ">/usr/local/autoresponders/$args{responderuser}\.$domain\-txt");
    flock(FH,2);
    seek(FH,0,2);

    print FH $args{text_body};

    flock(FH,8);
    close(FH);

    ## this is where the bash script gets written

    ## open the template
    open(FH, "/usr/local/ref/autoresponders/template.txt");
    flock(FH,2);
    seek(FH,0,0);

    ## open the new script for writing
    open(SH, ">/usr/local/autoresponders/$args{responderuser}\.$domain");
    flock(SH,2);
    seek(SH,0,2);

    ## print the template into the new script replacing TAGs with valid info
    while(my $i = <FH>) {
      $i =~ s/FROM/$args{email}\@$domain/;
      $i =~ s/RESPONDER/$args{responderuser}\@$domain/;
      $i =~ s/SUBJECT/$args{subject}/;
      $i =~ s/TEXTFILE/$args{responderuser}\.$domain\-txt/;
      print SH $i;
    }

    ## close the files
    flock(FH,8);
    close(FH);
    flock(FH,8);
    close(SH);

    ## make sure the file has execute permissions
    my $mode = 0755;
    chmod $mode, "/usr/local/autoresponders/$args{responderuser}\.$domain";

    ## create the symbolic link needed by smrsh
    symlink "/usr/local/autoresponders/$args{responderuser}\.$domain","/etc/smrsh/$args{responderuser}\.$domain";

    ## show the new list of configured autoresponders
    &list_current;

  }

}

sub delete_data {
my %args = %formdata;

  ## remove @ and replace with .
  $args{responderedited} = $args{responder};
  $args{responderedited} =~ s/\@/\./g;

  ## changed files
  my $virtfile = "/etc/mail/include/virtuser/virt.$domain";
  my $virttmp  = "/etc/mail/include/virtuser/virt.$domain.tmp";
  my $aliasfile = "/etc/mail/include/aliases/alias.$domain";
  my $aliastmp = "/etc/mail/include/aliases/alias.$domain.tmp";
  my $scriptfile = "/usr/local/autoresponders/$args{responderedited}";
  my $symlink = "/etc/smrsh/$args{responderedited}";
  my $textfile = $scriptfile . "-txt";

  ## clean up the virtuser table

  ## read in current virtuser
  open(FH, $virtfile)
    or die "Cant open virtuser file : $!\n";
  flock(FH,2);
  seek(FH,0,0);

  my @virtusers = <FH>;

  flock(FH,8);
  close(FH);

  ## print out temp virtuser file removing the deleted autoresponder
  open(TF, ">$virttmp")
    or die "Cant open temp virtuser file : $!\n";
  flock(SH,2);
  seek(SH,0,2);

  for my $i( sort @virtusers) {
    next if ($i =~ /^$args{responder}/);
    print TF $i;
  }

  flock(TF,8);
  close(TF);

  ## move the new file into place
  move($virttmp,$virtfile);

  ## clean up the alias file

  ## read in current alias file
  open(FH, $aliasfile)
    or die "Cant open aliases : $!\n";
  flock(FH,2);
  seek(FH,0,0);

  my @aliases = <FH>;

  flock(FH,8);
  close(FH);

  ## print out temp alias file removing the deleted autoresponder
  open(TF, ">$aliastmp")
    or die "Cant open temp alias file : $!\n";
  flock(SH,2);
  seek(SH,0,2);

  for my $i(sort @aliases) {
    next if ($i =~ /^auto-$args{responderedited}/);
    print TF $i;
  }

  flock(TF,8);
  close(TF);

  ## move new file into place
  move($aliastmp, $aliasfile);

  ## remove the script and text body files
  unlink($scriptfile)
    or warn "Cant remove scriptfile : $scriptfile : $!\n";
  unlink($textfile)
    or warn "Cant remove textfile : $textfile : $!\n";
  unlink($symlink)
    or warn "Cant remove symlink : $symlink : $!\n";

  ## list the current autoresponders
  &list_current(\%args);

}
