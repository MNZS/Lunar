#!/usr/bin/perl
# W3Mail - A webbased application to recieve POP3 mail and send e-mail via SMTP.
# Copyright (C) 2000  Spencer Miles
#

use MIME::Base64;
use CGI qw/:standard/;
use CGI::Carp qw (fatalsToBrowser);
use Text::Wrap qw(wrap $columns);
use Mail::POP3Client;
use Time::Local;
########### User Customized Variables ##########

require 'w3mail.conf';
require 'w3vars.cgi';

&initPage;

&createSession;

############################################
########## Send SMTP Message ###############
############################################


use Mail::Sender;
require "$datadir/$mailserv/$user/info";

$preview = $form->param('preview');


# Upload file attachments
$attach1 = $form->param('attach1');
$attach2 = $form->param('attach2');
$attach1 =~ s/^.*\\([^\\]+)$/$1/;
$attach2 =~ s/^.*\\([^\\]+)$/$1/;

$prevattach1 = $form->param('prevattach1');
$prevattach2 = $form->param('prevattach2');

if ($attach1) {
# Begin Patch by Yuri / Mods by hardware
	$FH_ONE = $form->param('attach1');
	open (MYFILEONE,">$mimedir/$attach1");

	binmode (MYFILEONE);
	binmode ($FH_ONE);
	while ($bytesread = read($FH_ONE, $buffer, 1024)) {
		print MYFILEONE $buffer;
	}
	close(MYFILEONE);
	$attachment1 = "$mimedir/$attach1";
}
if ($attach2) {
	$FH_TWO = $form->param('attach2');
	open (MYFILETWO,">$mimedir/$attach2");
	binmode (MYFILETWO);
	binmode ($FH_TWO);
	while ($bytesread = read($FH_TWO, $buffer, 1024)) {
		print MYFILETWO $buffer;
	}
	close(MYFILETWO);
	$attachment2 = "$mimedir/$attach2";
}

$attachment1 = "$mimedir/" . $prevattach1 if $prevattach1;
$attachment2 = "$mimedir/" . $prevattach2 if $prevattach2;

if (!$preview) {
	$sendpreview = $form->param('funct');
	
	if (!$sendpreview) {

		$cc = $form->param('cc');
		$bcc = $form->param('bcc');
		$subject = $form->param('subject');
		$data = $form->param('data');
		if (!$replyto) {
			$from = "$name <$user\@$mailserv_replyto>";
		} else {
			$from = "$name <$replyto>";
		}
			
		$rcpt = $form->param('rcpt');

		$huge = 'wrap'; #Used for Text::Wrap
		$wrappeddata = wrap('','',$data);
	
		} else {
		
		if(-e "$datadir/$mailserv/$user/preview") {
			#$user =~ s/(@)/\\@/g;
			require "$datadir/$mailserv/$user/preview";
			$huge = 'wrap'; #Used for Text::Wrap
			$wrappeddata = wrap('','',$data);
			system ("$system_rm $datadir/$mailserv/$user/preview");
			} else {
			print "Error - could not open preview";
			&printTail;
			exit;
			}
		}
      $rcpt =~ s/[^$OK_CHARS]//go;
      $subject =~ s/[^$OK_CHARS]//go;
      $cc =~ s/[^$OK_CHARS]//go;
      $bcc =~ s/[^$OK_CHARS]//go;


if ($attachment1) {
	ref($smtp = new Mail::Sender
	{smtp => $smtpserv, from => $from}) or die "Error($sender) : $Mail::Sender::Error";
		if ($attachment2) {
			$smtp->OpenMultipart({to => $rcpt, cc => $cc, bcc => $bcc, subject => $subject});
			$smtp->Body(0,0,"text/plain");
			$smtp->SendLine($wrappeddata);
			#	$smtp->SendFile({disposition => "attachment; filename=*", encoding => "Base64", file => "$attachment1"});
			#	$smtp->SendFile({disposition => "attachment; filename=*", encoding => "Base64", file => "$attachment2"});
			$smtp->SendFile({file => "$attachment1"});
			$smtp->SendFile({file => "$attachment2"});
			unlink ("$attachment1");
			unlink ("$attachment2");
		} else {
			$smtp->OpenMultipart({to => $rcpt, cc => $cc, bcc => $bcc, subject => $subject});
			$smtp->Body(0,0,"text/plain");
			$smtp->SendLine($wrappeddata);
			#	$smtp->SendFile({disposition => "attachment; filename=*", encoding => "Base64", file => "$attachment1"});
			$smtp->SendFile({file => "$attachment1"});
			unlink ("$attachment1");
		}
	} else {
	ref( $smtp = new Mail::Sender
			{smtp => $smtpserv, from => $from}) or die "Error($sender) : $Mail::Sender::Error";
	$smtp->Open({to => $rcpt, cc => $cc, bcc => $bcc, subject => $subject});
	$smtp->SendLine($wrappeddata);
	}


die "Can't open user directory" if (!opendir(USERDIR, "$datadir/$mailserv/$user") );
require "$datadir/$mailserv/$user/info";
$pass = decode_base64($encpass);

$metatag = qq~<meta HTTP-EQUIV="refresh" content="5; URL=$cgidir/inbox.cgi?mailserv=$mailserv&user=$user&SessionID=$SessionID">~;

if ($smtp->Close eq "1") {
	$var1 = $smtp->Close;
	
	$message = "Message successfully sent.";
	
	open(ITEMS, "<$datadir/$mailserv/$user/outbox/items");
	while (<ITEMS>) {
		my @line = split(/\,/, $_);
		$i = @line[0];
	}
	close(ITEMS);
	
	open(ITEMS, ">>$datadir/$mailserv/$user/outbox/items") || die "Cannot open $datadir/$mailserv/$user/outbox/items for output";
	if (!$i) {
		$i = 0;
	}
	my $item = $i+1;
	#my $date = timelocal($sec,$min,$hours);
	
	my $date = `date +"%a %d %b %Y %T"`;
	chomp $date;
	print ITEMS "$item,$subject,$rcpt,$from,$cc,$bcc,$date\n";
	close(ITEMS);
	
		
	open(SENT, ">$datadir/$mailserv/$user/outbox/$item.msg") || die "Cannot open $datadir/$mailserv/$outbox/ for output";
	$cc =~ s/(@)/\\@/g;
	$bcc =~ s/(@)/\\@/g;
	$from =~ s/(@)/\\@/g;
	$rcpt =~ s/(@)/\\@/g;
	$wrappeddata =~ s/(@)/\\@/g;
	$subject =~ s/(@)/\\@/g;
	
	print SENT "\$cc = \"$cc\"\;\n";
	print SENT "\$bcc = \"$bcc\"\;\n";
	print SENT "\$subject = \"$subject\"\;\n";
	print SENT "\$data = \"$wrappeddata\"\;\n";
	print SENT "\$from = \"$from\"\;\n";
	print SENT "\$rcpt = \"$rcpt\"\;\n";
	print SENT "\$date = \"$date\"\;\n";
	print SENT "\$attach1 = \"$attachment1\"\;\n";
	print SENT "\$attach2 = \"$attachment2\"\;\n";
	
	print SENT "1\;\n";
	close(SENT);	
	
} else {
	$message = "Error: Message was not successfully sent.<br>\n$Mail::Sender::Error";
}
&generateMessage;
}

###############################
####### Preview Message #######
###############################

elsif ($preview or $form->param('rcpt') !~ /^[\w-.]+\@[\w-]+\.[\w]+$/ or $form->param('cc') !~ /^[\w-.]+\@[\w-]+\.[\w]+$/ or $form->param('bcc') !~ /^[\w-.]+\@[\w-]+\.[\w]+$/) {


$SendID = $form->param('SessionID');

$cc = $form->param('cc');
$bcc = $form->param('bcc');
$subject = $form->param('subject');
$data = $form->param('data');
if (!$replyto) {
	$from = "$name <$user\@$mailserv_replyto>";
} else {
	$from = "$name <$replyto>";
}
$rcpt = $form->param('rcpt');

$huge = 'wrap'; #Used for Text::Wrap
$wrappeddata = wrap('','',$data);

$cc2 = $cc;
$cc2 =~ s/\\/\\\\/g;
$cc2 =~ s/@/\\@/g;
$cc2 =~ s/"/\\"/g;

$bcc2 = $bcc;
$bcc2 =~ s/\\/\\\\/g;
$bcc2 =~ s/@/\\@/g;
$bcc2 =~ s/"/\\"/g;

$subject2 = $subject;
$subject2 =~ s/\\/\\\\/g;
$subject2 =~ s/@/\\@/g;
$subject2 =~ s/"/\\"/g;

$data2 = $data;
$data2 =~ s/\\/\\\\/g;
$data2 =~ s/@/\\@/g;
$data2 =~ s/"/\\"/g;

$from2 = $from;
$from2 =~ s/\\/\\\\/g;
$from2 =~ s/@/\\@/g;
$from2 =~ s/"/\\"/g;

$rcpt2 = $rcpt;
$rcpt2 =~ s/\\/\\\\/g;
$rcpt2 =~ s/@/\\@/g;
$rcpt2 =~ s/"/\\"/g;

$attach12 = $attach1;
$attach12 =~ s/\\/\\\\/g;
$attach12 =~ s/@/\\@/g;
$attach12 =~ s/"/\\"/g;

$attach22 = $attach2;
$attach22 =~ s/\\/\\\\/g;
$attach22 =~ s/@/\\@/g;
$attach22 =~ s/"/\\"/g;


	open(PREVIEW, ">$datadir/$mailserv/$user/preview") || die "Cannot open file for output";
	$user =~ s/(@)/\\@/g;
	print PREVIEW "\$mailserv = \"$mailserv\"\;\n";
	print PREVIEW "\$user = \"$user\"\;\n";
	print PREVIEW "\$SessionID = \"$SendID\"\;\n";
	print PREVIEW "\$cc = \"$cc2\"\;\n";
	print PREVIEW "\$bcc = \"$bcc2\"\;\n";
	print PREVIEW "\$subject = \"$subject2\"\;\n";
	print PREVIEW "\$data = \"$data2\"\;\n";
	print PREVIEW "\$from = \"$from2\"\;\n";
	print PREVIEW "\$rcpt = \"$rcpt2\"\;\n";
	print PREVIEW "\$attach1 = \"$attach12\"\;\n";
	print PREVIEW "\$attach2 = \"$attach22\"\;\n";
	
	print PREVIEW "1\;\n";
	close(PREVIEW);	

print qq~
<div align="center">
<table border="0" cellpadding="1" cellspacing="0" bgcolor="#000000" width="95%">
<tr bgcolor="#FFFFFF">
	<td width="50%" align="left" valign="bottom"><img src="$imageshttp/title_preview.gif" width="104" height="19" border="0" alt="Preview"></td>
	<td width="50%" align="right" valign="bottom"><font face="Geneva, Arial, Helvetica">&nbsp;&nbsp;&nbsp;($replyto)</font></td>
</tr>
<tr>
	<td colspan="2">
		<table width="100%" border="0" cellspacing="1" cellpadding="3">
		<tr><td bgcolor="$bg_dark" width="15%"><font face="Geneva, Arial, Helvetica" size="-1"><b>From:</b></font></td><td bgcolor="$bg_light"><font face="Geneva, Arial, Helvetica">$from</font></td></tr>
		<tr><td bgcolor="$bg_dark"><font face="Geneva, Arial, Helvetica" size="-1"><b>Subject:</b></font></td><td bgcolor="$bg_light"><font face="Geneva, Arial, Helvetica">$subject</font></td></tr>
		<tr><td bgcolor="$bg_dark"><font face="Geneva, Arial, Helvetica" size="-1"><b>To:</b></font></td><td bgcolor="$bg_light"><font face="Geneva, Arial, Helvetica">$rcpt</font></td></tr>
~;
unless ($cc eq "") {
print qq~		<tr><td bgcolor="$bg_dark"><font face="Geneva, Arial, Helvetica" size="-1"><b>Cc:</b></font></td><td bgcolor="$bg_light"><font face="Geneva, Arial, Helvetica">$cc</font></td></tr>\n~;
}
unless ($bcc eq "") {
print qq~		<tr><td bgcolor="$bg_dark"><font face="Geneva, Arial, Helvetica" size="-1"><b>Bcc:</b></font></td><td bgcolor="$bg_light"><font face="Geneva, Arial, Helvetica">$bcc</font></td></tr>~;
}
print qq~
		<tr>
			<td bgcolor="$bg_light" colspan="2">
<xmp>
~;

print "$wrappeddata";

print qq~
</xmp>
			</td>
		</tr>
		<tr>
			<td colspan="2" bgcolor="$bg_light">
				<table border="0" cellspacing="0" cellpadding="0">
				<tr>
~;
#if ($rcpt =~ /^[\w-.]+\@[\w-]+\.[\w]+$/ && ($cc =~ /^[\w-.]+\@[\w-]+\.[\w]+$/ or $cc eq "") && ($bcc =~ /^[\w-.]+\@[\w-]+\.[\w]+$/ or $bcc eq "")) {
print qq~
					<td valign="bottom">
						<form method="get" action="sendmessage.cgi" name="editmsg" ENCTYPE="multipart/form-data">
							<input type="hidden" name="funct" value="sendpreview">
							<input type="hidden" name="mailserv" value="$mailserv">
							<input type="hidden" name="user" value="$user">
							<input type="hidden" name="SessionID" value="$SessionID">
							<input type="hidden" name="prevattach1" value="$prevattach1">
							<input type="hidden" name="prevattach2" value="$prevattach2">
							<input type="submit" value="Send Message">
						</form>
					</td>
~;
#}
print qq~<td valign="bottom">~;
#if ($rcpt =~ /^[\w-.]+\@[\w-]+\.[\w]+$/) { } else {
#print qq~<font face="Geneva, Arial, Helvetica" size="-1"><b>Invalid email-Address!</b></font><br>~;
#}
#if ($cc =~ /^[\w-.]+\@[\w-]+\.[\w]+$/ or $cc eq "") { } else {
#print qq~<font face="Geneva, Arial, Helvetica" size="-1"><b>Invalid cc-email-Address!</b></font><br>~;
#}
#if ($bcc =~ /^[\w-.]+\@[\w-]+\.[\w]+$/ or $bcc eq "") { } else {
#print qq~<font face="Geneva, Arial, Helvetica" size="-1"><b>Invalid bcc-email-Address!</b></font><br>~;
#}

print qq~
					    <form method="post" action="$cgidir/compose.cgi">
							<input type="hidden" name="funct" value="changepreview">
							<input type="hidden" name="mailserv" value="$mailserv">
							<input type="hidden" name="user" value="$user">
							<input type="hidden" name="SessionID" value="$SessionID">
							<input type="hidden" name="attachments" value="$prevattach1">
							<input type="hidden" name="attachments" value="$prevattach2">
							<input type="submit" value="Change Message">
						</form>
					</td>
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

}
