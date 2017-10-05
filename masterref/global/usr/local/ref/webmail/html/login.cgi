#!/usr/bin/perl
# W3Mail - A webbased application to recieve POP3 mail and send e-mail via SMTP.
# Copyright (C) 2001  Spencer Miles


use CGI qw/:standard/;
use CGI::Carp qw(fatalsToBrowser);
use CGI::Cookie;
$cgi = new CGI;

require 'w3mail.conf';
require 'w3vars.cgi';
&sessionid;

$cookies = $cgi->param('cookies');
$userCookie = $cgi->param('user');
$serverCookie = $cgi->param('server');

if( $cookies eq "off") {
      $nameCookie = new CGI::Cookie(-name=>'name',
                                -value=>$userCookie,
                                -path=>$cgidir
                                -expires=>'now');
      $serverCookie = new CGI::Cookie(-name=>'server',
                                -value=>$serverCookie,
                                -path=>$cgidir
                                -expires=>'now');
      print header(-cookie=>[$nameCookie,$serverCookie],
                   -type=>"text/html");
} else {
   print CGI::header(-type => "text/html");
   %cookies = fetch CGI::Cookie;
   $name = $cookies{'name'}=>value;
   $server = $cookies{'server'}=>value;
   if( $name && $server) {
      $loginName = $name->value;
      $serverName = $server->value;
   }
}

&printHeader(login);
my $divreply = @mailserver_replyto[0];


print qq~
<div align="center">
<div align="center">
 <table border="0" cellpadding="3" cellspacing="0" width="350">
  <tr>
   <td bgcolor="Black">
 <table border="0" cellpadding="0" cellspacing="0" width="350">
  <form method="post" action="$cgidir/inbox.cgi" name="login">
   <input type="hidden" name="SessionID" value="$SessionID">
   <input type="hidden" name="isLogin" value="1">
   <tr>
     <td>
        <table width="100%" border="0" cellspacing="0" cellpadding="0">
             <input type="hidden" name="mailserv" value="mail.DOMAIN">
             <tr><td bgcolor="#CC3300">&nbsp;</td><td bgcolor="#CC3300">&nbsp;</td></tr>
          <tr>
             <td bgcolor="#CC3300" align="right"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="#FFFF99"><b>Username:&nbsp;</b></font></td>
             <td bgcolor="#CC3300" valign="middle">
~;

if( $loginName && $serverName ) {
   print qq~ <input type="hidden" name="user" value="$loginName"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="#FFFF99"><b>~ . uc($loginName) . qq~</b></font>~;
} else {
   print qq~ <input name="user" size=20"> ~;
}

print qq~
             </td>
           </tr>
           <tr><td bgcolor="#CC3300">&nbsp;</td><td bgcolor="#CC3300">&nbsp;</td></tr>
           <tr>
             <td bgcolor="#CC3300" align="right"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="#FFFF99"><b>Password:&nbsp;</b></font></td>
             <td bgcolor="#CC3300"><input name="pass" type="password"></td>
           </tr>
           <tr><td bgcolor="#CC3300">&nbsp;</td><td bgcolor="#CC3300">&nbsp;</td></tr>

           <tr bgcolor="$bg_light">
             <td colspan="2">
               <table border="0" cellspacing="0" cellpadding="0" width="100%">
                <noscript>
                                        <tr>
                                                <td colspan="2">
                                                        <font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="#FFFF99">
                                                        <b>You have to enable javascript in<br>
                                                        your browsers preferences while using<br>
                                                        WebMail!
                                                        </font>
                                                </td>
                                        </tr>
                                        </noscript>
                                        <tr>
                                                <td align="center" colspan="2" bgcolor="#CC3300"><input type="image" src="images/login.gif" value="submit" border="0"</td>
					</tr>
					<tr><td colspan="2" bgcolor="#CC3300">&nbsp;</td></tr>
					<tr>
						<td colspan="2" bgcolor="#CC3300" align="center">
~;

if ( !$loginName && !$serverName ) {
   print qq~<input name="cookies" type="checkbox"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="#FFFF99">Remember my id on this computer</font></input></td>~;
} else {
   print qq~ <a href="./login.cgi?cookies=off&user=$loginName&server=$serverName"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="#FFFF99">Sign in as a different user</font></a>~;
}

print qq~
					</td></tr>
					<tr><td colspan="2" bgcolor="#CC3300">&nbsp;</td></tr>
					</table>
				</td>
			</tr>
			</table>
		</td>
	</tr>
	</form>
	</table>
</div>
~;
&printTail;
