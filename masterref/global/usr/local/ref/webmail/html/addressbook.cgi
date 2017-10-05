#!/usr/bin/perl
# W3Mail - A webbased application to recieve POP3 mail and send e-mail via SMTP.
# Copyright (C) 2000  Spencer Miles
#

use MIME::Base64;
use CGI qw/:standard/;
use CGI::Carp qw(fatalsToBrowser);

require 'w3mail.conf';
require 'w3vars.cgi';

$form = new CGI;
$CGI::POST_MAX=$maxpost * 100; # Max 100k posts
#print CGI::header(-type => "text/html");

# Retreive form fields...
$mailserv = $form->param('mailserv');
$user = $form->param('user');
$SessionID = $form->param('SessionID');
if ($form->param('pass')) {
	$pass = $form->param('pass');
}
$func = $form->param('func');
      #$mailserv =~ s/[^$OK_CHARS]//go;
      #$user =~ s/[^$OK_CHARS]//go;
      #$SessionID =~ s/[^$OK_CHARS]//go;
      #$func =~ s/[^$OK_CHARS]//go;

require "$datadir/$mailserv/$user/info";

if ($func eq "precontact") {
	&precontact;
}

if ($func eq "addcontact") {
	&addcontact;
}

if ($form->param("delete")) {
	&delete_contact;
}

if ($form->param("to")) {
	&addresscompose;
}

if ($form->param("edit")) {
         &editaddresses;
}

if ($func eq "import") {
	&import;
}

if ($func eq "uploadaddress") {
	&importbook;
}

sub import {
	&initPage;
	&constVars;
	print qq~
	<form method=POST action=addressbook.cgi ENCTYPE="multipart/form-data">
	 $const_vars
	 <input type="hidden" name="func" value="uploadaddress">
	 <input type="radio" name="client" value="outlook">
	 Outlook Express (.CSV) <input type=file name="outlookcsv">
	 <br><font size=-1>
	 To import addresses you must first export your address book in Outlook Express to a file.  To do so open Outlook Express and from the file menu choose Export -> Address Book.  Choose Text File (Comma Seperated Values) from the list of export types, and click export.  Choose a location to save the file to, click next, and from the list of fields you wish to export only choose Name and E-mail Address.  Next you need to click browse in this window, choose the file you have exported, and click Import to import your address book into W3Mail. <b>Note:</b> You must click the radio button next to Outlook Express in this screen before importing.</font>
	 <hr size=1>
	 <input type="radio" name="client" value="netscape">
	 Netscape Address Book (.LDIF) <input type=file name="netscapeldif">
	 <br>
	 <font size=-1>
	 To import your Netscape Address Book, simply open the Address Book in Netscape, click the File menu, click Export, type a file name, and click OK.  Then in this screen choose the file by clicking browse, and then click Import.  <b>Note:</b> You must click the radio button next to Netscape Address Book in this screen before importing.</font>
	 <br>
	 <input type=submit value="Import">
	</form>
	~;
}

sub importbook {
	&initPage;
	
	$client = $form->param('client');
      $client =~ s/[^$OK_CHARS]//go;

	if (!$client) {
		$errorMessage = "<b>You have not chosen an address book to import.</b>";
		&generateError;
	}
		
	if ($client eq "outlook") {
		$outlook = $form->param('outlookcsv');
      $outlook =~ s/[^$OK_CHARS]//go;
      
		if ($outlook eq "") {
			$errorMessage = "<b>You must choose a file to import</b>";
			&generateError;
		}
	}
	
	if ($client eq "netscape") {
		$netscape = $form->param('netscapeldif');
      $netscape =~ s/[^$OK_CHARS]//go;
      
		if ($netscape eq "") {
			$errorMessage = "<b>You must choose a file to import.</b>";
			&generateError;
		}
	}

	$addressbook = "$datadir/$mailserv/$user/addressbook";

	if ($outlook) {
		open (OUT, "$addressbook");
		while (<OUT>) {
			chomp;
			if (!/^1\;/) {
				push (@keep, $_);
			}
		}
		close (OUT);
		
		open (OUT, ">$addressbook");
		foreach (@keep) {
			print OUT $_,"\n";
		}
		close (OUT);
		
		my $firstline = <$outlook>;
		my @firstline = split(/\,/, $firstline);
		if (@firstline[0] !~ "Name" || @firstline[1] !~ "E-mail") {
			$errorMessage = "<b>$addresses[0]File not in proper format.<br>Please export outlook express CSV with Field 1 containing Full Name and Field 2 containing E-mail Address.</b";
			&generateError;
		}
		
		open (ADDRESSBOOK,">>$addressbook");
		print "<table border=1 width=300 align=center>";
		while (<$outlook>) {
			$i = 1;
			my @addresses = split(/\,/, $_);
			
			if ($addresses[0] eq "Name" && $addresses[1] =~ "E-mail") {
			} else {
				print "<tr><td>$addresses[0]</td><td>$addresses[1]</td></tr>";
				@addresses[1] =~ s/(@)/\\@/g;
				@addresses[0] =~ s/(@)/\\@/g;
				@addresses[1] =~ s/(\n)//g;
				print ADDRESSBOOK "\$addresses\{\"$addresses[0]\"\} = \"$addresses[1]\"\;\n";
			}
			$i++;
		}
		print ADDRESSBOOK "1\;";
		close(ADDRESSBOOK);
	}
	
	
	if ($netscape) {
		open (OUT, "$addressbook");
		while (<OUT>) {
			chomp;
			if (!/^1\;/) {
				push (@keep, $_);
			}
		}
		close (OUT);
		
		open (OUT, ">$addressbook");
		foreach (@keep) {
			print OUT $_,"\n";
		}
		close (OUT);
				
		open (ADDRESSBOOK,">>$addressbook");
		print "<table border=1 width=300 align=center>";
		$i = 0;
		while (<$netscape>) {
			my $name, $email;
			if (/^dn:\s+/i) {
				s/(dn:\s+)//g;
				s/(cn=)([a-zA-Z0-9.\-_\s]+)//g;
				$name = $2;
				s/(mail=)([a-zA-Z0-9.\-_]+@[a-zA-Z0-9.\-_]+)//g;
				$email = $2;
				if ($email !~ /[a-zA-Z0-9.\-_]+@[a-zA-Z0-9.\-_]+/) {
					$email = "";
				}
			chomp($name);
			if ($email && $name) {
				print "<tr><td>$name</td><td>$email</td></tr>";
				$email =~ s/(@)/\\@/g;
				$name =~ s/(@)/\\@/g;
				print ADDRESSBOOK "\$addresses\{\"$name\"\} = \"$email\"\;\n";			
				$i++;
			}
			}
		}
		print ADDRESSBOOK "1\;";
		close(ADDRESSBOOK);
	}
	
	print "</tr><tr><td colspan=2 align=center><b>$i Addresses Imported.</b></td></tr></table>";
	print "<center><a href=addressbook.cgi?edit=yes&user=$user&mailserv=$mailserv>Return to Address Book</a></center>";
}

sub precontact {
	if (-e "$datadir/$mailserv/$user/addressbook") {
		require "$datadir/$mailserv/$user/addressbook";
	}
	$email_address = $form->param('email_address');
	$contact_name = $form->param('contact_name');
   $email_address =~ s/[^$OK_CHARS]//go;
   $contact_name =~ s/[^$OK_CHARS]//go;

	print "Location: $cgidir/addressbook.cgi?mailserv=$mailserv&user=$user&SessionID=$SessionID&edit=yes&pre1=$contact_name&pre2=$email_address\n\n";
	exit;
}


sub addcontact {
	if (-e "$datadir/$mailserv/$user/addressbook") {
		require "$datadir/$mailserv/$user/addressbook";
	}
	$email_address = $form->param('email_address');
	$contact_name = $form->param('contact_name');
   $email_address =~ s/[^$OK_CHARS]//go;
   $contact_name =~ s/[^$OK_CHARS]//go;
	
	if ($email_address && $contact_name)	{
	
	} else {
	print "Location: $cgidir/addressbook.cgi?mailserv=$mailserv&user=$user&SessionID=$SessionID&edit=yes&pre1=$contact_name&pre2=$email_address\n\n";
	exit;
	}
	
	@keynames = keys(%addresses);
	
	open(ADDRESSOUT, ">$datadir/$mailserv/$user/addressbook");
	
	foreach $key (@keynames) {
		$addresses{$key} =~ s/(\@)/\\\@/g;
		$key2 = $key;
		$key2 =~ s/(\@)/\\\@/g;
		print ADDRESSOUT "\$addresses\{\"$key2\"\} = \"$addresses{$key}\"\;\n";
	}

	$email_address =~ s/(\@)/\\\@/g;
	$contact_name =~ s/\@/\\\@/g;
	print ADDRESSOUT "\$addresses\{\"$contact_name\"\} = \"$email_address\"\;\n";
	print ADDRESSOUT "1\;";
	close(ADDRESSOUT);
	print "Location: $cgidir/addressbook.cgi?mailserv=$mailserv&user=$user&SessionID=$SessionID&edit=yes\n\n";
	exit;
}


sub delete_contact {
	if (-e "$datadir/$mailserv/$user/addressbook") {
		require "$datadir/$mailserv/$user/addressbook";
	}
	$del_contact = $form->param("delete");
   $del_contact =~ s/[^$OK_CHARS]//go;
	@keynames = keys(%addresses);
	
	open(DELETEOUT, ">$datadir/$mailserv/$user/addressbook");
	
	foreach $key (@keynames) {
		if ($key ne $del_contact) {
			$addresses{$key} =~ s/(\@)/\\\@/g;
			$key2 = $key;
			$key2 =~ s/(\@)/\\\@/g;
			print DELETEOUT "\$addresses\{\"$key2\"\} = \"$addresses{$key}\"\;\n";
		}
	}

	print DELETEOUT "1\;";
	close(DELETEOUT);
	print "Location: $cgidir/addressbook.cgi?mailserv=$mailserv&user=$user&SessionID=$SessionID&edit=yes\n\n";
	exit;
}


sub editaddresses() {
&constVars;
print $form->header;
if (-e "$datadir/$mailserv/$user/addressbook") {
	require "$datadir/$mailserv/$user/addressbook";
}

@key_names = keys(%addresses);

$pre1 = $form->param('pre1');
$pre2 = $form->param('pre2');
      $pre1 =~ s/[^$OK_CHARS]//go;
      $pre1 =~ s/[^$OK_CHARS]//go;

&printHeader;
print qq~
<script language="JavaScript">
	function SendContact(email) {
		window.opener.document.editmsg.rcpt.value = email;
	}
</script>


<div align="center">

 
<table border="0" cellpadding="1" cellspacing="0" width="95%">
<tr>
	<td width="50%" align="left" valign="bottom">&nbsp;</td>
	<td width="50%" align="right" valign="bottom"><font face="Geneva, Arial, Helvetica">&nbsp;&nbsp;&nbsp;($replyto)</font></td>
</tr>
<tr>
	<td colspan="2">
      <form method="post" action="$cgidir/addressbook.cgi">  
		<table width="100%" border="0" cellspacing="1" cellpadding="3">
		<tr bgcolor="$bg_dark">
			 <td><font face="Geneva, Arial, Helvetica"><b>Action:</b></font></td>
			 <td><font face="Geneva, Arial, Helvetica"><b>Contact Name:</b></font></td>
			 <td><font face="Geneva, Arial, Helvetica"><b>E-Mail Address:</b></font></td>
		</tr>

		<tr bgcolor="$bg_dark">

$const_vars
<input type="hidden" name="func" value="addcontact">
			<td>
				<input type="submit" name="addcontact" value="Add Contact">
			</td>
			<td bgcolor="$bg_light"><input name="contact_name" value="$pre1"></td>
			<td bgcolor="$bg_light"><input name="email_address" value="$pre2"></td>
		</tr>
      </form>

      ~;

foreach $key (sort @key_names) {
	$addresses{$key} =~ s/(\\@)/@/g;
	print qq~
	<form method="post">   
	<tr bgcolor="$bg_dark">
	$const_vars
	<input type="hidden" name="delete" value="$key">
	<td>
	<input type="submit" value="Delete">
	</td>
	<td width="30%" bgcolor="$bg_light"><font face="Geneva, Arial, Helvetica">$key</font></td>
	<td bgcolor="$bg_light"><font face="Geneva, Arial, Helvetica"><a href="#" onclick="javascript:window.opener.location='$cgidir/compose.cgi?mailserv=$mailserv&user=$user&SessionID=$SessionID&to=$addresses{$key};return true'">$addresses{$key}</a></font></td>
	</tr>
   </form>

	~;
}

if (!-e "$datadir/$mailserv/$user/addressbook") {
	print qq~<tr><td colspan="3"><font face="Geneva, Arial, Helvetica">No Contacts Present.</font></td></tr>\n~;
}

print qq~

		</table>

	</td>
</tr>
<tr><td colspan="2">
<a href="$cgidir/addressbook.cgi?mailserv=$mailserv&user=$user&func=import"><font face="Geneva, Arial, Helvetica" color="#000000">Import Address Book</font></a>
</td></tr>
</table>
</div>
~;
}




sub addresscompose() {
print $form->header;
$to = $form->param("to");
      $to =~ s/[^$OK_CHARS]//go;

if (-e "$datadir/$mailserv/$user/addressbook") {
	require "$datadir/$mailserv/$user/addressbook";
}

@key_names = keys(%addresses);

&printHeader;
print qq~
<script language="JavaScript">
	function SendContact(email) {
		window.opener.document.editmsg.$to.value = email;
		window.close();
	}

function updateAddress() {
	for (var i = 0; i < document.list.elements.length - 1; i++) {
		var box = document.list.elements[i];
		if (window.opener.document.editmsg.$to.value) {
			var address = window.opener.document.editmsg.$to.value;
		}
		if (box.checked) {
			if (address) {
				address += ",";
				address += box.value;
				window.opener.document.editmsg.$to.value = address;
			}
			else {
				window.opener.document.editmsg.$to.value = box.value;
			}
		}
	}
	window.close();
}
</script>

<div align="center">
<table border="0" cellpadding="1" cellspacing="0" width="95%">
<tr>
	<td width="50%" align="left" valign="bottom">&nbsp;</td>
	<td width="50%" align="right" valign="bottom"><font face="Geneva, Arial, Helvetica">&nbsp;&nbsp;&nbsp;($replyto)</font></td>
</tr>
<tr>
	<td colspan="2">
		<table width="100%" border="0" cellspacing="1" cellpadding="3">
		<tr>
			<td colspan="3"><font face="Geneva, Arial, Helvetica" size="-1"><b>Copy entry to message</b></font></td>
		</tr>
<form name="list" method="post" action="javascript:updateAddress()">
$const_vars
~;

foreach $key (@key_names) {
	$addresses{$key} =~ s/(\\@)/@/g;
	print qq~
		<tr>
			<td valign="center" width="5">
				<input type="checkbox" name="$key" value="$addresses{$key}">
			</td>
			<td width="30%" bgcolor="$bg_light"><font face="Geneva, Arial, Helvetica">$key</font></td>
			<td bgcolor="$bg_light"><a href="javascript:SendContact('$addresses{$key}')">$addresses{$key}</a></td>
		</tr>
~;
}

if (!-e "$datadir/$mailserv/$user/addressbook") {
	print qq~<tr bgcolor="$bg_light"><td colspan="3"><font face="Geneva, Arial, Helvetica">No Contacts Present.</font></td></tr>~;
}

print qq~
		<tr bgcolor="$bg_dark">
			<td colspan="3"><input type="submit" value="OK"></td>
		</tr>
</form>
		</table>
	</td>
</tr>
</table>
</div>
~;
}


&printTail;
