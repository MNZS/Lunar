#!/usr/bin/perl
# W3Mail - A webbased application to recieve POP3 mail and send e-mail via SMTP.
# Copyright (C) 2000  Spencer Miles
#

use CGI qw/:standard/;
use CGI::Carp qw(fatalsToBrowser);
use Mail::POP3Client;
use MIME::Base64;

require "w3mail.conf";
require "w3vars.cgi";

&initPage;

# Clear the SessionID and Encoded Passwd.
	$sessionID = $form->param('SessionID');
	require "$datadir/$mailserv/$user/info";
	&logout;
	
	open (IN, "$datadir/$mailserv/$user/attachments");
	while (<IN>) {
		chomp $_;
		system("$system_rm \"$_\"");
	}
	close (IN);
	open (OUT, ">$datadir/$mailserv/$user/attachments");  	
	print "";
	close (OUT);
	
	print qq~
    <meta HTTP-EQUIV="refresh" content="4; URL=$homepage">
    <div align="center">
     <table border="0" cellpadding="1" cellspacing="0" bgcolor="#000000">
      <tr>
       <td>
        <table width="100%" border="0" cellspacing="1" cellpadding="10">
         <tr>
          <td bgcolor="$bg_dark">
           <b>Thank you for using W3Mail</b>
          </td>
         </tr>
         <tr>
          <td bgcolor="$bg_light">
           <font size="-2" face="Geneva, Arial, Helvetica">
	    You are now being returned to your homepage.<br>
	    If your browser does not support redirecting, please click <a href="$homepage">here</a> to return to your homepage.
            </font>
          </td>
         </tr>
        </table>
       </td>
      </tr>
     </table>
    </div>
	~;
	&printTail;
	exit;
