#!/usr/bin/perl -w

# This version of webpublisher was created for ABTA such that 
# files will be displayed in an alphabetical order in a pattern
# of <filename> - <title tag>

use CGI;
use File::Basename;
use File::stat;
use Time::localtime;
use Cwd;

############################

## first, lets grab the domain name 
my $client_domain = (split(/\//,cwd()))[-2];

my $rootpath = "/www/$client_domain/pub/public_html/";

my $rootURL = "http://www.$client_domain/";

my $imageURL = "http://www.$client_domain/webpublisher/images2/";

my $skin = 'env';

############################
my %params;
sub parse_form {
  my $buffer;
  read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
  if (length($buffer) < 5) {
    $buffer = $ENV{QUERY_STRING};
  }
 
  my @pairs = split(/&/, $buffer);
  foreach $pair (@pairs) {
    my ($name, $value) = split(/=/, $pair);

    $value =~ tr/+/ /;
    $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
    $value =~ s/[\;\|\\ ]/ /ig;
    push(@values, $value); push(@names,$name);   
    $params{$name} = $value;
  }
}

&parse_form;
my $q = new CGI;

my @editTypes = qw(textbox link imageURL email);
###############################################
# CHANGE PASSWORD HERE.
###############################################
## Default master password is "master" and
## default slave password is "slave".
###############################################
my %passwords = ('master' => 'divacat',
		 'edit'   => 'admin');
###############################################
my $empty_q = new CGI("");

sub printLawrence {

    print <<EOF

<SCRIPT LANGUAGE = "JavaScript"><!--
function startndnav(url) {
//alert (remoteWin);
        remoteWin = window.open(url,'ndnav','toolbar=0,top=10,left=25,directories=0,status=0,menubar=0,scrollbars=yes,resizable=no,width=500,height=500');
     remoteWin.location.href = url;
        if (remoteWin.opener == null)
        remoteWin.opener = self;
        if (window.focus)
                remoteWin.focus();
     }

// -->
</SCRIPT>

<body background="images1/editorback.gif" link="#009999" vlink="#009999" alink="#009999">

<div align="center">
  <center>
  <table border="0" cellpadding="0" cellspacing="0" width="300">
    <tr>
      <td><img border="0" src="images1/env-top-left.gif" width="20" height="32"></td>
      <td background="images1/env-top-mid.gif"><img border="0" src="images1/env-title.gif"></td>
      <td><img border="0" src="images1/env-top-right.gif" width="70" height="32"></td>
    </tr>
    <tr>
      <td background="images1/env-left.gif"><img border="0" src="images1/env-left.gif" width="20" height="10"></td>
      <td background="images1/env-centre.gif" width="100%"><font face="verdana, arial" size="-1">
EOF

## end of subroutine
}

sub endLawrence {
  
    print <<EOF
</font></td>
      <td background="images1/env-right.gif"><img border="0" src="images1/env-right.gif" width="70" height="10"></td>
    </tr>
    <tr>
      <td><img border="0" src="images1/env-bot-left.gif" width="20" height="14"></td>
      <td background="images1/env-bot-mid.gif"><img border="0" src="images1/env-bot-mid.gif" width="10" height="14"></td>
      <td><img border="0" src="images1/env-bot-right.gif" width="70" height="14"></td>
    </tr>
  </table>
  </center>
</div>

<p>

<center><A HREF="javascript:parent.startndnav('https://www.$client_domain/webpublisher/directions.htm')"><img src="images1/directions.gif" border="0"></a></center>
</body>

</html>
EOF

## end of subroutine
}

sub getFile {
  my($file, $asArray) = @_;
  my @cur;
  open MYFILE, $file;
  push @cur, $_ while chomp($_ = <MYFILE>);
  close MYFILE;
  return @cur if ($asArray =~ /T/i);
  return join "\n", @cur;
}

sub printLogout {
  print $q->end_form;
  print $q->br;
  print $q->start_form(-action => 'webpublisher.cgi',
		       -method => 'POST');
  &imageButton('logout');
  print $q->end_form;
}

sub pullName {
  my($fullStr) = @_;
  my @allFiles = &getFile('upoint.txt', 'T');
  $fullStr =~ /(.*?) -/;
  my($ret) = grep /$1/, @allFiles;
  return $ret;
}

sub fileDispHash {
  my @allFiles = &getFile('upoint.txt', 'T');
  my %fileDisp;

  foreach $curFile (@allFiles) {
    my $cur = &getFile($curFile);
    $cur =~ /\<title\>(.*?)<\/title/;
    my $title = $1;
    if (length($title) > 25) {
      $title = substr($title, 0, 25) . "...";
    }
    my $shortFile = basename($curFile);

#    my $date_string = ctime(stat($curFile)->mtime);
#    $date_string =~ /[a-zA-Z]{3}\s*[0-9]+/;

    $fileDisp{$curFile} = "$shortFile - $title"; 
  }
  return %fileDisp;
}  

sub imageButton {
  my($img) = @_;
  print $q->image_button(-src => "images1/w_$img.gif");
}

sub indent {
  return "\&nbsp;" x 5;
}

do {print "Content-type: text/html\n\n";
    &printLawrence;
    print "<form action=\"webpublisher.cgi\" method=POST>";
    "<font face=\"Verdana,Arial\" size=-1>"
    } unless defined $params{'seeFile'};

if (defined $params{'password'}) {
  foreach (keys %passwords) {
    $params{'mode'} = $_ if $passwords{$_} eq $params{'password'};
  }
  if (!defined $params{'mode'}) {
    ## pull just this scripts name out
    my $link = (split(/\//, $0))[-1];

    print "Sorry ....<br>Your password was incorrect.<br>Please <a href=$link>try again</a>.";
    &endLawrence;
    exit;
  }
}

if ($params{'mode'} eq 'edit') {
  if (!defined $params{'editPage'} || defined $params{'outFromSlaveEdit'}) {
    my %fileDisp = &fileDispHash;
    
    print $q->b("<font color=#cc3300>Slave Edit Mode:</font> Pick a file to edit ...");
    print $q->br;
    print $q->popup_menu(-name => 'editPage',
			 -value => [sort values %fileDisp]);
    &imageButton('startediting');
  } else {

    my $oldName = $params{'editPage'};
    $params{'editPage'} = &pullName($params{'editPage'});

    if (defined $params{'justSlaveEdited'}) {
      my $html = &getFile($params{'editPage'});
      my $ind = 0;
      foreach (@editTypes) {
	while ($html =~ s/(\<!-- upoint type="$_".*?\>).*?(\<!-- \/upoint --\>)/!~CUR~!/s) {
	  $ind++;
	  my ($curMatch, $begMatch, $endMatch) = ($&, $1, $2);
	  if (/textbox/) {
            #charles edit
	    #$params{"textbox$ind"} =~ s/\n/\<BR\>/gis;
	    $curMatch =~ s/\>.*\<!--/\>$params{"textbox$ind"}\<!--/s;
	  } elsif (/email/) {
	    $curMatch = "$begMatch<a href=\"mailto:$params{\"emailAddr$ind\"}\">$params{\"emailDesc$ind\"}</a>$endMatch";
	  } elsif (/link/) {
	    $curMatch = "$begMatch<a href=\"$params{\"linkAddr$ind\"}\">$params{\"linkDesc$ind\"}</a>$endMatch";
	  } elsif (/imageURL/) {
	    $params{"imageURL$ind"} = $imageURL . $params{"imageURL$ind"}
	      unless ($params{"imageURL$ind"} =~ /^http\:\/\//);
	    $curMatch = "$begMatch<img src=\"$params{\"imageURL$ind\"}\" align=\"$params{\"imageURLalign$ind\"}\">$endMatch";
	  }

	  $curMatch =~ s/upoint/ALREADYupoint/;
	  $html =~ s/!~CUR~!/$curMatch/;
	}
      }

      $html =~ s/ALREADYupoint/upoint/gs;
      open EDITEDPAGE, ">$params{'editPage'}";
      print EDITEDPAGE $html . "\n";
      close EDITEDPAGE;
    }

    my $html = &getFile($params{'editPage'});

    ## grab the individual documents name
    my $doc = (split(/\//, $params{'editPage'}))[-1];

    print $q->b("<font color=#cc3300>View page:</font> <a href=http://www.$client_domain/$doc target=_new>http://www.$client_domain/$doc</a>"), $q->br x 2;
    #print $q->b("<a href=http://www.$client_domain><font color=#cc3300>Page:</font></a> $params{'editPage'}."), $q->br x 2;
    #print qq|<a href="http://www.$client_domain/$params{'editPage'}>www.$client_domain/$params{'editPage'}</a><p>|; 

    my $ind = 0;
    foreach(@editTypes) {
      while ($html =~ s/\<!-- upoint type="$_".*?\>.*?\<!-- \/upoint --\>/!~CUR~!/s) {
	$ind++;
	my $curMatch = $&;

	my $subStr;
	if (/textbox/) {
	  #charles edit
	  #$curMatch =~ s/\<BR\>/\n/gis;
	  $curMatch =~ /name="(.*?)" rows=([0-9]+).*?\>(.*?)\<!--/s;
	  $subStr .= "<b>$1</b>:<br>" . &indent . "<textarea name=\"textbox$ind\" rows=$2 cols=75>$3</textarea>";
	} elsif (/email/) {
	  $curMatch =~ /name="(.*?)"/;
	  $curName = $1; $curMatch =~ /()/;
	  $curMatch =~ /.*?mailto\:(.*?)[\'\"].*?\>(.*?)\</s;
	  $subStr .= "<b>$curName</b>:<br>Contact description:<br>" . &indent .
	    $q->textfield(-name => "emailDesc$ind",
			  -value => $2,
			  -size => 50) .
	      "<br>Email address:<br>" . &indent .
		$q->textfield(-name => "emailAddr$ind",
			      -value => $1,
			      -size => 50);
	} elsif (/link/) {
	  $curMatch =~ /name="(.*?)"/is;
	  $curName = $1; $curMatch =~ /()/;
	  $curMatch =~ /.*?href=[\'\"](.*?)[\'\"].*?\>(.*?)\</s;
	  $subStr .= "<b>$curName</b>:<br>Link description:<br>" . &indent .
	    $q->textfield(-name => "linkDesc$ind",
			  -value => $2,
			  -size => 50) .
	      "<br>url:<br>" . &indent .
		$q->textfield(-name => "linkAddr$ind",
			      -value => $1,
			      -size => 50);
	} elsif (/imageURL/) {
	  $curMatch =~ /name="(.*?)"/is;
	  my $curName = $1;
	  $curMatch =~ /src=[\'\"](.*?)[\'\"]/is;
	  $subStr .= "<b>$curName</b>:<br>Image url:<br>" . &indent .
	    $q->textfield(-name => "imageURL$ind",
			  -value => ($1 eq $curName) ? "" : $1,
			  -size => 50);
	  $curMatch =~ /align=[\'\"](.*?)[\'\"]/s;
	  $subStr .= "<br>Alignment:<br>" . &indent .
	    $q->popup_menu(-name => "imageURLalign$ind",
			   -values => ["", "left", "center", "right"],
			   -default => $1);
	}# elsif (/library/) {
#	  $curMatch =~ /align="(.*?)" ref="(.*?)"/;
#	  $subStr = "<img align=\"$1\" src=\"$2\">";
#	}
	print $subStr, $q->br;
      }
      print $q->hr;
    }
    &imageButton('submitchanges');
    print $q->hidden(-name => 'justSlaveEdited');
    print $q->hidden(-name => 'mode',
		     -value => 'edit');
    print $q->hidden(-name => 'editPage',
		     -value => $oldName);
    print $q->end_form;
    print $q->start_form(-method => 'post',
			 -action => 'webpublisher.cgi');
    &imageButton('chooseafile');
  }

  print $q->hidden(-name => 'mode',
		   -value => 'edit');
  &printLogout;

} elsif ($params{'mode'} eq 'master') { 

  if ($params{'newFile'} =~ /[a-zA-Z]$/) {
    if (!(-e $params{'newFile'})) {
      print "<b><font color=#cc3300>Sorry!</font></b> Couldn't find file $params{'newFile'}";
    &endLawrence;
      exit;
    } else {
      print "New file $params{'newFile'} added and chmoded to 0777.<BR>";
    }
    open NEWFILE, ">>upoint.txt";
    print NEWFILE $params{'newFile'} . "\n";
    close NEWFILE;
    chmod 0777, $params{'newFile'};
  }
  if (defined $params{'editedFileName'}) {
    open EDITEDFILE, ">$params{'editedFileName'}";
    print EDITEDFILE $params{'editedFile'} . "\n";
    close EDITEDFILE;
  }
  if (defined $params{'rmFile'} && $params{'rmFile'} ne 'none') {
    my %newFiles;

    $params{'rmFile'} = &pullName($params{'rmFile'});
    @newFiles{&getFile('upoint.txt', 'T')} = ();
    delete $newFiles{$params{'rmFile'}};
    open NEWFILES, ">upoint.txt";
    print NEWFILES join "\n", keys %newFiles;
    print NEWFILES "\n";
    close NEWFILES;
  }

  my %fileDisp = &fileDispHash;

  print $q->b("<p><font color=#cc3300>Master Mode:</font></p>Delete File</b> from editable file list<BR>");
  print $q->popup_menu(-name => 'rmFile',
		       -values => ['none', sort values %fileDisp]);
  &imageButton('deleteafile');
  print $q->hidden(-name => 'mode',
		   -value => 'master');
  print $q->end_form;
  print $q->start_form(-method => 'post',
		       -action => 'webpublisher.cgi');
  print $q->b("Add File</b> to editable file list"), $q->br;
  print $empty_q->textfield(-name => 'newFile',
			    -value => $rootpath,
			    -size => 50);
  &imageButton('addafile');
  print $q->hidden(-name => 'mode',
		   -value => 'master');
  print $q->end_form;
  print $q->start_form(-method => 'post',
		       -action => 'webpublisher.cgi');

  if (defined $params{'editFile'} && $params{'editFile'} ne 'none') {
    $params{'editFile'} = &pullName($params{'editFile'});
    my $html = &getFile($params{'editFile'});
    print $q->b("Editing: <font color=#cc3300>$params{'editFile'}</font>"), $q->br;
    print $q->textarea(-name => 'editedFile',
		       -rows => 25,
		       -cols => 75,
		       -value => $html), $q->br;
    print $q->hidden(-name => 'editedFileName',
		     -value => $params{'editFile'});
    &imageButton('submitchanges');
  } else {
    print $q->b("Edit File</b> in editable file list"), $q->br;
    print $q->popup_menu(-name => 'editFile',
			 -values => ['none', sort values %fileDisp]);
    &imageButton('editafile');
  }
  
  print $q->hidden(-name => 'mode',
		   -value => 'master');
  print $q->end_form;
  print $q->start_form(-method => 'post',
		       -target => '_blank',
		       -action => 'webpublisher.cgi');
  print $q->b("View</b> Editable File"), $q->br;
  print $q->popup_menu(-name => 'seeFile',
		       -values => [sort values %fileDisp]);
  &imageButton('viewafile');
  print $q->end_form;
  print $q->start_form(-method => 'post',
		       -action => 'webpublisher.cgi');
  print "<input type=hidden name=mode value=edit>";
  &imageButton('backtoslavemode');

  &printLogout;

} elsif (defined $params{'seeFile'}) {
  $params{'seeFile'} = &pullName($params{'seeFile'});
  $params{'seeFile'} =~ s/$rootpath/$rootURL/i;
  print "Location: $params{'seeFile'}\n\n";
  exit;
} elsif (!defined $params{'mode'}) {
  print "Enter password :
  <input type=password name=password>";
  &imageButton('login');
}

&endLawrence;

exit;
