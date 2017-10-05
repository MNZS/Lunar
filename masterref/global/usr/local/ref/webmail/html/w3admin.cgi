#!/usr/bin/perl
# W3Mail - A webbased application to recieve POP3 mail and send e-mail via SMTP.
# Copyright (C) 2000  Spencer Miles
#

use CGI qw/:standard/;
use CGI::Carp qw(fatalsToBrowser);

require 'w3mail.conf';
require 'w3vars.cgi';

&initPage;

$func = $form->param('func');

print "<html><body bgcolor=white>\n";

if ($func eq "") {

	print qq~
	<head><title>W3Mail Configuration Login</title></head>
	<center>
	<form method="post" action="$cgidir/w3admin.cgi" name="login">
	<input type=hidden name=func value=conf>
	<table border=0 cellpadding=1 cellspacing=0 bgcolor=black width=40%><tr><td>
	<table width=100% border=0 cellspacing=1 cellpadding=3 bgcolor=#fffffg>
	<tr><td bgcolor=$table_bg colspan=2><font size=+2>W3Mail Configuration</font><font size=+1> (Please Login)</font></td></tr>
	<tr><td bgcolor=$table_head>Username:</td><td bgcolor=$table_bg><input name="user"></td></tr>
	<tr><td bgcolor=$table_head>Password:</td><td bgcolor=$table_bg><input name="pass" type="password"></td></tr>
	<tr><td bgcolor=$table_bg colspan=2><input type=submit value=Submit></td></tr>
	</table></td></tr></table>
	</form>
	</center>
	~;
}



if ($func eq "conf") {
	$user = $form->param('user');
	$pass = $form->param('pass');
   
	if ( $user eq $adminuser && $pass eq $adminpass && $pass ne "") {
		print qq~
		<head><title>W3Mail Configuration</title></head>
		<form method=\"post\" action=\"$cgidir/w3admin.cgi\">
		<input type=hidden name=func value=modify>
		<input type=hidden name=tail value=\"$tail\">
		<center><table border=0 cellpadding= cellspacing=0 bgcolor="#000000" width=70%>
		<tr bgcolor="#000000"><td>
		<table width=100% border=0 cellspacing=1 cellpadding=3 bgcolor=#fffffg>
		<tr><td colspan=2><font size=+2>W3Mail Configuration</font></td></tr>
		~;
		my $num_servers = scalar(@mailservers);
		for ($i = 0; $i < $num_servers; $i++) {
			my $mailserverreplyto = @mailserver_replyto[$i];
			my $num = $i+1;
			print "<tr><td width=30% bgcolor=$table_head>POP3 Server $num:</td><td bgcolor=$table_bg><input size=30 name=pop3 value=\"@mailservers[$i]\"></td></tr>\n";
			print "<tr><td bgcolor=$table_head>Reply-To Server $num:</td><td bgcolor=$table_bg><input size=30 name=reply value=\"$mailserverreplyto\"></td></tr>\n";
		}
	
		print qq~
		<tr><td bgcolor=$table_head>SMTP Server:</td><td bgcolor=$table_bg><input size=30 name=smtp value=$smtpserv></td></tr>
		<tr><td bgcolor=$table_head>CGI Directory:</td><td bgcolor=$table_bg><input size=30 name=cgi value=$cgidir></td></tr>
		<tr><td bgcolor=$table_head>MIME Temp Directory:</td><td bgcolor=$table_bg><input size=30 name=mime value=$mimedir></td></tr>
		<tr><td bgcolor=$table_head>MIME HTTP directory:</td><td bgcolor=$table_bg><input size=30 name=mimehttp value=$mimehttp></td></tr>	
		<tr><td bgcolor=$table_head>Images HTTP directory:</td><td bgcolor=$table_bg><input size=30 name=imageshttp value=$imageshttp></td></tr>
		<tr><td bgcolor=$table_head>Homepage:</td><td bgcolor=$table_bg><input size=30 name=homepage value=$homepage></td></tr>
		<tr><td bgcolor=$table_head>Admin Username:</td><td bgcolor=$table_bg><input size=30 name=username value=$adminuser></td></tr>	
		<tr><td bgcolor=$table_head>Admin Password:</td><td bgcolor=$table_bg><input size=30 name=password value=$adminpass></td></tr>
		<tr><td bgcolor=$table_head>User Data Directory:</td><td bgcolor=$table_bg><input size=30 name=data value=$datadir></td></tr>
		<tr><td bgcolor=$table_bg colspan=2><font>Colors and System Settings</font></td></tr>
		<tr><td bgcolor=$table_head>Style Sheet:</td><td bgcolor=$table_bg><input size=30 name=style value=$style></td></tr>	
		<tr><td bgcolor=$table_head>Background:</td><td bgcolor=$table_bg><input size=30 name=background value=$bgcolor></td></tr>
		<tr><td bgcolor=$table_head>Link:</td><td bgcolor=$table_bg><input size=30 name=link value=$link></td></tr>
		<tr><td bgcolor=$table_head>Visited Link:</td><td bgcolor=$table_bg><input size=30 name=visited value=$vlink></td></tr>
		<tr><td bgcolor=$table_head>Active Link:</td><td bgcolor=$table_bg><input size=30 name=active value=$alink></td></tr>
		<tr><td bgcolor=$table_head>IE Hover:</td><td bgcolor=$table_bg><input size=30 name=hover value=$hover></td></tr>
		<tr><td bgcolor=$table_head>Table Header:</td><td bgcolor=$table_bg><input size=30 name=head value=$table_head></td></tr>
		<tr><td bgcolor=$table_head>Table Background:</td><td bgcolor=$table_bg><input size=30 name=tablebg value=$table_bg></td></tr>
		<tr><td bgcolor=$table_head>Table Row Dark:</td><td bgcolor=$table_bg><input size=30 name=bgdark value=$bg_dark></td></tr>
		<tr><td bgcolor=$table_head>Table Row Light:</td><td bgcolor=$table_bg><input size=30 name=bglight value=$bg_light></td></tr>
		<tr><td bgcolor=$table_head>Messages Per Page:</td><td bgcolor=$table_bg><input size=30 name=messages value=$show_messages></td></tr>

		<tr><td bgcolor=$table_head>Default Signature:</td><td bgcolor=$table_bg><input size=30 name=def_signature value=\"$def_signature\"></td></tr>	
		<tr><td bgcolor=$table_head>Admin E-Mail Address:</td><td bgcolor=$table_bg><input size=30 name=adminEmail value=$adminEmail></td></tr>	

		<tr><td bgcolor=$table_bg colspan=2><input type=submit value=\"Submit Changes\"></td></tr>
		</table></td></tr></table></form>
		~;
	} else {
		print qq~
		<head><META HTTP-EQUIV=\"REFRESH\" CONTENT=\"2; URL=$cgidir/w3admin.cgi\"></head>
		Incorrect Username or Password.<br>
		You are now being returned to the login prompt.
		~;

	}
}

if ($func eq "modify") {
	@pop3 = $form->param('pop3');
	@reply = $form->param('reply');
	$smtp = $form->param('smtp');
	$cgi = $form->param('cgi');
	$mime = $form->param('mime');
	$mimehttp = $form->param('mimehttp');
	$username = $form->param('username');
	$password = $form->param('password');
	$data = $form->param('data');
	$tail = $form->param('tail');
	$background = $form->param('background');
	$link = $form->param('link');
	$visited = $form->param('visited');
	$active = $form->param('active');
	$hover = $form->param('hover');
	$head = $form->param('head');
	$tablebg = $form->param('tablebg');
	$bgdark = $form->param('bgdark');
	$bglight = $form->param('bglight');
	$messages = $form->param('messages');
	$imageshttp = $form->param('imageshttp');
	$style = $form->param('style');
	$adminEmail = $form->param('adminEmail');
	$def_signature = $form->param('def_signature');
	$homepage = $form->param('homepage');
	$adminEmail =~ s/(@)/\\@/g;
	$def_signature =~ s/(@)/\\@/g;
	
   $subject =~ s/[^$OK_CHARS]//go;
      $smtp =~ s/[^$OK_CHARS]//go;
      $cgi =~ s/[^$OK_CHARS]//go;
      $mime =~ s/[^$OK_CHARS]//go;
      $mimehttp =~ s/[^$OK_CHARS]//go;
      $username =~ s/[^$OK_CHARS]//go;
      $password =~ s/[^$OK_CHARS]//go;
      $data =~ s/[^$OK_CHARS]//go;
      $tail =~ s/[^$OK_CHARS]//go;
      $background =~ s/[^$OK_CHARS]//go;
      $link =~ s/[^$OK_CHARS]//go;
      $visited =~ s/[^$OK_CHARS]//go;
      $active =~ s/[^$OK_CHARS]//go;
      $hover =~ s/[^$OK_CHARS]//go;
      $head =~ s/[^$OK_CHARS]//go;
      $tablebg =~ s/[^$OK_CHARS]//go;
      $bgdark =~ s/[^$OK_CHARS]//go;
      $bgligh =~ s/[^$OK_CHARS]//go;
      $messages =~ s/[^$OK_CHARS]//go;
      $imageshttp =~ s/[^$OK_CHARS]//go;
      $style =~ s/[^$OK_CHARS]//go;
      $adminEmail =~ s/[^$OK_CHARS]//go;
      $def_signature =~ s/[^$OK_CHARS]//go;
      $homepage =~ s/[^$OK_CHARS]//go;
  
   
	open(OUT, ">w3mail.conf") || die "Cannot open file for output";
		
		print OUT "\@mailservers = (";
		foreach (@pop3) {
		print OUT "\"$_\",";
		}
		print OUT ")\;\n";

		print OUT "\@mailserver_replyto = (";
		foreach (@reply) {
		print OUT "\"$_\",";
		}
		print OUT ")\;\n";
		
		print OUT "\$smtpserv = \"$smtp\"\;\n";
		print OUT "\$cgidir = \"$cgi\"\;\n";
		print OUT "\$mimedir = \"$mime\"\;\n";
		print OUT "\$mimehttp = \"$mimehttp\"\;\n";
		print OUT "\$imageshttp = \"$imageshttp\"\;\n";
		print OUT "\$homepage = \"$homepage\"\;\n";
		print OUT "\$tail = \"$tail\"\;\n";
		print OUT "\$adminuser = \"$username\"\;\n"; 
		print OUT "\$adminpass = \"$password\"\;\n";
		print OUT "\$datadir = \"$data\"\;\n";
		print OUT "\n";
		print OUT "\$style = \"$style\"\;\n";
		print OUT "\$bgcolor = \"$background\"\;\n";
		print OUT "\$link = \"$link\"\;\n";
		print OUT "\$vlink = \"$visited\"\;\n";
		print OUT "\$alink = \"$active\"\;\n";
		print OUT "\$hover = \"$hover\"\;\n";
		print OUT "\n";
		print OUT "\$table_head = \"$head\"\;\n";
		print OUT "\$table_bg = \"$tablebg\"\;\n";
		print OUT "\$bg_dark = \"$bgdark\"\;\n";
		print OUT "\$bg_light = \"$bglight\"\;\n";
		print OUT "\$show_messages = \"$messages\"\;\n";
		print OUT "\n";
		print OUT "\$def_signature = \"$def_signature\"\;\n";
		print OUT "\$adminEmail = \"$adminEmail\"\;\n";
		print OUT "\$columns = \"75\"\;\n";
		print OUT "\$post_max = \"950\"\;\n";
		print OUT "\$system_rm = \"\/bin\/rm\"\;\n";
		print OUT "\$maxpost = \"100\"\;\n";
	close(OUT);
	print "<head><META HTTP-EQUIV=\"REFRESH\" CONTENT=\"2; URL=$cgidir/login.cgi\"></head>\n";
	$message = "Your W3Mail changes have been saved to w3mail.conf.";
	print qq~
    <div align="center">
     <table border="0" cellpadding="1" cellspacing="0" bgcolor="#000000">
      <tr>
       <td>
        <table width="100%" border="0" cellspacing="1" cellpadding="10">
         <tr>
          <td bgcolor="$bg_dark">
           <b>$message</b>
          </td>
         </tr>
         <tr>
          <td bgcolor="$bg_light">
           <font size="-2" face="Geneva, Arial, Helvetica">
	    You are now being returned to W3Mail Login.<br>
	    If your browser does not support redirecting, please click <a href="$cgidir/login.cgi">here</a> to return to W3Mail.
            </font>
          </td>
         </tr>
        </table>
       </td>
      </tr>
     </table>
    </div>
	~;
}
&printTail;
