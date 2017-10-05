#!/usr/bin/perl
# W3Mail - A webbased application to recieve POP3 mail and send e-mail via SMTP.
# Copyright (C) 2001  Spencer Miles

use MIME::Base64;
use Mail::POP3Client;
use CGI qw/:standard/;
use CGI::Carp qw(fatalsToBrowser);
use CGI::Cookie;
########### User Customized Variables ##########

require 'w3mail.conf';
require 'w3vars.cgi';

&initPage;

&createSession;
if ($form->param('folder')) {
	$folder = $form->param('folder');
} else {
	$folder = "inbox";
}
print qq~
<script language="JavaScript">
<!-- Hide this script from old browsers
	agent = navigator.userAgent;
	browserOk = 0;
	if (navigator.appName == "Netscape" && navigator.appVersion.substring(0,1) >= 2) {
		browserOk = 1
		} else {
	if (navigator.appName == "Microsoft Internet Explorer" && navigator.appVersion.substring(0,1) >= 3) {
		browserOk = 1 
		}
	}
	function checkorUncheck(foo) {
		if (browserOk) {
			for (i = 0; i < document.forms["deleteForm"].length; i++) {
				document.forms["deleteForm"].elements[i].checked = foo
			}
		}
	}
	function OpenAddressbook() {
		var addressWindow = window.open("addressbook.cgi?mailserv=$mailserv&user=$user&SessionID=$SessionID&edit=yes","AddressBook","width=600,height=450,resizable=yes,scrollbars=yes");
	}
	function addContact(contact, email_address) {
		var addressWindow = window.open("addressbook.cgi?func=precontact&contact_name=" + contact + "&email_address=" + email_address + "&mailserv=$mailserv&user=$user&SessionID=$SessionID&edit=yes","AddressBook","width=600,height=450,resizable=yes,scrollbars=yes");
	}
	function wstatus(txt) {
		window.status = txt;
		return true;
	}
// -- End hiding here -->
</script>
~;

if ($folder eq "inbox") {
# Return number of Messages on server.
$messages = $pop->Count();
$block = $form->param('block');

if ($block) {
   $topmsg = $block;
} else {
   $topmsg = $messages;
}

# Check for messages, if none exist die, if exist then display them...
if ($messages eq "0") {
   print qq~

<div align="center">
<table border="0" cellpadding="1" cellspacing="0" bgcolor="$bg_light" width="95%">
<tr>
	<td width="50%" align="left" valign="bottom"><img src="$imageshttp/title_inbox.gif" width="68" height="19" border="0" alt="Preferences"></td>
	<td width="50%" align="right" valign="bottom"><font face="Geneva, Arial, Helvetica">&nbsp;&nbsp;&nbsp;($replyto)</font></td>
</tr>
<tr>
	<td colspan="2">
		<table width="100%" border="0" cellspacing="1" cellpadding="10">
		<tr>
			<td bgcolor="$table_head">
				<font face="Geneva, Arial, Helvetica" size="+1">You have no messages.</font>
			</td>
		</tr>
		<tr bgcolor="$table_bg">
			<td>
				<table border="0" cellspacing="0" cellpadding="0" width="100%">
				<tr valign=top>
					<form method="post" action="$cgidir/inbox.cgi">$const_vars
					<td align="left" width="5%"><img src="$imageshttp/dot_clear.gif" width="10" height="1" border="0"><input type="image" src="$imageshttp/checkmail.gif" width="23" height="20" border="0" Name="Check mail" value="Check Mail" alt="Check E-Mail" onMouseOver="return wstatus('Check E-Mail')" onMouseOut="window.status='';return true"></td>
					</form>
					<form method="post" action="$cgidir/compose.cgi">$const_vars
					<td align="left" width="5%"><img src="$imageshttp/dot_clear.gif" width="10" height="1" border="0"><input type="image" src="$imageshttp/msg_new.gif" width="23" height="20" border="0" name="Compose Message" value="Compose Message" alt="Compose New Message" onMouseOver="return wstatus('Compose New Message')" onMouseOut="window.status='';return true"></form></td>
					

					<td align="right" width="85%">
						<form method="post" action="$cgidir/prefs.cgi">$const_vars
						<input type="hidden" name="func" value="modify">
						<input type="image" src="$imageshttp/prefs.gif" onMouseOver="window.status='Modify your preferences';return true" onMouseOut="window.status='';return true" border=0>
						</form>
					</td>
					<td align="right" width="5%" valign=top>
						<!img src="$imageshttp/dot_clear.gif" width="10" height="1" border="0">
											<form method="post" action="$cgidir/logout.cgi">$const_vars
						<input type="image" src="$imageshttp/logout.gif" width="23" height="20" border="0" name="Logout" value="Logout" alt="Logout" onMouseOver="return wstatus('Logout')" onMouseOut="window.status='';return true">
						<!img src="$imageshttp/dot_clear.gif" width="10" height="1" border="0"></td>
					</form>
				</tr>
				</table>
			</td>
		</tr>
		</table>
	</td>
</tr>
</table>
</div>
   ~;
	&printTail;
close;
}
        
$td_color = $bg_dark;

# Display list of Messages
if ($msgnum <= 0) {
	$inboxsize = ($pop->Size);
	print qq~
<div align="center">

<table border="0" cellpadding="0" cellspacing="0" width="97%">
<tr>
	<td width="68" align="left" valign="bottom"><img src="$imageshttp/title_inbox.gif" width="68" height="19" border="0" alt="Inbox"></td>
~;

&welcome;

print qq~
	<td width="25%" align="right" valign="bottom">
~;
	if ($messages > $show_messages) {
           print qq~
	<form method="post" action="$cgidir/inbox.cgi">$const_vars<font>Messages:</font><br><select name="block">
		~;
		$x = $messages;
		$msgblock = $messages;
		while ($x >= 1) {
			$x = $x - $show_messages;
			$bottom_msg = $x + 1;
			if ($bottom_msg < 1) {
				$bottom_msg = 1;
			}
			if ($topmsg eq $msgblock) {
				print qq~<option value="$msgblock" selected><font face="Geneva, Arial, Helvetica">$msgblock to $bottom_msg</font>~;
			} else {
				print qq~<option value="$msgblock">$msgblock to $bottom_msg</font>~;
			}
			$msgblock = $msgblock - $show_messages;
		}
		print qq~</select><input type="submit" value="Go!"></form></td>
</tr>
</table>
~;
	} else {
		print qq~</td></tr></table>~;
	}

	print qq~
<div align="center">
<form method="post" name="deleteForm" action="$cgidir/delete.cgi">
<input type="hidden" name="mailserv" value="$mailserv">
<input type="hidden" name="user" value="$user">
<input type="hidden" name="SessionID" value="$SessionID">
<input type="hidden" name="func" value="delete">

<table border="0" cellpadding="1" cellspacing="0" width="97%">
 <tr>
  <td>
   <table width="100%" border="0" cellspacing="0" cellpadding="3">
		<tr>
			<td colspan="2" width="75" bgcolor="#000000"><img src="$imageshttp/dot_clear.gif" width="1" height="1"></td>
			<td width=30% bgcolor="#000000"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="#ffff99"><b>Mail From:</b></font></td>
			<td width=40% bgcolor="#000000"><font color="#FFFF99" face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2"><b>Subject:</b></font></td>
			<td colspan="2" width=45 bgcolor="#000000"><img src="$imageshttp/dot_clear.gif" width="1" height="1"></td>
			<td bgcolor="#000000"><font color="#FFFF99" face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2"><b>Size:</b></font></td>
			<td width=60 bgcolor="#000000"><font color="#FFFF99" face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2"><b>Date:</b></font></td>
		</tr>
  </td>
 </tr>
~;

	$bottommsg = $topmsg - $show_messages;
	if (($topmsg - $show_messages) < 0) {
		$bottommsg = 0;
	}

	for ($i = $topmsg; $i > $bottommsg; $i-- ) {
		my ($from, $subject, $date, $read);
			foreach( $pop->Head($i)) {
				if (/^From:\s+/i) {
					s/(From:\s)//i;
					s/(<)/&lt;/g;
					s/(>)/&gt;/g;
					s/(")//g;
					s/(\w)(&lt;)/$1 &lt;/g;				
					$from = $_;
					}
				if ($from eq "") {
					$from = "(No Sender)";
					}
				if ($from) {                
					$contact = $from;
					$contact =~ s/\s(&lt;)([a-zA-Z0-9.\-_]+@[a-zA-Z0-9.\-_]+)(&gt;)//g;
					$email_address = $2;
					$contact =~ s/(")//g;
					$contact1 = $contact;
					$contact1 =~ s/(\s)/%20/g;
				}
				if (!$email_address) {
					$email_address = $contact;
				}
				if (/^Subject:\s+/i) {
					s/(Subject:\s)//i;
					$subject = $_;
					}
				if (/^Date:\s+/i) {
					s/(Date:\s)//i;
					$date = $_;
					}
				if (/^Status:\s/i) {
					s/(Status:\s)//i;
					$status = $_;
					chomp $status;
					if ($status eq "U") {
						$read = "<font color=\"red\"><b>*</b></font>";
					}
				}
				}
			# Parse subject to pass on to reply form
			$subject2 = $subject;
			$subject2 =~ s/(Subject:\s)//i;
			$subject2 =~ s/(\s)/%20/g;

			# Parse from to pass on to reply as recipient
			$rcpt = $from;
			$rcpt =~ s/(\s)//g;
			$rcpt =~ s/(&lt;)/ </g;
			$rcpt =~ s/(&gt;)/>/g;
			$rcpt =~ s/(\S+\s)//g;
			$rcpt =~ s/(<|>)//g;		
			


	if ( $td_color eq "#99CC99" ) {
	   $td_color = "#009999";
	} else {
           $td_color = "#99CC99";
	}

if (! length($subject) ) {
    $subject = '(No Subject)';
}

	print qq~
	<tr valign="top">
		<td width="52" bgcolor="$td_color">
		<nobr>
		 <font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2">$i.</font>
		 <input type="checkbox" name="msgnum" value="$i">$read
		 </nobr>
		</td>
		<td valign="top" width="23" bgcolor="$td_color">
		 <a href="javascript:addContact('$contact1','$email_address')" onMouseOver="return wstatus('Add $contact to your Address Book')" onMouseOut="window.status='';return true"><img src="$imageshttp/add_address.gif" width="23" height="20" border="0" alt="add contact"></a>
		</td>
		<td valign="top" width="30%" bgcolor="$td_color">
		  <a href="$cgidir/showmessage.cgi?msgnum=$i&mailserv=$mailserv&user=$user&SessionID=$SessionID" onMouseOver="return wstatus('Read message from $from')" onMouseOut="window.status='';return true">
		   <font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="#000000">$contact</font>
		  </a>
		</td>
		<td valign="top" width="40%" bgcolor="$td_color">
		 <font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2"> 
		  $subject 
		 </font>
		</td>
		<td valign="top" width="23" bgcolor="$td_color">
		 <a href="$cgidir/compose.cgi?mailserv=$mailserv&replynum=Re$i&user=$user&SessionID=$SessionID" onMouseOver="return wstatus('Reply to message from $from')" onMouseOut="window.status='';return true">
		  <img src="$imageshttp/msg_reply.gif" width="23" height="20" border="0" alt="Reply to Message">
		 </a>
		</td>
		<td valign="top" width="23" bgcolor="$td_color">
		 <a href="$cgidir/compose.cgi?mailserv=$mailserv&replynum=Fwd$i&user=$user&SessionID=$SessionID" onMouseOver="return wstatus('Forward message from $from')" onMouseOut="window.status='';return true">
		  <img src="$imageshttp/msg_forward.gif" width="23" height="20" border="0" alt="Forward Message">
		 </a>
		</td>
		<td valign="top" bgcolor="$td_color">
			<font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2"><nobr>
~;
&message_size($i);
print qq~  
			</nobr></font>
		</td>
		<td valign="top" bgcolor="$td_color">
			<font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2">	
~;
&parse_date($date);
print qq~
			</font>
		</td>
	<tr>
	~;

}

&inboxBar;

}
}

if ($folder eq "outbox") {
	print qq~
	<div align="center">
	<table border="0" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF" width="97%">
	<tr bgcolor="#FFFFFF">
		<td width="68" align="left" valign="bottom"><h2>Outbox</h2></td>
	~;
	
	
	print qq~
	</td><td width="20%">&nbsp</td></tr></table>
	
	<table border="0" cellpadding="1" cellspacing="0" bgcolor="#000000" width="97%">
	<tr>
	<td>
	<table width="100%" border="0" cellspacing="1" cellpadding="3">
	<tr bgcolor="$table_head"> 
	<td width=10%><img src="$imageshttp/dot_clear.gif" width="1" height="1"></td>
	<td width=36%><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2"><b>Recipient:</b></font></td>
	<td width=40%><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2"><b>Subject:</b></font></td>
	<td width=14%><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2"><b>Date:</b></font></td>
	</tr></tr>
	~;

	open (ITEMS, "<$datadir/$mailserv/$user/outbox/items");
	$td_color = $bg_dark;
	while (<ITEMS>) {
		@item = split(/\,/, $_);
		my $message = @item[0];		
		my $subject = @item[1];
		my $rcpt = @item[2];
		my $from = @item[3];
		my $cc = @item[4];
		my $bcc = @item[5];
		my $date = @item[6];
	if ($td_color eq $bg_dark) {
		$td_color = $bg_light;
	} else {
		$td_color = $bg_dark;
	}
	if ($rcpt) {
	print qq~
	$const_vars
	<input type=hidden name=folder value=outbox>
	<tr valign="top" bgcolor="$td_color"> 
		<td width=25><form method="post" name="deleteForm" action="$cgidir/delete.cgi">$const_vars<input type=hidden name=msgnum value=$message><input type=hidden name=folder value=outbox><input type="submit" value="Delete"></form></td>
		<td valign="top">
		 <font>
		  <a href="$cgidir/showmessage.cgi?&mailserv=$mailserv&user=$user&SessionID=$SessionID&msgnum=$message&folder=outbox" onMouseOver="return wstatus('Read message from $from')" onMouseOut="window.status='';return true">
		   $rcpt 
		  </a>
		 </font>
		</td>

		<td valign="top">
		 <font> 
		  $subject 
		 </font>
		</td>

		<td valign="top">
			<font>
~;
&parse_date($date);
print qq~
			</font>
		</td>
	<tr>
	~;
	} else {
		print "<tr><td colspan=6 bgcolor=\"white\">You have no messages in your outbox</td></tr>";
	}
	}
	
	
	

print qq~

  <tr bgcolor="$table_bg"> 
    
    <td colspan="7" valign="middle">
      <table border="0" cellspacing="0" cellpadding="0" width="100%">
	<tr>
	  <td width="50%" align="left" valign="top">
	     <table border="0" cellspacing="0" cellpadding="0">
	       <tr>

		   <td valign="top">
			<form method="post" action="$cgidir/compose.cgi">$const_vars		   
		    <img src="$imageshttp/dot_clear.gif" width="10" height="1" border="0"><input type="image" name="Compose" value="Compose Message" src="$imageshttp/msg_new.gif" width="23" height="20" border="0" alt="Compose New Message" onMouseOver="return wstatus('Compose New Message')" onMouseOut="window.status='';return true">
			</form>
		   </td>

		   <td valign="top">
			<form method="post" action="$cgidir/inbox.cgi">$const_vars
		    <img src="$imageshttp/dot_clear.gif" width="10" height="1" border="0"><input type="image" name="Check mail" value="Check Mail" src="$imageshttp/checkmail.gif" width="23" height="20" border="0" alt="Check Mail" onMouseOver="return wstatus('Check Mail')" onMouseOut="window.status='';return true">
		   </form>
		   </td>

		 <td align=right valign=bottom>
		   <form method="post" action="$cgidir/inbox.cgi">$const_vars<nobr><font>&nbsp;&nbsp;Folder:</font>
		     <select name="folder">
		~;
	open (INPUT, "<$datadir/$mailserv/$user/folders");
	while (<INPUT>) {
	my @folders = split(/\,/, $_);
	my $f_name = @folders[1];
	chomp $f_name;
	if (!$folder) {
		$folder = "inbox";
	}
	if ($f_name eq $folder) {
		print "<option value=$f_name selected>";
	} else {
		print "<option value=$f_name>";
	}
	print @folders[0];
	
	}
	close (INPUT);
	print qq~
	</select>
	<input type="submit" value="Go!">
	</nobr>
	</form>
	</td>
				
				</tr>
				</table>
			</td>
			<td width="50%" align="right" valign="top">
				<table border="0" cellspacing="0" cellpadding="0">
				<tr>
				<td valign="top"><a href="javascript:OpenAddressbook()"><img src="$imageshttp/addressbook.gif" width="23" height="20" border="0" alt="Open Addressbook" onMouseOver="return wstatus('Open Addressbook')" onMouseOut="window.status='';return true"></td>
				</form>
				<form method="post" action="$cgidir/prefs.cgi">$const_vars
				<input type="hidden" name="func" value="modify">
				<td valign="top"><img src="$imageshttp/dot_clear.gif" width="10" height="1" border="0"><input type="image" name="preferences" value="Preferences" src="$imageshttp/prefs.gif" width="23" height="20" border="0" alt="Modify your Preferences" onMouseOver="return wstatus('Modify your Preferences')" onMouseOut="window.status='';return true"></td>
				</form>
				<form method="post" action="$cgidir/logout.cgi">$const_vars
				<td valign="top"><img src="$imageshttp/dot_clear.gif" width="10" height="1" border="0"><input type="image" name="logout" value="Logout" src="$imageshttp/logout.gif" width="23" height="20" border="0" alt="Logout" onMouseOver="return wstatus('Logout')" onMouseOut="window.status='';return true"><img src="$imageshttp/dot_clear.gif" width="10" height="1" border="0"></form></td>
				</tr>
				</table>
			</td>
		</tr>
		</table>
	</td>
</tr>
</table>

</td></tr></table>
</div>
~;
	
	
}


$pop->Close();
 
&printTail;
