#!/usr/bin/perl
# W3Mail - A webbased application to recieve POP3 mail and send e-mail via SMTP.
# Copyright (C) 2000  Spencer Miles
#

use CGI qw(param);
use CGI::Carp qw(fatalsToBrowser);
use MIME::Base64;
use Mail::POP3Client;

require "w3mail.conf";
require "w3vars.cgi";

&initPage;

&createSession;

$folder = $form->param('folder');
      $folder =~ s/[^$OK_CHARS]//go;

if (!$folder) {
	@msgsToDelete = $form->param( 'msgnum' );
	foreach ( @msgsToDelete ) {
 	 $pop->Delete( $_ );
	}
}

if ($folder) {
	$msgnum = $form->param('msgnum');
	system("$system_rm $datadir/$mailserv/$user/$folder/$msgnum.msg");

	open(ITEMS, "<$datadir/$mailserv/$user/outbox/items") || die;
	while (<ITEMS>) {
		unshift @items, $_;
	}
	close(ITEMS);
	
	open(ITEMS, ">$datadir/$mailserv/$user/outbox/items") || die;
		foreach (@items) {
			@line = split(/\,/, $_);
			$item = @line[0];
			if ($msgnum eq $item) {
				#print "$msgnum deleted";
			} else {
				#print @items[$item-1];
				print ITEMS $_;
			}
		}
	close(ITEMS);

}

$pop->Close();

$message = "Message(s) successfully deleted.";
&generateMessage;
