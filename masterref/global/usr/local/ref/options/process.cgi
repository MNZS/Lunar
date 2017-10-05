#!/usr/bin/perl -w
#

# $Id: process.cgi,v 1.26 2002/05/28 16:02:12 root Exp $

# This entire script is based on the premise that clients wanting to
# take advantage of its capabilities have a directory at:
#
#  /etc/commerce/<client>
#
# Without this structure, the script will fail without heavily editing.
#
 
use strict;
use POSIX qw(strftime);
use Mail::Sendmail;

delete @ENV{qw(IFS CDPATH ENV BASH_ENV)};
$ENV{'PATH'} = "/usr/bin:/usr/local/bin";
use CGI;
$CGI::DISABLE_UPLOADS = 1;
$CGI::POST_MAX = 1024;

################## EDIT THIS ########################################
#####################################################################

# domain of client
my $domain = "DOMAIN"; # www.domain.com


####            DO NOT EDIT BELOW THIS MARK                      ####

#####################################################################
#####################################################################
#####################################################################
#####################################################################


## variables
my %CONFIG;
my $filename;
my %FORM;
my $filenamehead;
my @missed_fields;

## grab form input
my $query = CGI->new(); 

## grab form field and stick values in hash
my @formfields = $query->param;

for my $field(@formfields) {
  if ($field eq 'recipient' ||
    $field eq 'replyaddr' ||
    $field eq 'required' ||
    $field eq 'replyname' ||
    $field eq 'title' ||
    $field eq 'redirect' ||
    $field eq 'subject' ||
    $field eq 'postdir' ||
    $field eq 'body_message' ||
    $field eq 'return_link_title' ||
    $field eq 'return_link_url' ) {

    $CONFIG{$field} = $query->param($field);

  } else {
    if ($field eq "17cardnumber") {
      my @i = $query->param($field);
      for my $i(@i) {
        $FORM{$field} = "$FORM{$field} - $i";
      }
    
    } else {
      $FORM{$field} = $query->param($field);
    
    }
  }
}

## for required fields, add them to an array
#my @required = split(/,/, $CONFIG{required});

#for my $i(@required) {
# if (!$FORM{$i}) {
#    push @missed_fields, $i;
#  }
#}

#&advise if ($#missed_fields > -1);

# directory where files will be written
my $crypt = "crypt"; # crypt directory

# customer id
my $cust = $domain;
$cust =~ s/^www\.//;

# complete url that will be send to client
my $url = "$domain\/$crypt";

# 
my $mailprog = '/usr/lib/sendmail';

# set the date string 
my $date = strftime("%a %b %e, %Y at %H:%M:%S", localtime);

# get the result location
$filenamehead=(1000000000-time()) . "-" . $$ . ".txt";

# set the location for the crypt protected file

$filename="\/etc\/commerce\/$cust\/$crypt\/" . $filenamehead; 


# Redirect User to after page
&redirect();

#
&make_file();

# Send E-Mail
&send_mail();

# Subroutines

sub send_mail {

  ## declare mail hash
  my %mail;

  ## place variables into hash
  ## seperated into scalars to allow for 'if' judgements
  $mail{To} = "$CONFIG{recipient}";
  $mail{From} = "$CONFIG{replyname} <$CONFIG{replyaddr}>";
  $mail{Subject} = "$CONFIG{subject}";
  $mail{Message} = "Please process https://$url/$filenamehead\n\nThank you";

  ## send the mail
  &sendmail(%mail)
    or die "Problem with Mail::Sendmail! : $!\n";

}

sub make_file {
     open(FILE,">$filename");
     print FILE "To:      $CONFIG{'recipient'}\n";
     print FILE "Subject: $CONFIG{'subject'}\n";
     print FILE "Date:    $date\n";
     print FILE "Below is the result of your feedback form.\n";
     print FILE "---------------------------------------------------------------------------\n\n";

     for my $key (sort keys %FORM) {
	   # Print the name and value pairs in FORM array to html.
	      print FILE "$key: $FORM{$key}\n";
          }

     print FILE "---------------------------------------------------------------------------\n";

     close (FILE);
}
     
sub redirect {
  if ($CONFIG{'redirect'}) {
    print "Location: $CONFIG{'redirect'}\n\n";
  }
}

sub advise {
print <<WARN;
Content-type: text/html\n\n
<html>
<head>
  <title>Missed fields!</title>
  <body bgcolor=#FFFFFF>
The following form fields need to be completed:<p>
WARN

for my $i(@missed_fields) {
  print qq|<li> $i<br>\n|;
}

print <<WARN;
<p>
Please use your browser's back button<br>
to return to the previous page and fill<br>
out the missing fields.<br>
</body>
</html>
WARN

exit;
}
