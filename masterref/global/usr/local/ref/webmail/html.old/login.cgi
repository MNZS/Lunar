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
 <table border="0" cellpadding="1" cellspacing="0" bgcolor="#000000">
  <form method="post" action="$cgidir/inbox.cgi" name="login">
   <input type="hidden" name="SessionID" value="$SessionID">
   <input type="hidden" name="isLogin" value="1">
   <tr>
     <td bgcolor="$bg_light"><b>W3Mail Login</b></td>
   </tr>
   <tr>
     <td>
        <table width="100%" border="0" cellspacing="1" cellpadding="10">
	  <tr>
	     <td bgcolor="$bg_dark"><font><b>Mail Server:</b></font></td>
	     <td bgcolor="$bg_light">
	      <select name="mailserv">
~;

for ($i = 0; $i <= $#mailservers; $i++) {
   if(@mailservers[$i] eq $serverName) {
   print qq~
	       <option value="@mailservers[$i]" selected>@mailservers[$i]
   ~;
   } else {
   print qq~
	       <option value="@mailservers[$i]">@mailservers[$i]
   ~;
   }   
}

print qq~
	      </select>
	     </td>
	   </tr>
	   <tr>
             <td bgcolor="$bg_dark"><b>Username:</b></td>
	     <td bgcolor="$bg_light">
~;
if( $loginName && $serverName ) {
   print qq~ <input type="hidden" name="user" value="$loginName">$loginName~;
} else {
   print qq~ <input name="user" size=10"> ~;
}
print qq~
	     </td>
	   </tr>
           <tr>
	     <td bgcolor="$bg_dark"><b>Password:</b></td>
	     <td bgcolor="$bg_light"><input name="pass" type="password"></td>
	   </tr>

	   <tr bgcolor="$bg_light">
	     <td colspan="2">
	       <table border="0" cellspacing="0" cellpadding="0" width="100%">
		<noscript>
					<tr>
						<td bgcolor="#000000" colspan="2">
							<font size="+1" color="#FFFF00">
							<b>You have to enable javascript in<br>
							your browsers preferences while using<br>
							W3Mail!
							</font>
						</td>
					</tr>
					</noscript>
					<tr>
						<td align="left"><input type="submit" value="Login"></td>
						<td align="right">&nbsp;
~;
if( !$loginName && !$serverName ) {
   print "<input name=\"cookies\" type=\"checkbox\"><font size=\"-1\">Remember my id on this computer</font></input></td>"
} else {
   print qq~ <a href="./login.cgi?cookies=off&user=$loginName&server=$serverName">Sign in as a different user</a>~;
}
print qq~
					</tr>
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
