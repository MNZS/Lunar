#!/usr/bin/perl
# W3Mail - A webbased application to recieve POP3 mail and send e-mail via SMTP.
# Copyright (C) 2001  Spencer Miles

use MIME::Base64;
use CGI qw/:standard/;
use CGI::Carp qw(fatalsToBrowser);

require 'w3mail.conf';
require 'w3vars.cgi';

&initPage;

$func = $form->param('func');

if ($func eq "postprefs") {
 	&postPrefs;

	$message = "Your preferences have been updated.";
	&generateMessage;
}

if ($func eq "modify") {
	&preferences;
}
