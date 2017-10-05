#!/usr/bin/perl
use MIME::Base64;
$OK_CHARS='-a-zA-Z0-9_.@~$<>(){}!#%^&*[]:?=+\n\\\/, '; # Filter characters besides these

sub initPage {
	$form = new CGI;
	$CGI::POST_MAX=$maxpost * 100; # Max 100k posts
	# Retreive form fields...
   $isLogin = $form->param('isLogin');
   $cookies = $form->param('cookies');
   $mailserv = $form->param('mailserv');
	$user = $form->param('user');
	$SessionID = $form->param('SessionID');
   
   if( $isLogin eq "1" && $cookies eq "on") {
   #Send Cookies
      #print "Logging in...";
      $nameCookie = new CGI::Cookie(-name=>'name',
                                -value=>$user,
                                -path=>$cgidir,
                                -expires=>'+1M');
      $serverCookie = new CGI::Cookie(-name=>'server',
                                -value=>$mailserv,
                                -path=>$cgidir,
                                -expires=>'+1M');
      print header(-cookie=>[$nameCookie,$serverCookie],
                   -type=>"text/html"); 
   } else {
      print CGI::header(-type => "text/html");
   }
			
	&printHeader;		
	

	if ($form->param('pass')) {
		$pass = $form->param('pass');
	}
   $mailserv =~ s/[^$OK_CHARS]//go;
   $user =~ s/[^$OK_CHARS]//go;
   $SessionID =~ s/[^$OK_CHARS]//go;
   $pass =~ s/[^$OK_CHARS]//go;
	&testtm;


}
	
sub createSession {
	$isLogin = $form->param('isLogin');
   $isLogin =~ s/[^$OK_CHARS]//go;

	# Check for required directories

	if (!opendir(DATADIR, "$datadir")) {
		mkdir("$datadir", 0700);
		
		if (!opendir(DATADIR, "$datadir")) {
			$errorMessage = qq~
			<b>W3Mail directory error.</b><br>
			Directory $datadir could not be created.<br>
			~;
			&generateError;
		}
	}
	if (!opendir(MIMEDIR, "$mimedir")) {
		mkdir("$mimedir", 0700);
		
		if (!opendir(USERDIR, "$mimedir")) {
            $errorMessage = qq~
            <b>Mime directory error.</b><br>
            Directory $mimedir could not be created.
            ~;
            &generateError;
           }
	}

	if ($isLogin eq "1") {
		$pass = $form->param('pass');
      $pass =~ s/[^$OK_CHARS]//go;

		if ($pass eq "") {
			$errorMessage = qq~
			<b>Error: Incorrect password.</b><br>
			~;
			&generateError;
		}	
		$encpass = encode_base64($pass);
		chomp($encpass);
		&pop3connect;

		# Check for user and mailserver directories
		if (!opendir(MAILDIR, "$datadir/$mailserv")) {
			mkdir("$datadir/$mailserv", 0700);
			
			if (!opendir(MAILDIR, "$datadir/$mailserv")) {
				$errorMessage = qq~
				<b>W3Mail directory error.</b><br>
				Mailserver directory $datadir/$mailserv could not be created.<br>
				~;
				&generateError;
			}
		}
		if (!opendir(USERDIR, "$datadir/$mailserv/$user")) {
			mkdir("$datadir/$mailserv/$user", 0700);
			
			if (!opendir(USERDIR, "$datadir/$mailserv/$user")) {
				$errorMessage = qq~
				<b>W3Mail directory error.</b><br>
				User directory $datadir/$mailserv/$user could not be created.<br>
				~;
				&generateError;
			}
		}
		
		if (!-e "$datadir/$mailserv/$user/folders") {
			open(OUT, ">$datadir/$mailserv/$user/folders") || die "Couldn't open file";
			print OUT "Outbox,outbox\n";
			print OUT "Inbox,inbox\n";
			close OUT;
			if (!-e "$datadir/$mailserv/$user/folders") {
				$errorMessage = "<b>W3Mail file error.</b><br>$datadir/$mailserv/$user/folders.xml could not be created.<br>";
				&generateError;
			}
		}
		if (!opendir(OUTBOX, "$datadir/$mailserv/$user/outbox")) {
			mkdir("$datadir/$mailserv/$user/outbox", 0700);
			
			if (!opendir(USERDIR, "$datadir/$mailserv/$user/outbox")) {
				$errorMessage = qq~
				<b>W3Mail directory error.</b><br>
				Sent-items directory $datadir/$mailserv/$user/outbox could not be created.<br>
				~;
				&generateError;
			}
		}
		
		# Run preferences if user has no preferences
		if (! -e "$datadir/$mailserv/$user/info") {
			&getReplyto;
			&preferences;
		}

		if ($pop->Message() =~ /^\+OK/) {
			require "$datadir/$mailserv/$user/info";
			&login;
		}
      

		&constVars;
	}
	if (!$isLogin) {
		require "$datadir/$mailserv/$user/info";
		$pass = decode_base64($encpass);
		&checkID;
		&pop3connect;
		&constVars;
	}
}

sub testtm {
	open(FILE,decode_base64("dzNtYWlsLmxpYw=="));
	$key = decode_base64(<FILE>);
	@keys = split(/\|/,$key);
	my @exp = split(/:/,$keys[1]);
	$exp = @exp[1];
#	if($exp ne decode_base64("bmV2ZXI=")) {
#		&epx if $exp - time() < 0;
#	}
}

sub generateError {
	print qq~
    <div align="center">
     <table border="0" cellpadding="1" cellspacing="0">
      <tr>
       <td>
        <table width="100%" border="0" cellspacing="1" cellpadding="10">
         <tr>
          <td bgcolor="$bg_dark">
           <font size="+1" face="Geneva, Arial, Helvetica">$errorMessage<br>
           Please contact your <a href=mailto:$adminEmail?subject=W3Mail>System Administrator</a></font> <font size="-1">($adminEmail)</font>
          </td>
         </tr>
         <tr>
          <td bgcolor="$bg_light">
           <font size="-2" face="Geneva, Arial, Helvetica">
            If your browser does not support redirecting, please click <a href="$cgidir/login.cgi">here</a> to go back and try again.</font>
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
}

sub generateMessage {
	print qq~
	<meta HTTP-EQUIV="refresh" content="1; URL=$cgidir/inbox.cgi?mailserv=$mailserv&user=$user&SessionID=$SessionID">
    <div align="center">
     <table border="0" cellpadding="1" cellspacing="0">
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
	    You are now being returned to your Inbox.<br>
	    If your browser does not support redirecting, please click <a href="$cgidir/inbox.cgi?mailserv=$mailserv&user=$user&SessionID=$SessionID">here</a> to return to your inbox.
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
}

#sub redirectLogin {
#	$metatag = qq~<meta HTTP-EQUIV="refresh" content="5; URL=$cgidir/login.cgi">~;
#	&printHeader;
#}		                                                                                                                                                                                                

sub login {
	$replyto =~ s/(@)/\\@/g;
	$sig =~ s/(@)/\\@/g;
  	$name =~ s/(@)/\\@/g;
   
	open(OUT, ">$datadir/$mailserv/$user/info") || die "Cannot open file for output";
	print OUT "\$name = \"$name\"\;\n";
	print OUT "\$sig = \"$sig\"\;\n";
	print OUT "\$show_messages = \"$show_messages\"\;\n";
	print OUT "\$table_head = \"$table_head\"\;\n";
	print OUT "\$table_bg = \"$table_bg\"\;\n";
	print OUT "\$bg_dark = \"$bg_dark\"\;\n";
	print OUT "\$bg_light = \"$bg_light\"\;\n";
	print OUT "\$replyto = \"$replyto\"\;\n";	
	print OUT "\$encpass = \"$encpass\"\;\n";
	print OUT "\$SessionID = \"$SessionID\"\;\n";
#	print OUT "\$login = \"1\"\;\n";
	
	print OUT "1\;\n";
	close(OUT);
                       
   $name =~ s/(\\@)/@/g;
   $replyto =~ s/(\\@)/@/g;
}

sub epx {
	print qq~
    <div align="center">
     <table border="0" cellpadding="1" cellspacing="0">
      <tr>
       <td>
        <table width="100%" border="0" cellspacing="1" cellpadding="10">
         <tr>
          <td bgcolor="$bg_dark">
           <font size="+1" face="Geneva, Arial, Helvetica">Your version of W3Mail has expired.  To continue using W3Mail you must purchase the software at <a href="http://www.cascadesoft.com/">http://www.cascadesoft.com</a>.<br></font>
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
}

sub logout {
	$replyto =~ s/(@)/\\@/g;
	$sig =~ s/(@)/\\@/g;
	$name =~ s/(@)/\\@/g;
   
	open(OUT, ">$datadir/$mailserv/$user/info") || die "Cannot open file for output";
	print OUT "\$name = \"$name\"\;\n";
	print OUT "\$sig = \"$sig\"\;\n";
	print OUT "\$show_messages = \"$show_messages\"\;\n";
	print OUT "\$table_head = \"$table_head\"\;\n";
	print OUT "\$table_bg = \"$table_bg\"\;\n";
	print OUT "\$bg_dark = \"$bg_dark\"\;\n";
	print OUT "\$bg_light = \"$bg_light\"\;\n";
	print OUT "\$replyto = \"$replyto\"\;\n";	
	
#	print OUT "\$login = \"0\"\;\n";
	
	print OUT "1\;\n";
	close(OUT);
}

sub pop3connect {
	$pop = new Mail::POP3Client( USER     => "$user",
	AUTH_MODE => 'PASS',
#	DEBUG => 1,
	PASSWORD => "$pass",
	HOST     => "$mailserv");
	if ($pop->Message() !~ /^\+OK/) {
		$message = $pop->Message();
		$errorMessage = qq~
		<b>Incorrect username or password.</b><br>
		~;
		&generateError;
	}		
}

sub sessionid {
	my @numbers = ('1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f');
	
	srand();
	for ($i=0; $i<8; $i++) {
		$SessionID .= "$numbers[int rand @numbers]";
	}
}

sub checkID {
	if ($SessionID ne $form->param('SessionID')) {
		$errorMessage = qq~
		<b>Your session has terminated.  Please re-login</b><br>
		~;
		&generateError;
	}
}

sub printTail {

	if (open(FILE, "html.end")) {
		while (<FILE>) {
			s/%%bgcolor%%/$bgcolor/g;
			s/%%imageshttp%%/$imageshttp/g;
			print "$_";
		}
	}
}


sub printHeader {

	if (open(FILE, "html.top")) {
		if (!$replyto) {
			$replyto = "$user\@$mailserv_replyto";
		}
		while (<FILE>) {
			if (@_[0] eq "login") {
				s/%%onload%%/onload="document.login.user.focus()"/g;
			} else {
				s/%%onload%%//g;
			}	
			
			s/%%replyto%%/$replyto/g;
			s/%%link%%/$link/g;
			s/%%alink%%/$alink/g;
			s/%%vlink%%/$vlink/g;
			s/%%bgcolor%%/$bgcolor/g;
			s/%%imageshttp%%/$imageshttp/g;
			s/%%metatag%%/$metatag/g;
			s/%%css%%/$style/g;
			print "$_";
		}
	}
}

sub preferences {
	if(-e "$datadir/$mailserv/$user/info") {
		require "$datadir/$mailserv/$user/info";
	} else {
		require "w3mail.conf";
		if ($def_signature) {
			$sig = $def_signature;
		}
	}
	

	print qq~
	<script language=javascript>
		function OpenAddressbook() {
			var addressWindow = window.open("addressbook.cgi?mailserv=$mailserv&user=$user&SessionID=$SessionID&edit=yes","AddressBook","width=600,height=450,resizable=yes,scrollbars=yes");
		}
	</script>

   <script>
    function colorChange(_spanID) {
      theColor = document.forms['prefs'].elements[_spanID].value;
      document.getElementById(_spanID).style.backgroundColor=theColor;
  }
</script>


   
	<div align="center">
     <form method=post action="$cgidir/prefs.cgi" name="prefs">
      <table border="0" cellpadding="1" cellspacing="0" width="95%">
       <tr bgcolor="$bg_light">
	    <td width="50%" align="left" valign="bottom">
	     <img src="$imageshttp/title_prefs.gif" width="162" height="19" border="0" alt="Preferences">
	    </td>
		<td width="50%" align="right" valign="bottom">
		 <font face="Geneva, Arial, Helvetica"><b>($replyto)</b></font>
		</td>
	   </tr>
	   <tr>
		<td colspan="2">
	~;
	print &constVars;
	print qq~
		 <input type=hidden name=encpass value=$encpass>
		 <input type=hidden name=func value=postprefs>
		 <table width="100%" border="0" cellspacing="1" cellpadding="4">
		  <tr bgcolor="$bg_dark">
		   <td colspan="2">
	~;
	
	# Check existing preferences
	if (-e "$datadir/$mailserv/$user/info") {
	print qq~
			 <table border="0" cellspacing="0" cellpadding="0" width="100%">
			  <tr>
			   <td width="50%" align="left">
				<img src="$imageshttp/dot_clear.gif" width="10" height="1" border="0">
				<a href="$cgidir/inbox.cgi?mailserv=$mailserv&user=$user&SessionID=$SessionID" onMouseOver="window.status='Return to Inbox';return true"><img src="$imageshttp/checkmail.gif" width="23" height="20" border="0" alt="Inbox"></a>
				<img src="$imageshttp/dot_clear.gif" width="10" height="1" border="0">
				<a href="$cgidir/compose.cgi?mailserv=$mailserv&user=$user&SessionID=$SessionID" onMouseOver="window.status='Compose a new message';return true"><img src="$imageshttp/msg_new.gif" width="23" height="20" border="0" alt="Compose Message"></a>&nbsp;&nbsp;
			   </td>
			   <td width="50%" align="right">
				<a href="javascript:OpenAddressbook()" onMouseOver="window.status='Open Addressbook';return true"><img src="$imageshttp/addressbook.gif" width="23" height="20" border="0" alt="Addressbook"></a>&nbsp;&nbsp;
				<img src="$imageshttp/dot_clear.gif" width="10" height="1" border="0">
				<a href="$cgidir/prefs.cgi?mailserv=$mailserv&user=$user&SessionID=$SessionID&func=modify" onMouseOver="window.status='Modify your Preferences';return true"><img src="$imageshttp/prefs.gif" width="23" height="20" border="0" alt="Preferences"></a>&nbsp;&nbsp;
				<img src="$imageshttp/dot_clear.gif" width="10" height="1" border="0">
				<a href="$cgidir/logout.cgi?mailserv=$mailserv&user=$user&SessionID=$SessionID" onMouseOver="window.status='Logout';return true"><img src="$imageshttp/logout.gif" width="23" height="20" border="0" alt="Logout"></a>
				<img src="$imageshttp/dot_clear.gif" width="10" height="1" border="0">
			   </td>
			  </tr>
			 </table>
	~;
	} else {
	print qq~
			 <table border="0" cellspacing="0" cellpadding="0" width="100%">
			  <tr valign=top>
			   <td align="left" width="92%" bgcolor="#CC3300">
			    <b><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="#FFFF99">Welcome!  Since this is your first time logging into WebMail please fill out the following preferences.</b></font>
			   </td>
			   <td align="right" width="8%" bgcolor="#CC3300">
				<a href="$cgidir/login.cgi"><img src="$imageshttp/logout.gif" width="23" height="20" border="0" alt="exit"></a>
				<img src="$imageshttp/dot_clear.gif" width="10" height="1" border="0">
			   </td>
			  </tr>
			 </table>
	~;
	}
	print qq~
			</td>
		   </tr>
		   <tr>
			<td bgcolor="$bg_light"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="$bg_dark"><b>Name:</b></font></td>
			<td bgcolor="$bg_light"><input name="Name" value="$name"></td>
		   </tr>
		   <tr>
			<td bgcolor="$bg_light" width="25%"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="$bg_dark"><b>Reply-To Address:</font></td>
			<td bgcolor="$bg_light"><input name="replyto" value="$replyto"></td>
		   </tr>	
		   <tr>
			<td bgcolor="$bg_light" valign="top"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="$bg_dark"><b>Signature:</b></font></td>
			<td bgcolor="$bg_light"><textarea name="sig" rows="4" wrap="soft" cols="60">$sig</textarea></td>
		   </tr>
		   <tr>
			<td bgcolor="$bg_light"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2" color="$bg_dark"><b>Messages Per Page:</b></font></td>
			<td bgcolor="$bg_light"><input name="messages" value="$show_messages" size=4></td>
		   </tr>
~;

# 		   <tr>
#			<td bgcolor="$bg_dark" colspan="2"><font face="Geneva, Arial, Helvetica" size="+2">Colors</font></td>
#		   </tr>
#		   <tr>
#			<td bgcolor="$bg_dark"><font face="Geneva, Arial, Helvetica">Table Head Color:</font></td>
#			<td bgcolor="$bg_light"><input name="tablehead" value="$table_head" size="12" onBlur="colorChange('tablehead')"><div id="tablehead" style="background-color:#$table_head;border:1px solid black;width:65px">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div></td>
#		   </tr>	
#		   <tr>
#			<td bgcolor="$bg_dark"><font face="Geneva, Arial, Helvetica">Toolbar Color:</font></td>
#			<td bgcolor="$bg_light"><input name="tablebg" value="$table_bg" size="12" onBlur="colorChange('tablebg')"><div id="tablebg" style="background-color:#$table_bg;border:1px solid black;width:65px">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div></td>
#		   </tr>	
#		   <tr>
#			<td bgcolor="$bg_dark"><font face="Geneva, Arial, Helvetica">Dark Row Color:</font></td>
#			<td bgcolor="$bg_light"><input name="bgdark" value="$bg_dark" size="12" onBlur="colorChange('bgdark')"><div id="bgdark" style="background-color:#$bg_dark;border:1px solid black;width:65px">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div></td>
#		   </tr>	
#		   <tr>
#			<td bgcolor="$bg_dark"><font face="Geneva, Arial, Helvetica">Light Row Color:</font></td>
#			<td bgcolor="$bg_light"><input name="bglight" value="$bg_light" size="12" onBlur="colorChange('bglight')"><div id="bglight" style="background-color:#$bg_light;border:1px solid black;width:65px">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div></td>
#		   </tr>	

print qq~
		   <tr>
			<td bgcolor="$bg_light" colspan="2"><input type="submit" value="Submit"></td>
		   </tr>
		   </table>
	      </td>
         </tr>
        </table>
	   </form>
      </div>
	~;
	&printTail;
	exit;
	}

sub postPrefs {
	$name = $form->param('Name');
	$sig = $form->param('sig');
	$show_messages = $form->param('messages');
	$table_head = $form->param('tablehead');
	$table_bg = $form->param('tablebg');
	$bg_dark = $form->param('bgdark');
	$bg_light = $form->param('bglight');
	$replyto = $form->param('replyto');
	$encpass = $form->param('encpass');
	$SessionID = $form->param('SessionID');
         $name =~ s/[^$OK_CHARS]//go;
      $sig =~ s/[^$OK_CHARS]//go;
      $show_messages =~ s/[^$OK_CHARS]//go;
      $table_head =~ s/[^$OK_CHARS]//go;
      $table_bg =~ s/[^$OK_CHARS]//go;
      $bg_dark =~ s/[^$OK_CHARS]//go;
      $bg_light =~ s/[^$OK_CHARS]//go;
      $replyto =~ s/[^$OK_CHARS]//go;
      $encpass =~ s/[^$OK_CHARS]//go;
      $SessionID =~ s/[^$OK_CHARS]//go;

	$sig_parse = $sig;
	$sig_parse =~ s/\\/\\\\/g;
	$sig_parse =~ s/@/\\\@/g;
	$sig_parse =~ s/"/\\\"/g;
	$sig_parse =~ s/\n/\\n/g;
	$sig = $sig_parse;
	$replyto =~ s/(@)/\\@/g;
	$name =~ s/(@)/\\@/g;
   
open(OUT, ">$datadir/$mailserv/$user/info") || die "Cannot open file for output";
	print OUT "\$name = \"$name\"\;\n";
	print OUT "\$sig = \"$sig\"\;\n";
	print OUT "\$show_messages = \"$show_messages\"\;\n";
	print OUT "\$table_head = \"$table_head\"\;\n";
	print OUT "\$table_bg = \"$table_bg\"\;\n";
	print OUT "\$bg_dark = \"$bg_dark\"\;\n";
	print OUT "\$bg_light = \"$bg_light\"\;\n";
	print OUT "\$encpass = \"$encpass\"\;\n";
	print OUT "\$replyto = \"$replyto\"\;\n";
	print OUT "\$SessionID = \"$SessionID\"\;\n";
	
	print OUT "1\;\n";
	close(OUT);

}

	                                                                                                                                                                                                
sub getReplyto {
	if ($#mailservers > 0) {
		foreach ( @mailserver_replyto ) {
			$mailserv_replyto = $_ if ( $mailserv =~ /$_/ );
		}
	} else {
		$mailserv_replyto = @mailserver_replyto[0];
	}
	$replyto = "$user\@$mailserv_replyto";
	return $mailserv_replyto;
}

sub constVars {
	$const_vars = qq~
	<input type=Hidden Name="mailserv" value="$mailserv">
	<input type=hidden name="user" value="$user">
    	<input type=hidden name="SessionID" value="$SessionID"> 
    ~;
	return $const_vars;
}

sub message_size {
	$size = $pop->List($_[0]);

	$size =~ s/\d+\s//i;
	if ($size < 1024) {
		print $size;
		print "bytes";
	}
	if ($size >= 1024) {
		$size = int($size/1024);
		print "$size kb";
	}
}

sub parse_date {
	$date_tmp = $_[0];
	if ($date_tmp =~ /[,]/) {
		$date_tmp =~ s/(\w+),\s(\d+)\s(\w+)\s(\d+)\s(\d+:\d+):\d+//i;
		$day = $2;
		$month = $3;
		$year = $4;
		$time = $5;
		if ($month && $day) {
			print qq~$month&nbsp;$day&nbsp;$year&nbsp;$time~;
		} else {
			print "No Date";
		}
	} else {
		$date_tmp =~ s/(\w+)\s(\d+)\s(\w+)\s(\d+)\s(\d+:\d+):\d+//i;
		$day = $2;
		$month = $3;
		$year = $4;
		$time = $5;
		if ($month && $day) {
			print qq~$month&nbsp;$day&nbsp;$year&nbsp;$time~;
		} else {
			print "No Date";
		}
	}
}

sub userAttachments {
	open (OUT, ">>$datadir/$mailserv/$user/attachments");
		print OUT "$mimedir/$file\n";
	close (OUT);
}

sub inboxBar {

print qq~
  <tr bgcolor="$table_bg"> 
    <td colspan="2" valign="top" nowrap> 
		<a href="javascript:checkorUncheck(true)" onMouseOver="return wstatus('Select All Messages for Delete')" onMouseOut="window.status='';return true"><img src="$imageshttp/select_all.gif" width="23" height="20" border="0" alt="Select All Messages"></a>
		<a href="javascript:checkorUncheck(false)" onMouseOver="return wstatus('Deselect All Messages for Delete')" onMouseOut="window.status='';return true"><img src="$imageshttp/select_nothing.gif" width="23" height="20" border="0" alt="Deselect All Messages"></a>
		<input type="image" value="Delete" name="Delete Selected Messages" src="$imageshttp/msg_delete.gif" width="23" height="20" border="0" onMouseOver="return wstatus('Delete Selected Messages')" onMouseOut="window.status='';return true" alt="Delete Selected Message"></form>
    </td>
    <td colspan="6" valign="top" nowrap>

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
		   </form></nobr>
		   </td>
		 
		 <td align=left valign=top>
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
				<td valign="top" align="right"><a href="javascript:OpenAddressbook()"><img src="$imageshttp/addressbook.gif" width="23" height="20" border="0" alt="Open Addressbook" onMouseOver="return wstatus('Open Addressbook')" onMouseOut="window.status='';return true"></form></td>

				<td valign="top" align="right">
				<form method="post" action="$cgidir/prefs.cgi">$const_vars
				<input type="hidden" name="func" value="modify">
				<img src="$imageshttp/dot_clear.gif" width="10" height="1" border="0"><input type="image" name="preferences" value="Preferences" src="$imageshttp/prefs.gif" width="23" height="20" border="0" alt="Modify your Preferences" onMouseOver="return wstatus('Modify your Preferences')" onMouseOut="window.status='';return true"></form></td>
				<td valign="top" align="right">
				<form method="post" action="$cgidir/logout.cgi">$const_vars
				<img src="$imageshttp/dot_clear.gif" width="10" height="1" border="0"><input type="image" name="logout" value="Logout" src="$imageshttp/logout.gif" width="23" height="20" border="0" alt="Logout" onMouseOver="return wstatus('Logout')" onMouseOut="window.status='';return true"><img src="$imageshttp/dot_clear.gif" width="10" height="1" border="0"></form></td>
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

sub get_date {
    ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
    $mon++;
    if ($mon < 10) { $mon = "0$mon"; }
    if ($mday < 10) { $mday = "0$mday"; }
    if ($hour < 10) { $hour = "0$hour"; }
    if ($min < 10) { $min = "0$min"; }
    if ($sec < 10) { $sec = "0$sec"; }
    $year += 1900;
    return "$mon-$mday-$year";
}

sub welcome {
		print qq~<td align="center" valign="bottom"><font face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2"><b><b>Welcome, you have $messages message(s)!</b></font><br><font><nobr>Inbox: $messages message(s). $inboxsize bytes.</nobr></font></td>~;
}

1;
