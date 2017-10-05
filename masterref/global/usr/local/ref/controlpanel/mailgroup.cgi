#!/usr/bin/perl -w
 
# $Id: mailgroup.cgi,v 1.2 2002/03/26 14:23:43 root Exp root $

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
<tr><td align="right"><a href="http://www.lunarhosting.net"><img src="$images/portalogo.gif"  border="0" alt="L
unar Media Inc."></a>&nbsp;<p></td>
</tr>

  <tr>
    <td>
<!-- *********** -->   						              
REST

if ($formdata{new} eq "on") {
  &make_new;

} elsif ($formdata{del_addr} eq "on") {
  &delete_addr;

} elsif ($formdata{del_group} eq "on") {
  &delete_group;

} elsif (($formdata{editgroup} eq "on") || ($formdata{mod} eq "on")) {
  &edit_group(\%formdata);

} elsif ($formdata{makefiles} eq "on") {
  &make_files;

} else {
  ## show our current grouping
  &group_current;

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

sub group_current {

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
     <td bgcolor="#000000"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#FFFF99" size="-1"><b>Your Current  
Mailing Groups:<b></font></td>
    </tr>
REST

  ##first open the virtuser include file for the domain
  open(FH, "/etc/mail/include/virtuser/virt.$domain")
    or die "Cant open virtuser file : $!\n";
  flock(FH,2);
  seek(FH,0,0);
  while(<FH>) {
    ##stick the value into an array if its determined to be an autoresponder
    ##we take only the first portion of the file since the latter half is the destination
    push @ar_addrs, (split(/\t/, $_))[0]
      if (/group\-/);
  }
  ## unlock the file
  flock(FH,8);
  ## close the file
  close(FH);

  if ($#ar_addrs < 0) {
    print qq|<tr><td bgcolor="$bgcolor[$count]"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>There are currently no mailing groups configured.</b></font></td></tr>\n|;
  
  } else {
    for my $i(sort @ar_addrs) {
      my $name = "$i";
      $name =~ s/\@.*//;
      print qq|<tr><td bgcolor="$bgcolor[$count]" valign="middle" width="75%"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif"
 size="-1"><b>$i</b></font>&nbsp;&nbsp;&nbsp;<a href="https://www.$domain/$self?mod=on&groupname=$name"><img src="https://www.$domain/$images/edit.gif" border="0"></a>&nbsp;&nbsp;&nbsp;<a href="https://www.$domain/$self?del_group=on&groupname=$name"><img src="$images/delete.gif" border="0"></a></td></tr>\n|;
      if ($count > 1) { $count-- } else { $count++ }
    }
  }

## end of table
print <<REST;
   </table>
  </td>
 </tr>
</table>
<p>
<center><a href="https://www.$domain/$self?new=on"><img src="$images/addgroup.gif" border="0"></a></center>
REST

## end of subroutine
}

sub make_new { 
my $args = shift;

## error notification
my %err = (	"format" 	=> "The mailing group format should not include the \@ symbol.",
                "toomany"	=> "You have reached your maximum number of allowed mailing groups." );

print qq|<font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1" color="#cc3300"><b>$err{$args->{error}}</b></font><p>|
  if ($args->{error});

## beginning of form
print qq|<form action="https://www.$domain/$self" method="post">\n|;

## print out the new html table
print <<REST;
<!-- First table to set border color -->
<table width="450" cellspacing="0" cellpadding="0" border="0">
 <tr>
  <td bgcolor="#000000" width="450">
   <table width="450" border="0" cellspacing="2" cellpadding="5">
REST

## first table header
print qq|<tr><td bgcolor="#000000"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#FFFF99" size="-1"><b>Add a Mailing Group</b></font>&nbsp;&nbsp;<A HREF="javascript:parent.startndnav('https://www.$domain/controlpanel/mailgroup-howto.htm')"><img src="$images/question.jpg"></a></td></tr>|;

## for a new group
print qq|<tr><td bgcolor="#99CC99"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#000000" size="-1"><b>To:&nbsp;&nbsp;<input type=text maxlength="20" size="20" value="$args->{groupname}" name="groupname">&nbsp;\@$domain</b></font></td></tr>|;

## end of first table
print qq|</table></td></tr></table><p>|;

## field to key addition of group
print qq|<input type="hidden" name="makefiles" value="on">\n|;

## submit
print qq|<table cellpadding="0" cellspacing="0" border="0" width="400"><tr><td>|;
print qq|<center><input type="image" value="Submit" border="0" src="$images/submitbutton.gif"></center>|;
print qq|</td></tr></table>|;

## end of form
</form>

## end of subroutine
}

sub make_files {
my %args = %formdata;

  ## clean up the user input
  $args{groupname} =~ s/ //g;

  chomp $args{groupname};

  ## error checking
  if ($args{groupname} =~ /\@/) {
    $args{error} = "format";
    &make_new(\%args);

  ## if no errors add new
  } else {

    ## add the new entry to the virtuser file

    my $virtfile = "/etc/mail/include/virtuser/virt.$domain";
    my $virttmp = "/etc/mail/include/virtuser/virt.$domain.tmp";

    open(FH, $virtfile)
      or die "Cant open virt file : $virtfile : for reading : $!\n";
  
    open(TF, ">$virttmp")
      or die "Cant open temp virt file for writing : $!\n";

    my @virtusers = <FH>;

    for my $i(@virtusers) {
      next if ( $i =~ /^$args{groupname}\@$domain/);
      print TF $i;
    }

    print TF "$args{groupname}\@$domain\tgroup\-$args{groupname}\.$domain\n";

    close(TF);
    close(FH);

    open(FH, $virttmp)
      or die "Cant open temp virt file for reading : $!\n";

    @virtusers = <FH>;

    close(FH);

    open(FH, ">$virttmp")
    or die "Cant open temp virt file for writing final group : $!\n";

    print FH (sort @virtusers);

    close(FH);

    move($virttmp, $virtfile);

    ## add the new entry to the alias file

    my $aliasfile = "/etc/mail/include/aliases/alias.$domain";
    my $aliastmp = "/etc/mail/include/aliases/alias.$domain.tmp";

    open(FH, $aliasfile)
      or die "Cant open the alias file : $!\n";

    open(TF, ">$aliastmp")
      or die "Cant open the temp alias file : $!\n";

    my @aliases = <FH>;

    for my $i(@aliases) {
      next if ( $i =~ /^group\-$args{groupname}\./);
      print TF $i;
    }

    print TF "group-$args{groupname}\.$domain:\t:include:\t\/etc\/mail\/include\/groups\/$args{groupname}\.$domain\n";

    close(TF);
    close(FH);

    open(FH, $aliastmp)
      or die "Cant open the temp alias file : $!\n";

    @aliases = <FH>;

    close(FH);

    open(FH, ">$aliastmp")
      or die "Cant open the temp alias file : $!\n";

    print FH (sort @aliases);

    close(FH);

    move($aliastmp, $aliasfile);

    ## if the group file does not exist, create it
    if (!-e "/etc/mail/include/groups/$args{groupname}\.$domain") {
      open(FH,">/etc/mail/include/groups/$args{groupname}\.$domain")
        or die "Cant create the group file : $!\n";
      close(FH);
    }

    &edit_group(\%args);

  #  }

## end of subroutine
}

sub edit_group {
my $args = shift;

my $error;
my $message;
my $return_for_problem;

  if ( $args->{destination} =~ /[^\w\.\-\@]/ ) {
    $message = "I am sorry, you have entered an \"Illegal\" character in the E-Mail Field.<br>
         This field can only contain the following characters:<br>
         A-Z, a-z, 0-9, the dash (-), the underscore (_) and the period (.)<p>\n";
    $error=1;
    $return_for_problem = $args->{destination};

  } elsif ( $args->{destination} !~ /\@/ ) {
    $message = "I am sorry, the destination address that you entered does not<br>
           appear to be valid. Please re-enter your information.";
    $error=1;
    $return_for_problem = $args->{destination};

  } elsif ( $args->{destination} =~  tr/@// != 1 ) {
    $message = "Please enter only one e-mail address at a time.<br>";
    $error=1;
    $return_for_problem = $args->{destination};

  }

  if (($error) && (!$args->{del_addr}) && (!$args->{makefiles}) && (!$args->{mod})) {
    print qq|<font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#cc3300" size="-1"><b>$message</b></font>|;

  } else {
    ## open the group file for appending
    open(FH, ">>/etc/mail/include/groups/$args->{groupname}\.$domain")
      or die "Cant open group file : $args->{groupname} : $!\n";

    print FH "$args->{destination}\n" if ($args->{destination});

    close(FH);

  }

  ## build the form
  print qq|<form action="https://www.$domain/$self" method="post">|;

  ## table to show current mailing group
  print qq|<table width="600" cellspacing="0" cellpadding="0" border="0"><tr><td bgcolor="#000000">|;
  print qq|<table width="600" cellspacing="2" cellpadding="5" border="0"><tr><td bgcolor="#000000">|;
  print qq|<font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#FFFF99" size="-1"><b>Current Mailing Group : $args->{groupname}\@$domain</b></font>|;
  print qq|</td></tr></table>|;
  print qq|</td></tr></table><p>|;

  ## first table
  print <<REST;
  <!-- First table to set border color -->
  <table width="600" cellspacing="0" cellpadding="0" border="0">
   <tr>
    <td bgcolor="#000000" width="600">
     <table width="600" border="0" cellspacing="2" cellpadding="5">
REST

  ## first table header
  print qq|<tr><td bgcolor="#000000"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#FFFF99" size="-1"><b>Add an E-Mail Address to this Mailing Group</b></font>&nbsp;&nbsp;<A HREF="javascript:parent.startndnav('https://www.$domain/controlpanel/mailgroup-howto.htm')"><img src="$images/question.jpg"></a></td></tr>|;

  ## input
  print qq|<tr><td bgcolor="#99CC99"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#000000" size="-1"><b><input type="text" name="destination" size="30" value="$return_for_problem" maxlength="40"><p>(in the format username\@somedomain.com)</b></font></td></tr>|;

  ## end of first table
  print qq|</table></td></tr></table><p>|;

  ## hidden field for group name
  print qq|<input type="hidden" name="groupname" value="$args->{groupname}">|;

  ## hidden field to trigger address addition
  print qq|<input type="hidden" name="editgroup" value="on">|;

  ## submit the new email to be added
  print qq|<table cellpadding="0" cellspacing="0" border="0" width="600"><tr><td align="center">|;
  print qq|<input type="image" value="Submit" border="0" src="$images/submitbutton.gif">|;
  print qq|</td></tr></table><p>|;
  

  ## second table
  print <<REST;
  <!-- First table to set border color -->
  <table width="600" cellspacing="0" cellpadding="0" border="0">
   <tr>
    <td bgcolor="#000000" width="600">
     <table width="600" border="0" cellspacing="2" cellpadding="5">
REST

  ## second table header
  print qq|<tr><td bgcolor="#000000"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" color="#FFFF99" size="-1"><b>Current group</b></font>&nbsp;&nbsp;<A HREF="javascript:parent.startndnav('https://www.$domain/controlpanel/mailgroup-howto.htm')"><img src="$images/question.jpg"></a></td></tr>|;

  ## open the group of recipients
  open(FH, "/etc/mail/include/groups/$args->{groupname}\.$domain")
    or warn "Can not open group file : $!\n";

  my @groupaddrs = <FH>;

  close(FH);

  ## variables to create alternating table bgcolors
  my $count="1";
  my @bgcolor = ("junk", "#99CC99", "#009999");

  ## dynamically created table rows
  if ($#groupaddrs < 0) {
    print qq|<tr><td bgcolor="$bgcolor[$count]"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-1"><b>No addresses have been configured.</b></font></td></tr>\n|;
  
  } else {
    for my $i(sort @groupaddrs) {
      print qq|<tr><td bgcolor="$bgcolor[$count]" valign="middle"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif"size="-1"><b>$i</b></font>&nbsp;&nbsp;&nbsp;<a href="https://www.$domain/$self?del_addr=on&addr=$i&groupname=$args->{groupname}"><img src="$images/delete.gif" border="0"></a>|;
      if ($count > 1) { $count-- } else { $count++ }
    }
  }

  ## end of second table
  print qq|</table></td></tr></table><p>|;

## end of if loop
}

## end of subroutine
}

sub delete_addr {
my %args = %formdata;

  ## files touched
  my $groupfile = "/etc/mail/include/groups/$args{groupname}\.$domain";
  my $grouptmp = $groupfile . ".tmp";

  ## read in the current group
  open(FH, $groupfile)
    or die "Cant open groupfile : $!\n";
  flock(FH,2);
  seek(FH,0,0);

  my @addrs = <FH>;

  flock(FH,8);
  close(FH);

  ## open temp file for writing out new group
  open(TF, ">$grouptmp")
    or die "Cant open temp groupfile : $!\n";
  flock(TF,2);
  seek(TF,0,2);

  for my $i(sort @addrs) {
    next if ($i =~ /^$args{addr}/);
    print TF $i;
  }

  flock(TF,8);
  close(TF);

  ## move production file into place
  move($grouptmp, $groupfile);

  ## write out the edit screen again
  &edit_group(\%args);
  
}

sub delete_group {
my %args = %formdata;

  ## files touched
  my $groupfile = "/etc/mail/include/groups/$args{groupname}.$domain";
  my $aliasfile = "/etc/mail/include/aliases/alias.$domain";
  my $aliastmp = $aliasfile . ".tmp";
  my $virtfile = "/etc/mail/include/virtuser/virt.$domain";
  my $virttmp = $virtfile . ".tmp";

  ## remove the group of mail recipients
  unlink($groupfile)
    or warn "Cant remove group file : $!\n";

  ## read in the current aliases
  open(FH, $aliasfile)
    or warn "Cant open the alias file : $!\n";
  flock(FH,2);
  seek(FH,0,0);

  my @aliases = <FH>;

  flock(FH,8);
  close(FH);

  ## open tmp file for writing out new group
  open(TF, ">$aliastmp")
    or warn "Cant open tmp alias file : $!\n";
  flock(TF,2);
  seek(TF,0,2);

  for my $i(@aliases) {
    next if ($i =~ /^group-$args{groupname}\.$domain/);
    print TF $i;
  }

  flock(TF,8);
  close(TF);

  ## move tmp file into production
  move($aliastmp, $aliasfile);

  ## read in current virtusers
  open(FH, $virtfile)
    or warn "Cant open the virtuser file : $!\n";
  flock(FH,2);
  seek(FH,0,0);

  my @virtusers = <FH>;

  flock(FH,8);
  close(FH);

  ## open tmp file for writing out new group
  open(TF, ">$virttmp")
    or warn "Cant open tmp virtuser file : $!\n";
  flock(TF,2);
  seek(TF,0,2);

  for my $i(@virtusers) {
    next if ($i =~ /^$args{groupname}\@$domain/);
    print TF $i;
  }

  flock(TF,8);
  close(TF);

  ## move tmp file into production
  move($virttmp, $virtfile);

  ## show new group of configured groups
  &group_current;

}
