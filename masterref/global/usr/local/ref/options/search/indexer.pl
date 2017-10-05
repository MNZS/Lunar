#!/usr/bin/perl
#$rcs = ' $Id: indexer.pl,v 1.46 2001/03/03 21:50:02 daniel Exp $ ' ;	

# Perlfect Search
#
# Copyright (C) 1999-2000 Giorgos Zervas <giorgos@perlfect.com>
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA

use Fcntl;

# added program path to @INC because it fails to find ./conf.pl if
# started from other directory
{ 
  # block is for $1 not mantaining its value
  $0 =~ /(.*)(\\|\/)/;
  push @INC, $1 if $1;
}

my $db_package = "";
package AnyDBM_File;
@ISA = qw(DB_File) unless @ISA;
# You may try to comment in the next line if you don't have DB_File. Still
# this is not recommended.
#@ISA = qw(DB_File GDBM_File SDBM_File ODBM_File NDBM_File);
foreach my $isa (@ISA) {
  if( eval("require $isa") ) {
    $db_package = $isa;
    last;
  }
}
if( $db_package  ne 'DB_File' ) {
  die "*** The DB_File module was not found on your system.";
}

package main;
require 'conf.pl';
require 'indexer_filesystem.pl';
require 'SGMLEntities.pl';
if( $HTTP_START_URL ) {
  require 'indexer_web.pl';
}

$|=1;

# Calling via CGI is allowed with password:
if( $INDEXER_CGI_PASSWORD && $ENV{'REQUEST_METHOD'} ) {
  print "Content-Type: text/plain\n\n";
  print "Perlfect Search $VERSION indexer.pl\n\n";
  if( $ENV{'QUERY_STRING'} ) {		# call via method=GET
    print "*** Warning: You are calling this program in an insecure way!\n";
    print "*** Use method=\"POST\" to make the call more secure.\n\n";
  }
  use CGI;
  use CGI::Carp qw(fatalsToBrowser);
  my $query = new CGI;
  if( $query->param('password') ne $INDEXER_CGI_PASSWORD ) {
    print "Error: Access denied, invalid password.\n";
    exit;
  }
  print "Note: Do not call this script again while this instance is not finished.\n\n";
}

# Calling via CGI is NOT allowed, but someone tries to:
if( ! $INDEXER_CGI_PASSWORD && $ENV{'REQUEST_METHOD'} ) {
  print "Content-Type: text/plain\n\n";
  print "Error: Access denied. Cannot be called via CGI because \$INDEXER_CGI_PASSWORD is not set.\n";
  exit;
}

print "Using $db_package...\n";

my $DN  = 0;  #documents number
my $TN  = 0;  #terms number

my @stopwords;
my @no_index;

print "Checking for old temp files...\n";
delete_temp_files();

my %inv_index_db;
my %docs_db;
my %sizes_db;
my %desc_db;
my %title_db;
my %content_db;
my %terms_db;
my %df_db;
my %tf_db;

if( $LOW_MEMORY_INDEX ) {
  tie %inv_index_db, $db_package, $INV_INDEX_TMP_DB_FILE, O_CREAT|O_RDWR, 0755 or die "Cannot open $INV_INDEX_TMP_DB_FILE: $!";
  tie %docs_db,      $db_package, $DOCS_TMP_DB_FILE, O_CREAT|O_RDWR, 0755      or die "Cannot open $DOCS_TMP_DB_FILE: $!";
  tie %sizes_db,     $db_package, $SIZES_TMP_DB_FILE, O_CREAT|O_RDWR, 0755     or die "Cannot open $SIZES_TMP_DB_FILE: $!";
  tie %desc_db,      $db_package, $DESC_TMP_DB_FILE, O_CREAT|O_RDWR, 0755      or die "Cannot open $DESC_TMP_DB_FILE: $!"; 
  tie %titles_db,    $db_package, $TITLES_TMP_DB_FILE, O_CREAT|O_RDWR, 0755    or die "Cannot open $TITLES_TMP_DB_FILE: $!";
  tie %terms_db,     $db_package, $TERMS_TMP_DB_FILE, O_CREAT|O_RDWR, 0755     or die "Cannot open $TERMS_TMP_DB_FILE: $!"; 
  tie %df_db,        $db_package, $DF_DB_FILE, O_CREAT|O_RDWR, 0755            or die "Cannot open $DF_DB_FILE: $!";
  tie %tf_db,        $db_package, $TF_DB_FILE, O_CREAT|O_RDWR, 0755            or die "Cannot open $TF_DB_FILE: $!";
}
tie %content_db,   $db_package, $CONTENT_TMP_DB_FILE, O_CREAT|O_RDWR, 0755   or die "Cannot open $CONTENT_TMP_DB_FILE: $!";

print "Building string of special characters...\n";
build_char_string();
print "Loading \'no index\' regular expressions:\n";
load_excludes();
print "Loading stopwords...";
my $stopwords_regex = load_stopwords();
print "Done.\n";

print "Starting crawler...\n";
if( $HTTP_START_URL ) {
	init_http();
	crawl_http($HTTP_START_URL);
} else {
	init_filesystem();
	crawl_filesystem($DOCUMENT_ROOT);
}
print "Crawler finished($DN files, $TN terms)\n\n";

print "Calculating weight vectors: \n";
weights();

untie %content_db;
if( $LOW_MEMORY_INDEX ) {
  # Removing the files is a problem on Windows NT if they are still tie'd:
  untie %inv_index_db;
  untie %docs_db;
  untie %sizes_db;
  untie %desc_db;
  untie %titles_db;
  untie %terms_db;
  untie %df_db;
  untie %tf_db;
  print "Removing unused db files:\n";
  print "\t$TF_DB_FILE...";
  if (unlink $TF_DB_FILE) {
    print "ok\n";
  } else {
    warn "Cannot unlink $TF_DB_FILE: $!";
  }
  print "\t$DF_DB_FILE...";
  if (unlink $DF_DB_FILE) {
    print "ok\n";
  } else {
    warn "Cannot unlink $DF_DB_FILE: $!";
  }
} else {
  print "Copying hash values to database files...\n";
  save_db($INV_INDEX_TMP_DB_FILE, %inv_index_db);
  save_db($DOCS_TMP_DB_FILE, %docs_db);
  save_db($SIZES_TMP_DB_FILE, %sizes_db);
  save_db($DESC_TMP_DB_FILE, %desc_db);
  save_db($TITLES_TMP_DB_FILE, %titles_db);
  save_db($TERMS_TMP_DB_FILE, %terms_db);
}

print "Renaming newly created db files...\n";
rename_db();

print "Indexer finished.\n";
exit;

# Copy the keys and values of a hash to a persistent file on disk.
sub save_db {
  my $name = shift;
  print "\t$name\n";
  my %hash = @_;
  my %db_tmp;
  tie %db_tmp, "DB_File", $name, O_CREAT|O_RDWR, 0755 or die "Cannot open '$name': $!"; 
  %db_tmp = %hash;
  untie %db_tmp;
}

# Sometimes people stop indexer.pl with Ctrl-C and temp files are left over.
# We better delete them so they don't confuse us.
sub delete_temp_files {
  my @tmp_files = ($INV_INDEX_TMP_DB_FILE,$DOCS_TMP_DB_FILE,$SIZES_TMP_DB_FILE,
    $TERMS_TMP_DB_FILE,$DESC_TMP_DB_FILE,$TITLES_TMP_DB_FILE,$CONTENT_TMP_DB_FILE);
  if( $LOW_MEMORY_INDEX ) {
    push(@tmp_files, $DF_DB_FILE,$TF_DB_FILE);
  }
  foreach my $oldfile (@tmp_files) {
    next unless (-e $oldfile);
    if (unlink $oldfile) {
      print "\tRemoving old temp file '$oldfile'\n";
    } else {
      warn "Cannot unlink $oldfile: $!";
    }
  }
}

# Save important parts of a file to the database.
sub index_file {
  my ($url, $doc_id, $buffer) = @_;
  my ($term, $term_id);
  my %tf;

  print "\t $doc_id: $url\n";
  $sizes_db{$doc_id} = length(${$buffer});		# remember document size

  # Many auto-generated HTML files contain (correct) syntax that makes our
  # regexp very slow. So better clean up now:
  ${$buffer} =~ s/\s+>/>/gs;
  ${$buffer} =~ s/<\s+/</gs;

  record_desc($doc_id, $buffer, $url);
  if ($INDEX_URLS) {
    # to search for parts of URLs, e.g. filenames:
    # (cutting out $DOCUMENT_ROOT for security reasons!)
    ${$buffer} = cut_document_root($url)." ".${$buffer};
  }
  # to rank words in the title tag and in headlines differently:
  get_tag_contents("title", $buffer, $TITLE_WEIGHT);
  get_headline_contents($buffer);
  # to search for text in the follwing meta tags:
  ${$buffer} .= " ".get_meta_content("description", $buffer, $META_WEIGHT);
  ${$buffer} .= " ".get_meta_content("keywords", $buffer, $META_WEIGHT);
  ${$buffer} .= " ".get_meta_content("author", $buffer, $META_WEIGHT);
  # to search for images' alt texts:
  get_alt_texts($buffer);
  normalize($buffer);
  
  foreach (split " ", ${$buffer}) {
    $_ = substr $_, 0, $STEMCHARS if $STEMCHARS;
    if (length $_ >= $MINLENGTH) {
      $term_id = record_term($_);
      ++$tf{$term_id};
    }
  }
  
  foreach (keys %tf) {
    $df_db{$_}++;
    $tf_db{$_} = '' unless defined $tf_db{$_};
    $tf_db{$_} .= pack("ww", $doc_id, $tf{$_}); 
  }
}

# Calculate the weight (score) for each term in each file and 
# save it to the database.
sub weights {
  my ($weight, $term_id, $doc_id);
  my $step = $TN / 50;
  my $count = 0;
  
  $step = 1 if $step < 1;

  print "0%  10%  20%  30%  40%  50%  60%  70%  80%  90%  100%\n";
  print "|----|----|----|----|----|----|----|----|----|----|\n";
  print ">";

  foreach $term_id (keys %tf_db) {
    my $weights = $inv_index_db{$term_id} || '';
    my $df = $df_db{$term_id};
    my %tdf = unpack("w*",$tf_db{$term_id}); 
    $count++;
    print "\b >" unless $count % $step;
    foreach $doc_id (keys %tdf) {
      #print "weight = $tdf{$doc_id} * log ($DN / $df)\n";
      $weight = $tdf{$doc_id} * log ($DN / $df);
      $weight = int($weight*100);
      $weight = 65535 if ( $weight > 65535 );	# we're limited to 16 bit
      $weights .= pack("SS", $doc_id, $weight);
    }
    undef %tdf;
    $inv_index_db{$term_id} = $weights;
  }
  print "\n";
}

# Replace umlauts etc by ASCII characters, remove stopwords, remove HTML, 
# remove remaining special charcaters. In the end, we only have [a-zA-Z0-9_].
# Then it is converted to lowercase and returned.
sub normalize {
  my $buffer = $_[0];

  ${$buffer} =~ s/$IGNORE_TEXT_START.*?$IGNORE_TEXT_END//gis;  # strip user defined parts
  ${$buffer} =~ s/<!--.*?-->//gis;  # strip html comments
  ${$buffer} =~ s/-(\s*\n\s*)?//g;  # join parts of hyphenated words

  if( $SPECIAL_CHARACTERS ) {
    ${$buffer} = normalize_special_chars(${$buffer});
    ${$buffer} = remove_accents(${$buffer});
  }

  # Replace HTML tags (and maybe numbers) by spaces:
  if ($INDEX_NUMBERS) {
    ${$buffer} =~ s/(<[^>]*>)/ /gs;
  } else {
    ${$buffer} =~ s/(\b\d+\b)|(<[^>]*>)/ /gs;
  }

  ${$buffer} =~ s/$stopwords_regex//gio;
  ${$buffer} =~ tr/a-zA-Z0-9_/ /cs;
  ${$buffer} = lc ${$buffer};
}

# Return the body without HTML and unnecessary whitespace.
sub get_cleaned_body {
  my $buffer = $_[0];
  my ($cleaned) = (${$buffer} =~ m/<BODY.*?>(.*)<\/BODY>/is);
  $cleaned = ${$buffer} if( ! $cleaned );	# PDF files don't have a <body>
  $cleaned =~ s/$IGNORE_TEXT_START.*?$IGNORE_TEXT_END//gis;  # strip user defined parts
  $cleaned =~ s/<!--.*?-->//gis;        # strip html comments
  $cleaned =~ s/<.+?>/ /gis;            # strip html
  $cleaned =~ s/\s+/ /gis;              # strip too much whitespace
  $cleaned =~ tr/\n\r/ /s;
  $cleaned = normalize_special_chars($cleaned);
  return $cleaned;
}

# Save the (document ID, filename) relation to the database.
sub record_file {
  my $file = $_[0];
  $file = cut_document_root($file);
  ++$DN;
  # for development only:
  #if( $DN % 100 == 0 ) {
  #  memory_usage();
  #}
  if( $DN >= 65535 ) {
    die "Error: Indexing more than 65534 documents is not supported";
  }
  $docs_db{$DN} = $file;
  return $DN;
}

# Save a short description for every document to the database. If no 
# meta description tag is available, take the first words from the body.
# Also save the <title> to the database.
sub record_desc {
  my ($doc_id, $buffer, $file) = @_;
  my ($desc, $title, $cleanbody);
  my @desc_ary;

  # Save Description or beginning of body:
  $desc = get_meta_content("description", $buffer, 1);
  if( ! $desc || $CONTEXT_SIZE ) {
    $cleanbody = get_cleaned_body($buffer);
  }
  unless ($desc) {
    @desc_ary = split " ", $cleanbody;
    my $to = $DESC_WORDS;
    $to = scalar(@desc_ary)-1 if( $DESC_WORDS > scalar(@desc_ary) );
    $desc = join " ", @desc_ary[0..$to];
    $desc .= "..." if( $desc !~ m/\.\s*$/ );
  }
  $desc_db{$doc_id} = $desc;

  # Save title:
  ${$buffer} =~ m/<TITLE>(.*?)<\/TITLE>/is;
  $title = $1;
  if( (! $title) || $title =~ m/^\s+$/ ) {
    $file =~ s/.*\///;	# remove the path
    $title = $file;
  }
  $titles_db{$doc_id} = $title;

  # Optionally save the document (to show results with context):
  if( $CONTEXT_SIZE ) {
    my $cont = $cleanbody;
    $cont = substr($cont, 0, $CONTEXT_SIZE) if( $CONTEXT_SIZE != -1 );
    $content_db{$doc_id} = $cont;
  }
}

# Get the content part for a certain meta tag. Weight with
# a certain factor by just repeating the result that often.
sub get_meta_content {
  my $name = $_[0];
  my $buffer = $_[1];
  my $weight = $_[2];
  my ($content) = (${$buffer} =~ m/<META\s+name\s*=\s*[\"\']?$name[\"\']?\s+content=[\"\'](.*?)[\"\']\s*>/is);
  return "" if( ! $content || $content =~ m/^\s+$/ );
  $content = (($content." ") x $weight);
  return $content;  
}

# Add all values for alt="...", joined with spaces to $buffer.
sub get_alt_texts {
  my $buffer = $_[0];
  my $alt_texts = "";
  while( ${$buffer} =~ m/alt\s*=\s*[\"\'](.*?)[\"\']/gis ) {
  	$alt_texts .= " ".$1;
  }
  ${$buffer} .= $alt_texts;
}

# Add the contents of a certain tag, weighted by just repeating these contents
# to $buffer.
sub get_tag_contents {
  my $tag = $_[0];
  my $buffer = $_[1];
  my $weight = $_[2];
  my $tag_content = "";
  while( ${$buffer} =~ m/<$tag.*?>(.*?)<\/$tag>/igs ) {
    $tag_content .= (" ".$1) x $weight;
  }
  ${$buffer} .= $tag_content;
}

# Add the contents of all headline levels, weighted by just repeating these contents
# to $buffer.
sub get_headline_contents {
  my $buffer = $_[0];
  my $level;
  my $headlines = "";
  for( $level = 1; $level <= 6; $level++ ) {
    while( ${$buffer} =~ m/<h$level.*?>(.*?)<\/h$level>/igs ) {
      $headlines .= (" ".$1) x $H_WEIGHT{$level};
    }
  }
  ${$buffer} .= $headlines;
}

# Checks if a file is PDF depending on the filename. If so, write it to a
# temporary file and feed it to $PDFTOTEXT, return the output. If it's not
# PDF, return the buffer unmodified.
sub parse_pdf {
  my $buffer = $_[0];
  my $url = $_[1];
  if ($url =~ m/\.pdf$/i && $PDFTOTEXT) {
    my $tmpfile = "$TMP_DIR/temp.pdf";
    # Saving to a temporary file is necessary for http requested PDFs. To
    # keeps things simpler, we also do it for local files from disk.
    open(TMPFILE, ">$tmpfile") or warn "Cannot write '$tmpfile': $!";
    binmode(TMPFILE);
    print TMPFILE ${$buffer};
    close(TMPFILE);
    # filename security check is done in to_be_ignored():
    ${$buffer} = `$PDFTOTEXT "$tmpfile" -` or (warn "Cannot execute '$PDFTOTEXT $tmpfile -': $!" and return undef);
    unlink $tmpfile or warn "Cannot remove '$tmpfile: $!'"
  }
}

# Save a term's ID to the database, if it does not yet exist. Return the ID.
sub record_term {
  my $term = $_[0];
  print STDERR "Warning: record_term($term): No term was supplied\n" unless $term;
  if ($terms_db{$term}) {
    return $terms_db{$term};
  } else {
    ++$TN;
    $terms_db{$term} = $TN;
    return $TN;
  }
}

# Is the file listed in @no_index or is it a PDF file with illegal characters
# in the filename?
# Supported ways to list a file in conf/no_index:
# /home/www/test/index.html (absolute path)
# /test/index.html (path relative to webroot, but with slash)
# test/index.html (path relative to webroot, no slash)
# http://localhost/test/index.html (absolute URL)
sub to_be_ignored {
  my $file = shift;
  # Check @no_index:
  my $file_relative;
  $file_relative = cut_document_root($file);
  foreach my $regexp (@no_index) {
    if( $file_relative =~ m/^\/?$regexp$/ || $file =~ m/^$regexp$/ ) {
      return "listed in no_index.txt";
    }
  }
  # For PDF files check filename for security reasons (it later gets handed to a shell!):
  if( $file =~ m/\.pdf$/i && $PDFTOTEXT ) {
    if( $file !~ m/^[\/\\a-zA-Z0-9_.:+-]*$/ || $file =~ m/\.\./ ) {
      return "Ignoring '$file': illegal characters in filename";
    }
  }
  return undef;
}

# Remove $DOCUMENT_ROOT or $BASE_URL from an absolute filename/url and return the 
# relative filename/url, but starting with a slash.
sub cut_document_root {
  my $file = shift;
  my $root = "";
  my $tmp_file = "";
  if( $file =~ m/^http:/i ) {
    $root = $BASE_URL;
    $tmp_file = $file;
  } else {
    $DOCUMENT_ROOT =~ s/\\/\//g;
    # On Windows, both / and \ are valid to seperate paths. We still have to 
    # filter out $DOCUMENT_ROOT, so make \ to /:
    $file =~ s/\\/\//g;
    $tmp_file = $file;
    $root = $DOCUMENT_ROOT;
  }
  ($file) = ($file =~ m/^$root(.*)$/);
  if( ! $file ) {
    # This should never happen!
    print STDERR "Warning: cannot remove '$root' from '$tmp_file'\n";
  }
  unless ($file =~ /^\//) {
    $file = "/".$file;
  }
  return $file;
}

# Load the user's list of files that should not be indexed.
sub load_excludes {
  if (-e $NO_INDEX_FILE) {
    open (FILE, $NO_INDEX_FILE) or (warn "Cannot open $NO_INDEX_FILE: $!" and next);
    while (<FILE>) {
      chomp;
      $_ =~ s/\r//g;        # get rid of carriage returns      
      $_ =~ s/(\#.*)//g;    # ingore comments
      $_ =~ s/[\/\s]*$//;   # remove any trailing spaces and slashes
      next if( ! $_ );
      print "\t- $_\n";
      
      $_ = quotemeta;       # escape all non-alphanumeric characters
      $_ =~ s/\\\*/\.\*/g;  # except for the * which is replaced by .*
      push @no_index, $_;
    }
    close (FILE);
  } else {
    print STDERR "Warning: $NO_INDEX_FILE missing.";
  }
}

# Move the temporary files to their non-temporary places. This is
# called when the new index is complete. This way the old index 
# files can still be used while the new ones are being created.
sub rename_db {
  my @files = (
	       [$TERMS_TMP_DB_FILE, $TERMS_DB_FILE],
	       [$DOCS_TMP_DB_FILE, $DOCS_DB_FILE],
	       [$SIZES_TMP_DB_FILE, $SIZES_DB_FILE],
	       [$TITLES_TMP_DB_FILE, $TITLES_DB_FILE],
	       [$CONTENT_TMP_DB_FILE, $CONTENT_DB_FILE],
	       [$DESC_TMP_DB_FILE, $DESC_DB_FILE],
	       [$INV_INDEX_TMP_DB_FILE, $INV_INDEX_DB_FILE],
	      );

  foreach (@files) {
    print "\t ", $_->[0], " to ", $_->[1], "\n";
    rename $_->[0], $_->[1] or (warn "Cannot rename $_->[0]: $!" and next);
  }
}

# For development only: check memory usage during indexing.
sub memory_usage {
	my $pid = $$;
	my $str = `top -b -n 0 -p $pid`;
	my ($line) = ($str =~ m/^(.*?indexer\.pl.*?)$/igm);
	$line =~ s/^\s+//;
	my @line = split(/\s+/, $line);
	print "mem: $line[4]\n";
}

# Shut up misguided -w warnings about "used only once". Has no functional meaning.
sub warnings_sillyness {
  my $zz;
  $zz = $SIZES_DB_FILE;
  $zz = $TITLE_WEIGHT;
  $zz = $SPECIAL_CHARACTERS;
  $zz = $H_WEIGHT;
  $zz = $INDEX_URLS;
  $zz = $DESC_WORDS;
  $zz = $INV_INDEX_DB_FILE;
  $zz = $MINLENGTH;
  $zz = $BASE_URL;
  $zz = $DESC_DB_FILE;
  $zz = $TITLES_DB_FILE;
  $zz = $TERMS_DB_FILE;
  $zz = $DOCS_DB_FILE;
  $zz = $TMP_DIR;
  $zz = $CONTENT_DB_FILE;
  $zz = $INDEX_NUMBERS;
}
