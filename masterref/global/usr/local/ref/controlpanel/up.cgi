#!/usr/bin/perl -w

use strict;
use CGI qw/:standard/;

print header,
  start_html('file upload'),
  h1('file upload');

print_form() ;
print end_html;

sub print_form {

  print start_multipart_form(),

    filefield(-name=>'upload',-size=>60),br,

    submit(-label=>'Upload file'),

    end_form;
}
