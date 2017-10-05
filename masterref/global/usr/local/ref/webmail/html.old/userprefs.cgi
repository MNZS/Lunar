#!/usr/bin/perl


sub user_prefs {
	&replyto;	### Get reply-to address
	if(-e "$datadir/$mailserv/$user/info") {
		require "$datadir/$mailserv/$user/info";
	} else {
		require "w3mail.conf";
	if ($def_signature) {
		$sig = $def_signature;
		}
	}
	
	&PrintTop;
	print qq~
<script language=javascript>
	function OpenAddressbook() {
		var addressWindow = window.open("addressbook.cgi?mailserv=$mailserv&user=$user&SessionID=$SessionID&edit=yes","AddressBook","width=600,height=450,resizable=yes,scrollbars=yes");
	}
</script>

<div align="center">
<form method=post action="$cgidir/prefs.cgi">
<table border="0" cellpadding="1" cellspacing="0" bgcolor="#000000" width="95%">
<tr bgcolor="#FFFFFF">
	<td width="50%" align="left" valign="bottom"><img src="$imageshttp/title_prefs.gif" width="162" height="19" border="0" alt="Preferences"></td>
	<td width="50%" align="right" valign="bottom"><font face="Geneva, Arial, Helvetica">&nbsp;&nbsp;&nbsp;($user\@$mailserv_replyto)</font></td>
</tr>
<tr>
	<td colspan="2">
$const_vars
~;
	if ($pass) {
		$encpass = encode_base64($pass);
		chomp($encpass);
	}

	print qq~
		<input type=hidden name=encpass value=$encpass>
		<input type=hidden name=func value=postprefs>
		<table width="100%" border="0" cellspacing="1" cellpadding="4">
		<tr bgcolor="$table_bg">
			<td colspan="2">
~;
	#Check existing preferences
	if(-e "$datadir/$mailserv/$user/info") {
	print qq~
				<table border="0" cellspacing="0" cellpadding="0" width="100%">
				<tr>
					<td width="50%" align="left">
						<img src="$imageshttp/dot_clear.gif" width="10" height="1" border="0">
						<a href="$cgidir/inbox.cgi?mailserv=$mailserv&user=$user&SessionID=$SessionID" onMouseOver="window.status='Got to Inbox';return true"><img src="$imageshttp/checkmail.gif" width="23" height="20" border="0" alt="Inbox"></a>
						<img src="$imageshttp/dot_clear.gif" width="10" height="1" border="0">
						<a href="$cgidir/compose.cgi?mailserv=$mailserv&user=$user&SessionID=$SessionID" onMouseOver="window.status='Compose a message';return true"><img src="$imageshttp/msg_new.gif" width="23" height="20" border="0" alt="Compose message"></a>&nbsp;&nbsp;
					</td>
					<td width="50%" align="right">
						<a href="javascript:OpenAddressbook()" onMouseOver="window.status='Open adressbook';return true"><img src="$imageshttp/addressbook.gif" width="23" height="20" border="0" alt="Addressbook"></a>&nbsp;&nbsp;
						<img src="$imageshttp/dot_clear.gif" width="10" height="1" border="0">
						<a href="$cgidir/prefs.cgi?mailserv=$mailserv&user=$user&SessionID=$SessionID" onMouseOver="window.status='Modify your preferences';return true"><img src="$imageshttp/prefs.gif" width="23" height="20" border="0" alt="Preferences"></a>&nbsp;&nbsp;
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
				<tr>
					<td align="right" width="100%">
						<a href="$cgidir/login.cgi"><img src="$imageshttp/logout.gif" width="23" height="20" border="0" alt="exit"></a>
						<img src="$imageshttp/dot_clear.gif" width="10" height="1" border="0">
					</td>
				</tr>
				</table>
~;
	}	
	#Go on
	print qq~
			</td>
		</tr>
		<tr>
			<td bgcolor="$bg_dark"><font face="Geneva, Arial, Helvetica">Name:</font></td>
			<td bgcolor="$bg_light"><input name="Name" value="$name"></td>
		</tr>
		<tr>
			<td bgcolor="$bg_dark" width="25%"><font face="Geneva, Arial, Helvetica">Reply-To Address:</font></td>
			<td bgcolor="$bg_light"><input name="replyto" value="$replyto"></td>
		</tr>	
		<tr>
			<td bgcolor="$bg_dark" valign="top"><font face="Geneva, Arial, Helvetica">Signature</font></td>
			<td bgcolor="$bg_light"><textarea name="sig" rows="4" wrap="soft" cols="75">$sig</textarea></td>
		</tr>
		<tr>
			<td bgcolor="$bg_dark"><font face="Geneva, Arial, Helvetica">Messages Per Page:</font></td>
			<td bgcolor="$bg_light"><input name="messages" value="$show_messages" size=4></td>
		</tr>
		<tr>
			<td bgcolor="$bg_dark" colspan="2"><font face="Geneva, Arial, Helvetica" size="+2">Colors</font></td>
		</tr>
		<tr>
			<td bgcolor="$bg_dark"><font face="Geneva, Arial, Helvetica">Table Head Color:</font></td>
			<td bgcolor="$bg_light"><input name="tablehead" value="$table_head" size="12"></td>
		</tr>	
		<tr>
			<td bgcolor="$bg_dark"><font face="Geneva, Arial, Helvetica">Toolbar Color:</font></td>
			<td bgcolor="$bg_light"><input name="tablebg" value="$table_bg" size="12"></td>
		</tr>	
		<tr>
			<td bgcolor="$bg_dark"><font face="Geneva, Arial, Helvetica">Dark Row Color:</font></td>
			<td bgcolor="$bg_light"><input name="bgdark" value="$bg_dark" size="12"></td>
		</tr>	
		<tr>
			<td bgcolor="$bg_dark"><font face="Geneva, Arial, Helvetica">Light Row Color:</font></td>
			<td bgcolor="$bg_light"><input name="bglight" value="$bg_light" size="12>"</td>
		</tr>	
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
&PrintTail;
}

1;
