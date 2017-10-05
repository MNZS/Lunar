# Perlfect Search - SGMLEntities.pl
# Mapping of Numbers to HTML entities and useful functions
# Hash taken from htdig's SGMLEntities.cc (shortened)

#$rcs = ' $Id: SGMLEntities.pl,v 1.7 2001/03/03 19:49:33 daniel Exp $ ' ;

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

# Load the users' list of (common) words that should not be indexed. Return
# a regular expression that can be used to remove exactly those words.
sub load_stopwords {
  my @stopwords;
  my $stopwords_regex;

  open (FILE, $STOPWORDS_FILE) or (warn "Cannot open $STOPWORDS_FILE: $!" and next);
  while (<FILE>) {
    chomp;
    $_ =~ s/\r//g; # get rid of carriage returns
    push @stopwords, $_;
  }
  close(FILE);
  $stopwords_regex = '\b(' . join('|', @stopwords) . ')\b';

  return $stopwords_regex;
}

my $special_chars;	# special characters we have to replace
# Build list of special characters that will be replaced in normalize(),
# put this list in global variable $special_chars.
sub build_char_string {
  foreach my $number (keys %entities) {
    $special_chars .= chr($number);
  }
}

# Represent all special characters as the character they are based on.
sub remove_accents {
  my $buffer = $_[0];
  # Special cases:
  $buffer =~ s/&thorn;/th/igs;
  $buffer =~ s/&eth;/d/igs;
  $buffer =~ s/&szlig;/ss/igs;
  # Now represent special characters as the characters they are based on:
  $buffer =~ s/&(..?)(grave|acute|circ|tilde|uml|ring|cedil|slash|lig);/$1/igs;
  return $buffer;
}

# Represent all special characters as HTML entities like &<entitiy>;
sub normalize_special_chars {
  my $buffer = $_[0];
  # There may be special characters that are not encoded, so encode them:
  $buffer =~ s/([$special_chars])/"&#".ord($1).";"/gse;
  # Special characters can be encoded using hex values:
  $buffer =~ s/&#x([\dA-F]{2});/"&#".hex("0x".$1).";"/igse;
  # Special characters may be encoded with numbers, undo that (use the if() to avoid warnings):
  $buffer =~ s/&#(\d\d\d);/if( $1 >= 192 && $1 <= 255 ) { "&$entities{$1};"; }/gse;
  return $buffer;
}

%entities = (
	192 => 'Agrave',	#  capital A, grave accent 
	193 => 'Aacute',	#  capital A, acute accent 
	194 => 'Acirc',		#  capital A, circumflex accent 
	195 => 'Atilde',	#  capital A, tilde 
	196 => 'Auml',		#  capital A, dieresis or umlaut mark 
	197 => 'Aring',		#  capital A, ring 
	198 => 'AElig',		#  capital AE diphthong (ligature) 
	199 => 'Ccedil',	#  capital C, cedilla 
	200 => 'Egrave',	#  capital E, grave accent 
	201 => 'Eacute',	#  capital E, acute accent 
	202 => 'Ecirc',		#  capital E, circumflex accent 
	203 => 'Euml',		#  capital E, dieresis or umlaut mark 
	205 => 'Igrave',	#  capital I, grave accent 
	204 => 'Iacute',	#  capital I, acute accent 
	206 => 'Icirc',		#  capital I, circumflex accent 
	207 => 'Iuml',		#  capital I, dieresis or umlaut mark 
	208 => 'ETH',		#  capital Eth, Icelandic (Dstrok) 
	209 => 'Ntilde',	#  capital N, tilde 
	210 => 'Ograve',	#  capital O, grave accent 
	211 => 'Oacute',	#  capital O, acute accent 
	212 => 'Ocirc',		#  capital O, circumflex accent 
	213 => 'Otilde',	#  capital O, tilde 
	214 => 'Ouml',		#  capital O, dieresis or umlaut mark 
	216 => 'Oslash',	#  capital O, slash 
	217 => 'Ugrave',	#  capital U, grave accent 
	218 => 'Uacute',	#  capital U, acute accent 
	219 => 'Ucirc',		#  capital U, circumflex accent 
	220 => 'Uuml',		#  capital U, dieresis or umlaut mark 
	221 => 'Yacute',	#  capital Y, acute accent 
	222 => 'THORN',		#  capital THORN, Icelandic 
	223 => 'szlig',		#  small sharp s, German (sz ligature) 
	224 => 'agrave',	#  small a, grave accent 
	225 => 'aacute',	#  small a, acute accent 
	226 => 'acirc',		#  small a, circumflex accent 
	227 => 'atilde',	#  small a, tilde
	228 => 'auml',		#  small a, dieresis or umlaut mark 
	229 => 'aring',		#  small a, ring
	230 => 'aelig',		#  small ae diphthong (ligature) 
	231 => 'ccedil',	#  small c, cedilla 
	232 => 'egrave',	#  small e, grave accent 
	233 => 'eacute',	#  small e, acute accent 
	234 => 'ecirc',		#  small e, circumflex accent 
	235 => 'euml',		#  small e, dieresis or umlaut mark 
	236 => 'igrave',	#  small i, grave accent 
	237 => 'iacute',	#  small i, acute accent 
	238 => 'icirc',		#  small i, circumflex accent 
	239 => 'iuml',		#  small i, dieresis or umlaut mark 
	240 => 'eth',		#  small eth, Icelandic 
	241 => 'ntilde',	#  small n, tilde 
	242 => 'ograve',	#  small o, grave accent 
	243 => 'oacute',	#  small o, acute accent 
	244 => 'ocirc',		#  small o, circumflex accent 
	245 => 'otilde',	#  small o, tilde 
	246 => 'ouml',		#  small o, dieresis or umlaut mark 
	248 => 'oslash',	#  small o, slash 
	249 => 'ugrave',	#  small u, grave accent 
	250 => 'uacute',	#  small u, acute accent 
	251 => 'ucirc',		#  small u, circumflex accent 
	252 => 'uuml',		#  small u, dieresis or umlaut mark 
	253 => 'yacute',	#  small y, acute accent 
	254 => 'thorn',		#  small thorn, Icelandic 
	255 => 'yuml',		#  small y, dieresis or umlaut mark
);

1;
