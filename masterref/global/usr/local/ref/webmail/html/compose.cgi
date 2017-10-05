#!/usr/bin/perl

# W3Mail - A webbased application to recieve POP3 mail and send e-mail via SMTP.
# Copyright (C) 2001  Spencer Miles

use CGI qw/:standard/;
use MIME::Parser;
use MIME::Entity;
use MIME::Body;
use MIME::Base64;
use Mail::POP3Client;
use CGI::Carp qw(fatalsToBrowser);

require 'w3mail.conf';
require 'w3vars.cgi';

&initPage;

&createSession;

$replynum = $form->param( 'replynum' );
$to = $form->param('to');
$mailserv = $form->param( 'mailserv' );
$replynum =~ s/([a-zA-Z]+)//g;
$replynum =~ s/[^$OK_CHARS]//go;
$to =~ s/[^$OK_CHARS]//go;
$mailserv =~ s/[^$OK_CHARS]//go;
$msgnum = $replynum;
$type = $1;
my @attachments = $form->param('attachments');
my $body = "";

# If a Reply or Forward get the Body of the message...
if ($replynum >= 1) {
   foreach( $pop->Head($replynum) ) {
	if (/^From:\s+/i) {
	   s/(From:\s)//i;
	   s/(<)/&lt;/g;
	   s/(>)/&gt;/g;
	   $from = $_;
	}
	if (/^Subject:\s+/i) {
	   s/(Subject:\s)//i;
	   $subject = $_;
	}
	if (/^Date:\s+/i) {
	   s/(Date:\s)//i;
	   $date = $_;
	}
	if (/^Content-Type:\s+/i) {
		s/(Content-Type:\s)//i;
		s/\|//g;
		$content_type = $_;
	}
   }
   $subject2 = $subject;
   $subject2 =~ s/(Subject:\s)//i;
   $subject2 =~ s/(\s)/%20/g;

   $rcpt = $from;
   $rcpt =~ s/(\s)//g;
   $rcpt =~ s/(&lt;)/ </g;
   $rcpt =~ s/(&gt;)/>/g;
   $rcpt =~ s/(\S+\s)//g;
   $rcpt =~ s/(<|>)//g;

   $date2 = $date;
   $date2 =~ s/(^\S+,)|(-\d+)//g;
} # end if

if($content_type !~ /multipart/i) {
	$body = $pop->Body($replynum);
	$body =~ s/(\n)/\n> /g;
}

if ($content_type =~ /multipart/i) {
	$msg = $pop->HeadAndBody($msgnum);
	
	open (OUT, ">$mimedir/$msgnum.part");
	print OUT $msg;
	close(OUT);
	&mime_msgs;
}

sub mime_msgs {
	use MIME::Parser;
	&parseMessage;
}

sub parseMessage {
    my $file;
    my $entity;

	$file = "$mimedir/$msgnum.part";
	my $msgdir = "$mimedir";
	my $parser = new MIME::Parser;
 	$parser->parse_nested_messages('REPLACE');
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
		if (scalar($ent->head->mime_type) =~ /^text/i || scalar($ent->head->mime_type) =~ /^message/i) {
			open (PART, $ent->bodyhandle->path);

			$file = $ent->bodyhandle->path;   
			$file =~ s/($mimedir\/)//g;
			$filehref = $file;
			$filehref =~ s/( )/%20/g;
			if ($file !~ /msg/i) {
				push(@attachments,$file) if $type eq "Fwd";
			}
			if (scalar($ent->head->mime_type) !~ /html/i) {
				$body .= "\n\n";
				while (<PART>) {
					$body .= "> " . $_;
				}
			}

		close(PART);
		unlink "$mimedir/$msgnum.part";
		unlink "$mimedir/$file";
		}
		elsif (scalar($ent->head->mime_type) =~ scalar($ent->head->mime_type) =~ /^image/) {
			$file = $ent->bodyhandle->path;
			$file =~ s/($mimedir\/)//g;
			$filehref = $image;
			$filehref =~ s/( )/%20/g;
			push(@attachments,$file) if $type eq "Fwd";
			&userAttachments;
		}
		else {
			$file = $ent->bodyhandle->path;
			$file =~ s/($mimedir\/)//g;
			$filehref = $file;
			$filehref =~ s/( )/%20/g;
			push(@attachments,$file) if $type eq "Fwd";

			&userAttachments;
		}
	}
}

$pop->Close();

$changepreview = $form->param('funct');
	      $changepreview =~ s/[^$OK_CHARS]//go;

if ($changepreview) {
require "$datadir/$mailserv/$user/preview";
$to = $rcpt;
system ("rm $datadir/$mailserv/$user/preview");
}

print qq~
<script>
function OpenAddressbook() {
	var addressWindow = window.open("addressbook.cgi?mailserv=$mailserv&user=$user&SessionID=$SessionID&edit=yes","AddressBook","width=600,height=450,resizable=yes,scrollbars=yes");
	}

function SendTo(toccbcc) {
	var url = "addressbook.cgi?mailserv=$mailserv&user=$user&SessionID=$SessionID&to=" + toccbcc;
	var addressWindow = window.open(url,"AddressBook","width=600,height=450,resizable=yes,scrollbars=yes");
	}
	
function validator() {
	if (document.editmsg.attach1.value != "") {
		var confirm1 = confirm("You will lose your attachments previewing the message.\\nAre you sure you wish to continue?");
		if (!confirm1) {
			history.go(-1);
		}
	}
}
</script>
<br>

<div align="center">
<form method="post" action="sendmessage.cgi" name="editmsg" ENCTYPE="multipart/form-data">
$const_vars
<table border="0" cellpadding="1" cellspacing="0" bgcolor="$bg_light" width="95%">
<tr>
	<td width="50%" align="left" valign="bottom"><img src="$imageshttp/title_compose.gif" width="252" height="19" border="0" alt="Compose Message"></td>
	<td width="50%" align="right" valign="bottom"><font face="Geneva, Arial, Helvetica">&nbsp;&nbsp;&nbsp;($replyto)</font></td>
</tr>
<tr>
	<td colspan="2">
		<table width="100%" border="0" cellspacing="1" cellpadding="3">
		<tr bgcolor="$table_bg">
			<td colspan="4">
				<table border="0" cellspacing="0" cellpadding="0" width="100%">
				<tr>
					<td width="50% align="left">
					<img src="$imageshttp/dot_clear.gif" width="10" height="1">
					<a href="$cgidir/inbox.cgi?mailserv=$mailserv&user=$user&SessionID=$SessionID" onMouseOver="window.status='Return to Inbox';return true" onMouseOut="window.status='';return true"><img src="$imageshttp/checkmail.gif" width="23" height="20" border="0" alt="Inbox"></a>
					</td>
					<td width="50%" align="right">
					<a href="javascript:OpenAddressbook()" onMouseOver="window.status='Open Adressbook';return true" onMouseOut="window.status='';return true"><img src="$imageshttp/addressbook.gif" width="23" height="20" border="0" alt="Addressbook"></a>
					<img src="$imageshttp/dot_clear.gif" width="10" height="1">
					<a href="$cgidir/prefs.cgi?mailserv=$mailserv&user=$user&SessionID=$SessionID&func=modify" onMouseOver="window.status='Modify your preferences';return true" onMouseOut="window.status='';return true"><img src="$imageshttp/prefs.gif" width="23" height="20" border="0" alt="Preferences"></a>
					<img src="$imageshttp/dot_clear.gif" width="10" height="1">
					<a href="$cgidir/logout.cgi?mailserv=$mailserv&user=$user&SessionID=$SessionID" onMouseOver="window.status='Logout';return true" onMouseOut="window.status='';return true"><img src="$imageshttp/logout.gif" width="23" height="20" border="0" alt="Logout"></a>
					<img src="$imageshttp/dot_clear.gif" width="10" height="1">
					</td>
				</tr>
				</table>
			</td>
		</tr>
~;


if ($type eq "Fwd") {
	print qq~
		<tr bgcolor="$bg_dark">
			<td><a href="javascript:SendTo('rcpt')"><font face="Geneva, Arial, Helvetica" size="-1" color="#000000">Recipient:</font></a></td>
			<td><input name="rcpt" size="30" tabindex="1"></td>
			<td><font face="Geneva, Arial, Helvetica" size="-1">Subject:</font></td>
			<td><input name="subject" value="Fwd: $subject" size="30" tabindex="2"></td>
		</tr>\n~;
}
if ($type eq "Re") {
	print qq~
		<tr bgcolor="$bg_dark">
			<td><a href="javascript:SendTo('rcpt')"><a href="javascript:SendTo('rcpt')"><font face="Geneva, Arial, Helvetica" size="-1" color="#000000">Recipient:</font></a></td>
			<td><input name="rcpt" size="30" value="$rcpt" tabindex="1"></td>
			<td><font face="Geneva, Arial, Helvetica" size="-1">Subject:</font></td>
			<td><input name="subject" value="Re: $subject" size="30" tabindex="2"></font></td>
		</tr>\n~;
}
if (!$type) {
	print qq~
		<tr bgcolor="$bg_dark">
			<td><a href="javascript:SendTo('rcpt')"><a href="javascript:SendTo('rcpt')"><font face="Geneva, Arial, Helvetica" size="-1" color="#000000">Recipient:</font></a></td>
			<td><input name="rcpt" size="30" value="$to" tabindex="1"></td>
			<td><font face="Geneva, Arial, Helvetica" size="-1">Subject:</font></td>
			<td><input name="subject" value="$subject" size="30" tabindex="2"></td>
		</tr>\n~;
}
print qq~
		<tr bgcolor="$bg_dark">
			<td><a href="javascript:SendTo('cc')"><a href="javascript:SendTo('rcpt')"><font face="Geneva, Arial, Helvetica" size="-1" color="#000000">CC:</font></a></td>
			<td><input name="cc" size="30" value="$cc"></td>
			<td><font face="Geneva, Arial, Helvetica" size="-1">Attachment 1:</td>
~;
if(!$attachments[0]) {
	print qq~<td><input type="file" name="attach1"></td>~;
} else {
	my $attach1 = $attachments[0];
	print qq~<td><input type="hidden" name="prevattach1" value="$attach1">$attach1</td>~;
}

print qq~
		</tr>
		<tr bgcolor="$bg_dark">
			<td><a href="javascript:SendTo('bcc')"><a href="javascript:SendTo('rcpt')"><font face="Geneva, Arial, Helvetica" size="-1" color="#000000">BCC:</font></a></td>
			<td><input name="bcc" size="30" value="$bcc"></font></td>
			<td><font face="Geneva, Arial, Helvetica" size="-1">Attachment 2:</td>
~;
if(!$attachments[1]) {
	print qq~<td><input type="file" name="attach2"></td>~;
} else {
	my $attach2 = $attachments[1];
	print qq~<td><input type="hidden" name="prevattach2" value="$attach2">$attach2</td>~;
}
print qq~
		</tr>
		<tr bgcolor="$bg_light">
			<td valign="top" bgcolor="$bg_dark"><font face="Geneva, Arial, Helvetica">Message:</font></td>
			<td colspan="3"><textarea name="data" rows="13" wrap="soft" cols="75" tabindex="3">~;
print "$data";

### Print signature if it exists.
if (!$changepreview) {
	if($sig) {
		print "&nbsp;";
		print "\n\n--\n";
		print $sig;
	}
	if ($rcpt) {
		print "&nbsp;";
		print "\n\n$rcpt wrote:\n> ";
		print $body;
	}


}

print qq~</textarea>
			</td>
		</tr>
		<tr bgcolor="$bg_light">
			<td colspan="4">
				<input type="submit" name=preview value="Preview Message">
				<input type="submit" value="Send Message">
				<input type="reset" value="Clear">
			</td>
		</tr>
		</table>
	</td>
</tr>
</table>
</form>
</div>
~;
&printTail;
