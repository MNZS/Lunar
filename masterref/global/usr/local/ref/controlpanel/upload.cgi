#!/usr/bin/perl -w

use strict;
use CGI qw/:standard/;

print header,
  start_html('file upload'),
  h1('file upload');

print_form() 
  #unless param;
#print_results() 
  #if param
print end_html

sub print_form {

  print start_multipart_form(),

    filefield(-name=>'upload',-size=>60),br,

    submit(-label=>'Upload file'),

    end_form;
}

sub print_results {

  my $length;

  my $file = param('upload');

  if (!$file) { 

    print "No File Uploaded!";

    return;

  }


  print h2('File Name'),$file;

  print h2('File MIME type'),

  uploadInfo($file)->{'Content-Type'};

  while(<$file>) {

    $length += length($_);

  }

  print h2('file Length'),$length;

}


