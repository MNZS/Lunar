#!/usr/bin/perl

# W3Mail - A webbased application to recieve POP3 mail and send e-mail via SMTP.
# Copyright (C) 2001  Spencer Miles

use Mail::POP3Client;
use MIME::Parser;
use MIME::Entity;
use MIME::Body;
use MIME::Base64;
use CGI qw/:standard/;
use CGI::Carp qw(fatalsToBrowser);
use Text::Wrap qw(wrap $columns);

require 'w3mail.conf';
require 'w3vars.cgi';

&initPage;

&createSession;

$msgblock = $form->param('msgblock');
$msgnum = $form->param('msgnum');
$encpass = $form->param('encpass');
$func = $form->param('func');
$block = $form->param('block');
@urls = ("ftp://","http://","https://","telnet://","gopher://");
$folder = $form->param('folder');

$status = $pop->Count();

if (!$folder) {
# Return number of Messages on server.
$messages = $pop->Count();

if ($block) {
   $topmsg = $block;
} else {
   $topmsg = $messages;
}
        
	my ($from, $subject, $to, $cc, $date);
	foreach( $pop->Head($msgnum)) {
		if (/^From:\s+/i) {
			s/(From:\s)//i;
			s/(<)/&lt;/g;
			s/(>)/&gt;/g;
			s/(")//g;
			s/\|//g;
			$from = $_;
			}
		if ($from) {
			$contact = $from;
			$contact =~ s/\s(&lt;)(\w+@[a-zA-Z0-9.-]+)(&gt;)//g;
			$contact =~ s/\|//g;
			$email_address = $2;
			$contact =~ s/(\s)/%20/g;
			$contact =~ s/(")//g;
			}
		if (!$email_address) {
			$email_address = $contact;
		}
		if (/^Subject:\s+/i) {
			s/(Subject:\s)//i;
			s/\|//g;
			$subject = $_;
			}
		if (/^To:\s+/i) {
			s/(To:\s)//i;
			s/\|//g;
			$to = $_;
			}
		if (/^Cc:\s+/i) {
			s/(Cc:\s)//i;
			s/\|//g;
			$cc = $_;
			}
		if (/^Date:\s+/i) {
			s/(Date:\s)//i;
			s/\|//g;
			$date = $_;
		}
		if (/^Content-Type:\s+/i) {
			s/(Content-Type:\s)//i;
			s/\|//g;
			$content_type = $_;
		}
	}

		$rcpt = $from;
		$rcpt =~ s/(\s)//g;
		$rcpt =~ s/(&lt;)/</g;
		$rcpt =~ s/(&gt;)/>/g;
		$rcpt =~ s/(\S+\s)//g;
		$rcpt =~ s/\<\>//g;
		$rcpt =~  s/\|//g;

		$subject2 = $subject;
		$subject2 =~ s/(Subject:\s)//i;
		$subject2 =~ s/(\s)/%20/g;

		$next = $msgnum+1;
		$prev = $msgnum-1;


print qq~
<style type="text/css"><!-- a:hover{color:$hover} --></style>
<script language=javascript>
	function OpenAddressbook() {
		var addressWindow = window.open("addressbook.cgi?mailserv=$mailserv&user=$user&SessionID=$SessionID&edit=yes","AddressBook","width=600,height=450,resizable=yes,scrollbars=yes");
	}
	
	function addContact(contact, email_address) {
		var addressWindow = window.open("addressbook.cgi?func=precontact&contact_name=" + contact + "&email_address=" + email_address + "&mailserv=$mailserv&user=$user&SessionID=$SessionID&edit=yes","AddressBook","width=600,height=450,resizable=yes,scrollbars=yes");
	}
</script>
~;

print qq~
<div align="center">
<table border="0" cellpadding="1" cellspacing="0" width="95%">
<tr>
	<td width="50%" align="left" valign="bottom"><img src="$imageshttp/title_show_msg.gif" width="201" height="19" border="0" alt="Preferences"></td>
	<td width="50%" align="right" valign="bottom"><font>&nbsp;&nbsp;&nbsp;($replyto)</font></td>
</tr>
<tr>
	<td colspan="2">
		<table width=100% border=0 cellspacing=1 cellpadding=3>
		<tr>
			<td bgcolor="$bg_dark"><font><b>From:</b></font></td><td bgcolor="$bg_light"><font>$from&nbsp;</font></td></tr>
~;
	if ($subject) {
		print qq~<tr><td bgcolor="$bg_dark"><font><b>Subject:</b></font></td><td bgcolor="$bg_light"><font>$subject&nbsp;</font></td></tr>\n~;
	} else {
		print qq~<tr><td bgcolor="$bg_dark"><font><b>Subject:</font></b></td><td bgcolor="$bg_light"><font>(No Subject)</font></td></tr>\n~;
	}
	if ($to) {
		print qq~<tr><td bgcolor="$bg_dark"><b><font>To:</font></b></td><td bgcolor="$bg_light"><font>$to&nbsp;</font></td></tr>\n~;
	}
	if ($cc) {
		print qq~<tr><td bgcolor="$bg_dark"><font><b>Cc:</b></font></td><td bgcolor="$bg_light"><font>$cc&nbsp;</font></td></tr>\n~;
	}
print qq~
	<tr><td bgcolor="$bg_dark"><font><b>Date:</b></font></td><td bgcolor="$bg_light"><font>
~;
&parse_date($date);
print qq~
		</font>
		</td>
	</tr>
	<tr>
		<td bgcolor="$table_bg" colspan="2">
			<table border="0" cellspacing="0" cellpadding="0" width="100%">
			<tr>
				<td width="50%" align="left">
					<img src="$imageshttp/dot_clear.gif" width="10" height="1" border="0">
					<a href="$cgidir/inbox.cgi?mailserv=$mailserv&user=$user&SessionID=$SessionID" onMouseOver="window.status='Return to Inbox';return true"><img src="$imageshttp/checkmail.gif" width="23" height="20" border="0" alt="Inbox"></a>
					<img src="$imageshttp/dot_clear.gif" width="10" height="1" border="0">
					<a href="$cgidir/compose.cgi?mailserv=$mailserv&user=$user&SessionID=$SessionID" onMouseOver="window.status='Compose Message';return true"><img src="$imageshttp/msg_new.gif" width="23" height="20" border="0" alt="Compose Message"></a>
					<img src="$imageshttp/dot_clear.gif" width="10" height="1" border="0">
					<a href="$cgidir/compose.cgi?mailserv=$mailserv&replynum=Re$msgnum&user=$user&SessionID=$SessionID" onMouseOver="window.status='Reply to $from';return true"><img src="$imageshttp/msg_reply.gif" width="23" height="20" border="0" alt="Reply"></a>
					<img src="$imageshttp/dot_clear.gif" width="10" height="1" border="0">
					<a href="$cgidir/compose.cgi?mailserv=$mailserv&replynum=Fwd$msgnum&user=$user&SessionID=$SessionID" onMouseOver="window.status='Forward this Message';return true"><img src="$imageshttp/msg_forward.gif" width="23" height="20" border="0" alt="Forward"></a>
					<img src="$imageshttp/dot_clear.gif" width="10" height="1" border="0">
					<a href="$cgidir/delete.cgi?mailserv=$mailserv&user=$user&msgnum=$msgnum&SessionID=$SessionID" onMouseOver="window.status='Delete Message';return true"><img src="$imageshttp/msg_delete.gif" width="23" height="20" border="0" alt="Delete"></a>
				</td>
				<td width="50%" align="right">
~;
if ($msgnum != $messages) 	{
	print qq~<img src="$imageshttp/dot_clear.gif" width="10" height="1" border="0"><a href="$cgidir/showmessage.cgi?mailserv=$mailserv&msgnum=$next&user=$user&SessionID=$SessionID" onMouseOver="window.status='Previous Message';return true"><img src="$imageshttp/msg_prev.gif" width="23" height="20" border="0" alt="Previous Message"></a>~;
	}
if ($msgnum != 1) {
	print qq~<img src="$imageshttp/dot_clear.gif" width="10" height="1" border="0"><a href="$cgidir/showmessage.cgi?mailserv=$mailserv&msgnum=$prev&user=$user&SessionID=$SessionID" onMouseOver="window.status='Next Message';return true"><img src="$imageshttp/msg_next.gif" width="23" height="20" border="0" alt="Next Message"></a>~;
	}

print qq~
					<img src="$imageshttp/dot_clear.gif" width="10" height="1" border="0">
					<a href="javascript:OpenAddressbook()" onMouseOver="window.status='Open Addressbook';return true" onMouseOut="window.status='';return true"><img src="$imageshttp/addressbook.gif" width="23" height="20" border="0" alt="Open Addressbook"></a>
					<img src="$imageshttp/dot_clear.gif" width="10" height="1" border="0">
					<a href="javascript:addContact('$contact', '$email_address')" onMouseOver="window.status='Add contact to your Address Book';return true"><img src="$imageshttp/add_address.gif" width="23" height="20" border="0" alt="Add Contact to Address Book"></a>
					<img src="$imageshttp/dot_clear.gif" width="10" height="1" border="0">
					<a href="$cgidir/logout.cgi?mailserv=$mailserv&user=$user&SessionID=$SessionID" onMouseOver="window.status='Logout';return true"><img src="$imageshttp/logout.gif" width="23" height="20" border="0" alt="logout"></a>
					<img src="$imageshttp/dot_clear.gif" width="10" height="1" border="0">
				</td>
			</tr>
			</table>
		</td>
	</tr>
~;

###### Test if message has mime stuff
if ($content_type !~ /multipart/i) {

		$body = $pop->Body($msgnum);

		$wrappedbody = wrap('','',$body);

		if ($body !~ /<html>/i) {
		$wrappedbody =~ s/</\&lt;/g;
		$wrappedbody =~ s/>/\&gt;/g;
		}

		foreach $url (@urls) {
			$wrappedbody =~ s/($url\S+)(\s)/<a href=$1>$1<\/a>$2/g;
		}
		$wrappedbody =~ s/([\w-.]+\@[\w-]+\.[\w]+)(\s)/<a href=compose.cgi?mailserv=$mailserv&user=$user&SessionID=$SessionID&to=$1>$1<\/a>$2/g;
		$wrappedbody =~ s/\n/<br>\n/g;

	print qq~<tr bgcolor="$bg_light"><td colspan="2"><font face="Courier, Courier New">~;
	
	if ($body !~ /<html>/i) {

	print "$wrappedbody";
	} else {
	$body =~ s/<html>//gi;
	$body =~ s/<\/html>//gi;
	$body =~ s/<!doctype[^>]*>//gi;
	foreach $url (@urls) {
		$body =~ s/($url\S+)(\s)/<a href=$1>$1<\/a>$2/g;
	}
	$body =~ s/([\w-.]+\@[\w-]+\.[\w]+)(\s)/<a href=compose.cgi?mailserv=$mailserv&user=$user&SessionID=$SessionID&to=$1>$1<\/a>$2/g;
#	$body =~ s/(<)([a-zA-Z0-9.\-_]+@[a-zA-Z0-9.\-_]+)/<a href=compose.cgi?mailserv=$mailserv&user=$user&SessionID=$SessionID&to=$1>$1<\/a>/g;
	
	$body =~ s/\n/<br>\n/g;
	print "$body";
	}
	
	print qq~</font>\n</td></tr>~;
	print qq~</table></td></tr></table></div>~;
}



	###################
	###### MIME STUFF #
	###################

if ($content_type =~ /multipart/i) {
	
$msg = $pop->HeadAndBody($msgnum);


print qq~
<tr bgcolor="$bg_light"><td colspan=2>
<font face="Courier, Courier New">
~;

open (OUT, ">$mimedir/$msgnum.part");
print OUT $msg;
close(OUT);


&mime_msgs;



print qq~</font>~;

print "</td></tr>\n";
print "</table></td></tr></table></div>\n";	

}


&printTail;
$pop->Close();


# Subs
#

#------------------------------------------------------------
# mime_msgs
#------------------------------------------------------------

sub mime_msgs {

use MIME::Parser;

&main;

}


#------------------------------------------------------------
# main
#------------------------------------------------------------
sub main {
    my $file;
    my $entity;

	$file = "$mimedir/$msgnum.part";
	
	my $msgdir = "$mimedir";

	my $parser = new MIME::Parser;
    
	$parser->output_dir($msgdir);


	open FILE, $file or die "couldn't open $file";
	$entity = $parser->read(\*FILE) or 
	    print "Couldn't parse MIME in $file; continuing...\n";
	close FILE;

	dump_entity($entity) if $entity;
}


#------------------------------------------------------------
# dump_entity - dump an entity's file info
#------------------------------------------------------------
sub dump_entity {
    my $ent = shift;
    my @parts = $ent->parts;

    if (@parts) {        # multipart...
	map { dump_entity($_) } @parts;
    } else {               # single part...
    if (scalar($ent->head->mime_type) =~ /^text/i || /^message/i) {
    	open (PART, $ent->bodyhandle->path);
		$file = $ent->bodyhandle->path;   
		$file =~ s/($mimedir\/)//g;
		$filehref = $file;
		$filehref =~ s/( )/%20/g;
		if ($file !~ /msg/i) {
			print qq~<div align="center">\n<table border="2" width="50%">\n<tr>~;
			print qq~<td width="15"><img src="$imageshttp/attachment.gif" width="15" height="20" border="0"></td>~;
			print qq~<td><font face="Geneva, Arial, Helvetica" size="-1"><b>Inline Attachment:</b></font></td>~;
# Remove line below
#			print qq~<td><div align="center"><a href="$mimehttp/$file">$file</a></div></td>\n~;
			print qq~<td><div align="center"><a href="$mimehttp/$filehref">$file</a></div></td>\n~;			
			print qq~<td><div align=center>~;
			print scalar($ent->head->mime_type);
			print qq~</div></td></tr></table></div><p><hr size="1" noshade>\n~;
		}
		if (scalar($ent->head->mime_type) !~ /html/i) {
			while (<PART>) {
				$body = $_;
				$body =~ s/</\&lt;/g;
				$body =~ s/>/\&gt;/g;
    			$body =~ s/\n/<br>\n/g;
    			foreach $url (@urls) {
					$body =~ s/($url\S+)(\s)/<a href=\"$1\">$1<\/a>$2/g;
				}
				$body =~ s/([\w-.]+\@[\w-]+\.[\w]+)(\s)/<a href=compose.cgi?mailserv=$mailserv&user=$user&SessionID=$SessionID&to=$1>$1<\/a>$2/g;
				print $body;
   		 	}
		} else {
			while (<PART>) {
				print $_;
			}
		}	
    close(PART);
    unlink "$mimedir/$file";
	unlink "$mimedir/$msgnum.part";
    }
    if (scalar($ent->head->mime_type) =~ /^image/) {
    	$file = $ent->bodyhandle->path;
		$file =~ s/($mimedir\/)//g;
		$filehref = $file;
		$filehref =~ s/( )/%20/g;
		print qq~<hr width=70% noshade>\n~;
		print qq~<div align="center">\n<table border="2" width="50%">\n<tr>~;
		print qq~<td><a href="$mimehttp/$filehref">$file</a></td>\n~;		
		print qq~<td><b>Name:</b> $file<br><b>File Type:</b> ~;
		print scalar($ent->head->mime_type);
		print qq~</td></tr></table>\n~;
    	print qq~<a href="$mimehttp/$filehref" border="0"><img src=$mimehttp/$filehref></a>\n~;      	
      	print qq~</div>\n~;
      	&userAttachments;
	}
	if (scalar($ent->head->mime_type) =~ /^application/ || /^audio/ || /^video/) {
		$file = $ent->bodyhandle->path;
		$file =~ s/($mimedir\/)//g;
		$filehref = $file;
		$filehref =~ s/( )/%20/g;
		print qq~<hr size="1" noshade>\n~;
		print qq~<div align="center">\n<table border="2" width="50%">\n<tr>~;
		print qq~<td align="center" width="15"><img src="$imageshttp/attachment.gif" width="15" height="20" border="0"><br></td>~;
		print qq~<td><a href="$mimehttp/$filehref">$file</a></td>\n~;		
		print qq~<td><b>Name:</b> $file<br><b>File Type:</b> ~;
		print scalar($ent->head->mime_type);
		print qq~</td></tr></table></div>\n~;
		&userAttachments;
    }
    }
}
}

if ($folder) {
	if(!opendir(FOLDER, "$datadir/$mailserv/$user/$folder")) {
		$errorMessage = "<b>Couldn't open folder $folder.</b>";
		&generateError;
	}
	require "$datadir/$mailserv/$user/$folder/$msgnum.msg";
	foreach $url (@urls) {
		$data =~ s/($url\S+)(\s)/<a href=$1>$1<\/a>$2/g;
	}
	$data =~ s/([\w-.]+\@[\w-]+\.[\w]+)(\s)/<a href=compose.cgi?mailserv=$mailserv&user=$user&SessionID=$SessionID&to=$1>$1<\/a>$2/g;
	$data =~ s/\n/<br>\n/g;
	print qq~
<div align="center">
<table border="0" cellpadding="1" cellspacing="0" bgcolor="#000000" width="95%">
<tr bgcolor="#FFFFFF">
	<td width="50%" align="left" valign="bottom"><img src="$imageshttp/title_show_msg.gif" width="201" height="19" border="0" alt="Preferences"></td>
	<td width="50%" align="right" valign="bottom"><font>&nbsp;&nbsp;&nbsp;($replyto)</font></td>
</tr>
<tr>
	<td colspan="2">
		<table width=100% border=0 cellspacing=1 cellpadding=3>
		<tr>
			<td bgcolor="$bg_dark"><font><b>From:</b></font></td><td bgcolor="$bg_light"><font>$from&nbsp;</font></td></tr>
~;
	if ($rcpt) {
		print qq~<tr><td bgcolor="$bg_dark"><b><font>To:</font></b></td><td bgcolor="$bg_light"><font>$rcpt&nbsp;</font></td></tr>\n~;
	}
	if ($subject) {
		print qq~<tr><td bgcolor="$bg_dark"><font><b>Subject:</b></font></td><td bgcolor="$bg_light"><font>$subject&nbsp;</font></td></tr>\n~;
	} else {
		print qq~<tr><td bgcolor="$bg_dark"><font><b>Subject:</font></b></td><td bgcolor="$bg_light"><font>(No Subject)</font></td></tr>\n~;
	}

	if ($cc) {
		print qq~<tr><td bgcolor="$bg_dark"><font><b>Cc:</b></font></td><td bgcolor="$bg_light"><font>$cc&nbsp;</font></td></tr>\n~;
	}
print qq~
	<tr><td bgcolor="$bg_dark"><font><b>Date:</b></font></td><td bgcolor="$bg_light"><font>
~;
&parse_date($date);
print qq~
		</font>
		</td>
	</tr>
	<tr>
		<td bgcolor="$table_bg" colspan="2">
			<table border="0" cellspacing="0" cellpadding="0" width="100%">
			<tr>
				<td width="50%" align="left">
					<img src="$imageshttp/dot_clear.gif" width="10" height="1" border="0">
					<a href="$cgidir/inbox.cgi?mailserv=$mailserv&user=$user&SessionID=$SessionID" onMouseOver="window.status='Return to Inbox';return true"><img src="$imageshttp/checkmail.gif" width="23" height="20" border="0" alt="Inbox"></a>
					<img src="$imageshttp/dot_clear.gif" width="10" height="1" border="0">
					<a href="$cgidir/compose.cgi?mailserv=$mailserv&user=$user&SessionID=$SessionID" onMouseOver="window.status='Compose Message';return true"><img src="$imageshttp/msg_new.gif" width="23" height="20" border="0" alt="Compose Message"></a>
					<img src="$imageshttp/dot_clear.gif" width="10" height="1" border="0">
					<a href="$cgidir/delete.cgi?mailserv=$mailserv&user=$user&msgnum=$msgnum&SessionID=$SessionID&folder=outbox" onMouseOver="window.status='Delete Message';return true"><img src="$imageshttp/msg_delete.gif" width="23" height="20" border="0" alt="Delete"></a>
				</td>
				<td width="50%" align="right">
~;


print qq~

					<img src="$imageshttp/dot_clear.gif" width="10" height="1" border="0">
					<a href="$cgidir/logout.cgi?mailserv=$mailserv&user=$user&SessionID=$SessionID" onMouseOver="window.status='Logout';return true"><img src="$imageshttp/logout.gif" width="23" height="20" border="0" alt="logout"></a>
					<img src="$imageshttp/dot_clear.gif" width="10" height="1" border="0">
				</td>
			</tr>
			</table>
		</td>
	</tr>
	<tr bgcolor="$bg_light"><td colspan="2"><font face="Courier, Courier New">
	$data
	</td></tr>
	
	
</table></td></tr></table>
~;	
	
	
	&printTail;
}
