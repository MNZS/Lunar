# Perlfect Search - file system indexing
#$rcs = ' $Id: indexer_filesystem.pl,v 1.4 2000/12/26 22:12:36 daniel Exp $ ' ;

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

# Currently empty.
sub init_filesystem {
}

# Recursively traverse the filesystem, but ignore the files on @no_index.
sub crawl_filesystem {
  my $dir = $_[0];
  my $doc_id;
  my $file;
  
  print $dir,"\n";

  chdir $dir or (warn "Cannot chdir $dir: $!" and next);
  opendir(DIR, $dir) or (warn "Cannot open $dir: $!" and next);
  my @contents = readdir DIR;
  closedir(DIR);

  my @dirs  = grep {-d and not /^\.{1,2}$/} @contents; 
  my @files = grep {-f and /^.+\.(.+)$/ and grep {/^\Q$1\E$/} @EXT} @contents;
  
  FILE: foreach my $f (@files) {
    $file = $dir."/".$f;
    $file =~ s/\/\//\//og;

    next FILE if( to_be_ignored($file) );
    $doc_id = record_file($file);

    # loading the file:
    my $buffer = "";
    undef $/;
    open(FILE, $file) or (warn "Cannot open '$file': $!" and $DN-- and next);
    binmode(FILE);		# for reading PDF files under Windows NT
    $buffer = <FILE>;
    close(FILE); 
    $/ = "\n";  
    parse_pdf(\$buffer, $file);
    if( ! $buffer ) {
      $DN--;
      next;
    }
    index_file($file, $doc_id, \$buffer);
  }

  DIR: foreach my $d (@dirs) {
    $file = $dir."/".$d;
    $file =~ s/\/\//\//og;
    
    foreach my $regexp (@no_index) {
      next DIR if $file =~ /^$regexp$/;
    }
    crawl_filesystem($file);
  }
}

1;
