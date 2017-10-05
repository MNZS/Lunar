#!/usr/bin/perl -w

use strict;
use Fcntl ':flock';
use CGI;
#use CGI::Carp qw(fatalsToBrowser carpout);
$CGI::DISABLE_UPLOADS = 1;
$CGI::POST_MAX = 1024;

## project notes
my $rcs = (qw$Revision: 1.27 $)[-1];

## file definitions

my $database = "/www/cesworldwide.com/database/webform.csv";

######################################################################
######################################################################

## definitions
my @missing_fields = ();

## initialize a cgi.pm object
my $query = new CGI;
$query = CGI->new();

## grab the form values
my %formdata = ();
my @formfields = $query->param;
for my $i(@formfields) {
  my $j = lc $i;
  $formdata{$j} = $query->param("$i");
  $formdata{$j} =~ s/\,/ /g;
  $formdata{$j} =~ s/\cM//g;
  $formdata{$j} =~ s/\n/ /g;
}

## grab the required fields
if ($formdata{required}) {

  ## the form field required should be ^ seperated
  my @required = split(/\^/, $formdata{required});

  ## loop through the required fields to ensure they have input
  for my $i(@required) {
   
   ## stick the field name into missing_fields unless it has a value 
   push @missing_fields, $i
      unless ($formdata{$i});

  ## end for loop
  }

## end if
}    


## if missing_fields has at least one value run the error message
if (@missing_fields) {
  errorRequire(@missing_fields);

  ## break the loop
  exit;

   
} else { 
  ## open/lock our database file
  open(FH, ">>$database")
    or die "Cant open database! : $!\n";

  ## lock the file for writing
  flock(FH,2);

  ## place our pointer at the file end
  seek(FH,0,2);

  ## add our data to the db file
  print FH "$formdata{event},$formdata{title},$formdata{firstname},$formdata{lastname},$formdata{suffix},$formdata{address1},$formdata{address2},$formdata{city},$formdata{state},$formdata{zip},$formdata{ownrent},$formdata{email},$formdata{agegroup},$formdata{music},$formdata{drink},$formdata{entertainment1},$formdata{entertainment2},$formdata{entertainment3},$formdata{notes}\n";

  ## unlock the file
  flock(FH,8);

  ## close the file
  close(FH); 

  ## print the success page
  &successPage;

## end if
}

## subroutines

sub genHeader { 
## generate html headers
print <<HTML;
Content-type: text/html\n\n

<html>
  <head>
   <title></title>
  </head>
  <body>
HTML

## end of genHeader
}

sub genFooter { 

print <<HTML;
  </body>
</html>
HTML

## end of genFooter
}

sub errorRequire { 
my @fields = @_;

&genHeader;

print qq|<b>The following required form fields have not been completed.<br>Please use your browser's BACK button to make the necessary changes.</b><p>|;

for my $i(@fields) {

  print "<li>$i</li>";

}


&genFooter;
exit;
}

sub successPage { 

print "Location: http://www.cesworldwide.com/thanks.htm\n\n";

## end of successPage
}
