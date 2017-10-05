#!/usr/bin/perl --
# -*-mode: Perl; tab-width: 4 -*-

my $relVersion = "1.0.8";

############################################################################
# Soupermail
#
# Internal build version:
# $Id: soupermail.pl,v 1.136 2001/02/07 22:04:55 aithalv Exp $
#
# Soupermail. A whacky and powerful WWW to Email form handler.
# Copyright (C) 1998, 1999, 2000, 2001 
#			   Vittal Aithal <vittal.aithal@bigfoot.com>
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See 
# the GNU General Public License for more details. You should have received 
# a copy of the GNU General Public License along with this program; if not,
# write to the Free Software Foundation, Inc., 675 Mass Ave, Cambridge, 
# MA 02139, USA.
#
############################################################################

############################################################################
# Set up the modules soupermail uses - these should all be perl5 standard
############################################################################
use lib qw(.);
use CGI;
use FileHandle;
use File::Copy;
use Fcntl qw(:DEFAULT :flock);
use Time::Local;
use POSIX qw(floor);
use MIME::Lite;
use strict;
use 5.004;

# Not all systems will have DBI, so eval to trap.
eval('use DBI;');
my $hasDbi = ($@ ? 0 : 1);

BEGIN {
	if ($^O =~ /MSWin/i) {
		require Win32::File;
		import Win32::File;
	}
}


############################################################################
my ($soupermailAdmin, $serverRoot, $mailprog, $mailhost, $pgpencrypt,
	$tempDir, $debug, $lout, $loutOpts, $pgpSet, $privateRoot, $forkable,
	$fhBug, $uploadTimeout, $ps2pdf, $fileLocking, $smtpPoolSize, $paranoid) = "";
############################################################################

############################################################################
# ---CHANGE ME FOR YOUR SITE---
# This is who to mail when soupermail goes wrong
# PLEASE PLEASE PLEASE PLEASE PLEASE PLEASE PLEASE PLEASE
# PLEASE PLEASE PLEASE PLEASE PLEASE PLEASE PLEASE PLEASE
# PLEASE PLEASE PLEASE PLEASE PLEASE PLEASE PLEASE PLEASE
# CHANGE THIS!!!
# I REALLY DON'T WANT TO GET ADMIN EMAILS ABOUT YOUR SITE!!!!
############################################################################
#$soupermailAdmin = 'vittal.aithal@bigfoot.com';
$soupermailAdmin = 'hosting@lunarmedia.net';

############################################################################
# ---CHANGE ME FOR YOUR SITE---
# This is where the webserver's document tree starts
# Do NOT include a trailing '/' character
#
# Some examples:
#	$serverRoot = 'c:/inetpub/wwwroot';		# Default NT/IIS setup
#	$serverRoot = $ENV{'DOCUMENT_ROOT'};	# May work on some webservers
#	$serverRoot = '/home/www/html';			# A typical UNIX setting
############################################################################
#$serverRoot = $ENV{'DOCUMENT_ROOT'};
$serverRoot = '/www/metaldecor.com/public_html';

############################################################################
# ---CHANGE ME FOR YOUR SITE---
# If you want to hide your config files from people browsing your site,
# provide a path OUTSIDE your server root here.
#
# Some examples:
#   $privateRoot = "c:/inetpub/private";
############################################################################
#$privateRoot = "/home/httpd/soupermail.sourceforge.net/private";


############################################################################
# Program locations. These will vary from site to site, so check that
# they're there and setup as appropriate
############################################################################

############################################################################
# ---CHANGE ME FOR YOUR SITE---
# To send outgoing mail, soupermail needs an SMTP mailserver to talk to.
# If you don't know the address of a suitable mailserver, ask your ISP
# or a system administrator. If you don't have a mailserver handy, you
# can use sendmail.
# If you indend to use the maillist features, I suggest you use a mailhost
# since it is probably faster.
#
# Some examples: 
#	$mailhost = 'localhost';				# Local SMTP server for NT
#	$mailprog = '';							# No mail program for NT
#
#	$mailhost = '';							# No SMTP host for UNIX
#	$mailprog = '/usr/lib/sendmail';		# Local sendmail for UNIX
############################################################################
#$mailhost = 'localhost';
$mailhost = '';

$mailprog = '/usr/lib/sendmail';


############################################################################
# ---CHANGE ME FOR YOUR SITE---
# The program to do pgp encryption. This was tested with PGP 5.0i 
# and GNU Privacy Guard 1.0.4 on my home Linux box, your milage 
# may vary with others.
# Set up the versions of GPG and/or pgp you have on your server
# here.
############################################################################
#$pgpSet = {
#	'gpg'	=> '/usr/local/bin/gpg',
#	'pgp2'	=> '/usr/local/bin/pgp2.6.3',
#	'pgp5'	=> '/usr/local/bin/pgpe',
#};

############################################################################
# ---CHANGE ME FOR YOUR SITE---
# These are the programs needed to generate PDFs
# $ps2pdf is the location of the ps2pdf command
# $lout is the location of the lout executable
# Safe to comment out if they're not used
#
# Some examples:
#	Ghostscript and lout settings for NT
#	$ps2pdf = 'c:/gstools/gs5.50/ps2pdf.bat';
#	$lout = 'c:/lout/3.17/lout.exe';
############################################################################
# Ghostscript and lout settings for UNIX
#$ps2pdf = '/usr/bin/ps2pdf';
#$lout = '/usr/local/bin/lout';

############################################################################
# ---CHANGE ME FOR YOUR SITE---
# Where to write out temporary files. If you're using PGP, or making
# PDFs, several files will be generated in a sudirectory off here. 
# Include a trailing '/' character.
#
# Some examples:
#	$tempDir = 'c:/temp/';	# Default temp area on NT
############################################################################
$tempDir = '/var/tmp/';

############################################################################
# Uncomment this to see what soupermail's doing.
# On a production server make sure its commented out.
############################################################################
$debug = "";
$debug = "${tempDir}soupermaillog";

############################################################################
# If your machine doesn't have fork() support, try setting this to 0
############################################################################
$forkable = 1;

############################################################################
# If you have trouble uploading files, try setting this to 1
# FreeBSD users may well need to do this
############################################################################
$fhBug = 1;

############################################################################
# If you are uploading large files, and soupermail's timing out, then
# increase this value. The units are seconds
############################################################################
$uploadTimeout = 100;

############################################################################
# This stuff is for PDF generation
############################################################################
$loutOpts = " -S";

############################################################################
# $maxbytes is the maximum number of bytes allowed to be uploaded.
# Its not very cleverly handled at the moment, but what can you do.
############################################################################
my ($maxbytes) = 102400;

############################################################################
# $maxdownload is the maximum number of bytes allowed to be downloaded.
############################################################################
my ($maxdownload) = 10240000;

############################################################################
# To prevent problems when lots of people are submiting fileto forms at
# the same time, file locking can be used. However - NT may screw up.
############################################################################
$fileLocking = 1;

############################################################################
# If you are sending out a large mailing list to several hundred addresses
# and you find that mailing stops after a while, you may have to increase
# this value. Check your SMTP server's maximum messages per connection to
# get a feel for the value.
############################################################################
$smtpPoolSize = 20;

############################################################################
# Paranoid should be used where people other than yourself have access to
# your server. i.e. Other people can put content on some part of your 
# server. At worst case the person would write their own config files,
# and read data from your server. Setting $paranoid to 1 prevents
# Soupermail from reading files from a directory, unless that directory
# contains a file called soupermail.allow
############################################################################
$paranoid = 0;

############################################################################
# Right, that in theory is the end of anything you have to configure in
# soupermail.pl - the rest's generic... well, maybe :)
#
# HOWEVER - remember you'll have to write config files for your forms -
# so now would be a good time to ==> READ THE MANUAL!! <==
# Just to repeat... READ THE MANUAL, READ THE MANUAL, READ THE MANUAL
# If things are going wrong, also READ THE FAQ AND THE HELP FORUM!!!!
#
# http://soupermail.sourceforge.net/manual.html
# http://soupermail.sourceforge.net/faq.html
# http://sourceforge.net/forum/forum.php?forum_id=342
#
# Very important that stuff, Soupermail's complex, and takes time to learn,
# please try to read about it BEFORE using it.
############################################################################



############################################################################
# Set up some global constants
############################################################################

############################################################################
# Useful month shortcuts
############################################################################
my (%MONTHS) = 
	('Jan','01','Feb','02','Mar','03','Apr','04','May','05','Jun','06',
	 'Jul','07','Aug','08','Sep','09','Oct','10','Nov','11','Dec','12');


############################################################################
# We may be generating cookies, and they'll live in @cookieList
# $cookieStr determines how many cookies we're allowing (9 by default)
############################################################################
my (@cookieList) = ();
my ($cookieStr) = 'cookie([123456789])';


############################################################################
# Other globals
############################################################################
my ($pageRoot, $config, %CONFIG, @required, @typeChecks, $configRoot,
	$query, $child, @bindVals, %sqlVals, %sqlCount, @listSql, $base);
my $parent = $$;
my @ignored = ('SoupermailConf');
my $CRLF = "\015\012";


############################################################################
# Some default configuration values
############################################################################
my $today				= time;
$CONFIG{'expirydate'}	= $today;
$CONFIG{'subject'}		= "Form Submission";
$CONFIG{'error'}		= "";
$CONFIG{'successcookie'}= 1;
$CONFIG{'failurecookie'}= 0;
$CONFIG{'blankcookie'}	= 0;
$CONFIG{'expirescookie'}= 0;
$CONFIG{'cgiwrappers'}	= 0;
$CONFIG{'pgpuploads'}	= 1;
$CONFIG{'pgppdfs'}		= 1;
$CONFIG{'pgptextmode'}	= 0;
$CONFIG{'counter'}		= {};
$CONFIG{'charset'}		= 'iso-8859-1';
$CONFIG{'encoding'}		= '8BIT';
$CONFIG{'pgpmime'}		= 1;
$CONFIG{'alphasort'}	= 1;
$CONFIG{'encodesubjects'}= 0;
$CONFIG{'successmime'}	= 'text/html';
$CONFIG{'failuremime'}	= 'text/html';
$CONFIG{'blankmime'}	= 'text/html';
$CONFIG{'expiresmime'}	= 'text/html';
$CONFIG{'listprecedence'}= 'list';
$CONFIG{'defaultencryption'} = 'gpg';
$CONFIG{'charset'}		= 'iso-8859-1';
$CONFIG{'sqluser'}		= "";
$CONFIG{'sqlpassword'}	= "";
$CONFIG{'sqlname'}		= "";
$CONFIG{'listbase'}		= "";
$CONFIG{'mailbase'}		= "";
$CONFIG{'senderbase'}	= "";

my %needToReplace = ();
### These are the config options that can use variable replacement
my $replaceable = "^(mailto|(sender)?replyto|senderfrom|${cookieStr}value|" .
				  '(sender)?subject|(sender)?bcc|ref|fileto|error|' .
				  'goto(success|blank|expires|failure))';
my $scratchPad = "";
my $OS;
my $attachCount = 1;
my $eToken = q([\w\-\.\!\#\$\%\^\&\*\{\}\'\|\+\`\~]);

### Taint things if we're not private
my $privateConfig = 0;
my $denyFile = "soupermail.deny";
my $allowFile = "soupermail.allow";

if ($^O =~ /MSWin/i) {
	$OS = "windows";
} else {
	$OS = "unix";
}

### Just in case people didn't read the instructions :)
$serverRoot =~ s/[\/\\]$//;
### Concatenate dir breaks into single ones.
$serverRoot =~ s/[\/\\]+/\//g;


### Speed things up by interpreting only what we need

my $fileFunctions =<<'END_OF_FILE_FUNCTIONS';
############################################################################
# Subroutine: hideFile ( filename )
# Make an OS specific call to hide a file from the webserver
# makes the file hidden under windows, chmoded under unix
############################################################################
sub hideFile {
	($debug) && (print STDERR "hideFile (@_) \@ " . time . "\n");
	my $filename = shift;
	no strict 'subs';
	if ($OS eq "windows") {
		Win32::File::SetAttributes($filename, Win32::File::HIDDEN)
	} else {
		if ($CONFIG{"cgiwrappers"}) {
			chmod 0600, $filename;
		} else {
			chmod 0266, $filename;
		}
	}
}

############################################################################
# Subroutine: saveResults ()
# Save the results to a file called $fileto
############################################################################
sub saveResults {
	($debug) && (print STDERR "saveResults (@_) \@ " . time . "\n");
	my $outstring = "";
	my $outbuffer = "";
	my ($value, $tmpfile);
	if ($CONFIG{'filetemplate'}) {
		grabFile($CONFIG{'filetemplate'}, \$outbuffer);
		if ($CONFIG{'nofilecr'}) {
			substOutput(\$outbuffer, '2');
		} else {
			substOutput(\$outbuffer, '0');
		}
		$outbuffer =~ s/\cM?\n$//;
	} else {
		my (@keylist) = sort($query->param());
		my ($key);
		foreach $key (@keylist) {
			### Because we may be dealing with multiple values, need to
			### join with a comma.
			$value = join(',', $query->param($key));
			$value =~ s/\cM?\n/ /g if ($CONFIG{'nofilecr'});
			$outbuffer .= "$key = $value\n";
		}
	}
	my ($header, $footer, $fileto) = "";
	if ($CONFIG{'headings'}) {
		grabFile($CONFIG{'headings'}, \$header);
	}
	if ($CONFIG{'footings'}) {
		grabFile($CONFIG{'footings'}, \$footer);
	}
	showFile($CONFIG{'fileto'});

	if (-f $CONFIG{'fileto'}) {
		my @fileStats = stat($CONFIG{'fileto'});
		### Is the file going to be bigger than the maximum?
		if ($CONFIG{'filemaxbytes'} && 
			($fileStats[7] + length($outbuffer)) > $CONFIG{'filemaxbytes'}) {
			### Yes, it is too big, but first see if it needs copying.
			if ($CONFIG{'filebackupformat'}) {
				copy($CONFIG{'fileto'}, $CONFIG{'filebackupformat'});
				hideFile($CONFIG{'filebackupformat'}) 
					unless ($CONFIG{'filereadable'});
			}
			### Now delete it.
			unlink $CONFIG{'fileto'};
		} else {
			grabFile($CONFIG{'fileto'}, \$fileto);
		}
	}

	$fileto = $header . $footer unless ($fileto);
	if ($CONFIG{'filepgpuserid'}) {
		pgpMessage(\$outbuffer, $CONFIG{'filepgpuserid'});
	}

	open (FILETO, "> $CONFIG{fileto}") ||
		fatal("Failed to write data file:\n\n    $CONFIG{fileto}");
	($fileLocking) && flock(FILETO, LOCK_EX);
	if ($CONFIG{'fileattop'}) {
		### want to add new entries to top of file.
		print FILETO $header;
		print FILETO $outbuffer;
		print FILETO substr($fileto, length($header));
	} else {
		if ($footer) {
			print FILETO substr($fileto, 0, (-1 * length($footer)));
		} else {
			print FILETO $fileto;
		}
		print FILETO $outbuffer;
		print FILETO $footer;
	}
	($fileLocking) && flock(FILETO, LOCK_UN);
	close (FILETO);

	hideFile($CONFIG{'fileto'}) unless ($CONFIG{'filereadable'});
	return 1;
}

sub genFileto {
	$CONFIG{'fileto'} = makePath(translateFormat($CONFIG{'fileto'}));
	$CONFIG{'fileto'} =~ m!^(.*)/[^/]*$!;
	my $tmpFileName = $1;

	### We have to check to see if its writable, or at least the
	### directory where it'll be created is writable. Also check
	### the file's a read file and not a symlink
	fatal ("Can not write to fileto of:\n\n    $CONFIG{fileto}") 
		if ((-e $CONFIG{'fileto'} && ! -w $CONFIG{'fileto'}) ||
			(-e $CONFIG{'fileto'} && -l $CONFIG{'fileto'}) ||
			(! -e $CONFIG{'fileto'} && ! -w $tmpFileName));
}
END_OF_FILE_FUNCTIONS


my $templateFunctions =<<'END_OF_TEMPLATE_FUNCTIONS';
############################################################################
# Subroutine: getOutVals ( name, {attributes}, iscounter )
# Given a variable name and an assoc array of attributes, return a list
# of values with appropriate formatting. The value of iscounter is set by
# reference.
############################################################################
sub getOutVals {
	my @nameoutput = ();
	$_ = shift;
	my $at = shift;
	my $isCounter = shift;
	my %ATTRIBS = %$at;
	$debug && print STDERR "In getOutVals with $_\n";

	$ATTRIBS{'format'} = '%ddd% %mmmm% %dd% %yyyy%' if (/^http_date/ && 
						 !$ATTRIBS{'format'});
	$ATTRIBS{'format'} = '%hhhh%:%mm%:%ss%' if (/^http_time/ && 
						 !$ATTRIBS{'format'});
	$$isCounter = 0;

	if (/^http_[a-zA-Z_]+$/) {
		if (!/^http_(time|date)$/) {
			push(@nameoutput, getHttpValue($_)) if (getHttpValue($_));
		} else {
			push(@nameoutput, translateFormat($ATTRIBS{'format'},
											  $ATTRIBS{'timeoffset'}));
		}
	} elsif (/^cookie_([\w\-]+)/) {
		push(@nameoutput, $query->cookie($1)) if ($query->cookie($1));
	} elsif (/^counter_(\d+)/i) {
		push(@nameoutput, $CONFIG{"counter"}->{"${1}value"})
			if ($CONFIG{"counter"}->{"${1}value"});
		$$isCounter = (!$CONFIG{"counter"}->{"${1}value"});
	} elsif (/^maillist_(\d+)$/) {
		if ($CONFIG{"maillistdata"}) {
			push(@nameoutput, $CONFIG{"maillistdata"}->{$1});
		}
	} elsif (/^sql_\d+_\d+_\d+$/) {
		push(@nameoutput, $sqlVals{$_}) if ($sqlVals{$_} || $sqlVals{$_} eq '0');
	} else {
		push(@nameoutput, $query->param($_));
	}
	if ($ATTRIBS{'format'} =~ /^\%(c+)\%$/) {
		my $span = length($1);
		@nameoutput = map { s/\D//g; s/(\d{0,$span})/$1 /g; s/\s+$//s; $_; } 
						  @nameoutput;
	}
	return @nameoutput;
}



############################################################################
# doMaths ( element_list, element_name, attributes )
# For every element in the list, perform the maths function specified in 
# the math attribute. Assume this is for the element named element_name
############################################################################
sub doMaths {
	my $list = shift;
	my $name = shift;
	my $at = shift;
	my $isCounter = 0;

	my $expr = $at->{'math'};
	$expr =~ s/\s//g;
	my $toEval = "";
	my $mathSyms = '\)\(\+\-\*\/';

	$debug && print STDERR "In doMath with $expr\n";

	while ($expr =~ /[sS][uU][mM]\(([^\)]+)\)/) {
		my $var = $1;
		my @vals = getOutVals($var, $at, \$isCounter);
		my $sum = 0;
		for (@vals) {
			if (/^(\-?(\d*\.)?\d+)$/) {
				$sum += $_;
			}
		}
		$expr =~ s/[sS][uU][mM]\(\Q$var\E\)/$sum/g;
	}

	while ($expr =~ /[cC][oO][uU][nN][tT]\(([^\)]+)\)/) {
		my $var = $1;
		my @vals = getOutVals($var, $at, \$isCounter);
		my $cnt = scalar(@vals);
		$expr =~ s/[cC][oO][uU][nN][tT]\(\Q$var\E\)/$cnt/g;
	}

	my @breakdown = split(/([^$mathSyms]+)/, $expr);
	$debug && print STDERR ("Breakdown = " . join(" | ", @breakdown) . "\n");
	for (@breakdown) {
		if (/^\s*([$mathSyms]+|(?:\d*\.)?\d+)\s*$/) {
			s/^0+([^\.])/$1/;
			$toEval .= $_;
		} elsif ($_ ne $name && $_) {
			my @vals = getOutVals($_, $at, \$isCounter);
			if ($vals[0] && $vals[0] =~ /^(\-?(\d*\.)?\d+)$/) {
				my $x = sprintf("%f", $vals[0]);
				$toEval .= "(" . $x . ")";
			} elsif ($_) {
				$toEval .= "0";
			}
		} elsif ($_) {
			$toEval .= $name;
		}
	}

	$toEval =~ s/([$mathSyms])(\-(?:(\d*\.)?\d+))/$1\($2\)/g;
	$toEval =~ s/\)\(\-(\d)/\)-\($1/g;
	$debug && print STDERR "to eval is $toEval\n";
	my $i = 0;
	while ($i < scalar(@$list)) {
		my $thisEval = $toEval;
		my $rep = ($list->[$i] ? 
			($list->[$i] =~ /^(\-?(\d*\.)?\d+)$/ ? 
				$list->[$i] : "1") : "0");
		$thisEval =~ s/\Q$name\E/$list->[$i]/g;
		$thisEval =~ s/[^${mathSyms}\.\d]//g;
		$debug && print STDERR "Evaling $thisEval\n";
		my $r = eval($thisEval);
		if ($at->{'precision'} =~/^(\-?)\d+$/) {
			### allow for negative precisions for the fractional portion
			if ($1) {
				$at->{'precision'} = $at->{'precision'} * -1;
				$r = $r - int($r);
				$r = sprintf("%." . $at->{'precision'} . "f", $r);
				$r =~ s/.*\.//;
			} else {
				$r = sprintf("%." . $at->{'precision'} . "f", $r);
			}
		}
		$list->[$i] = ($r ? $r : ($@ ? "NaN" : "0"));
		$i++;
	}
}



############################################################################
# Subroutine: URLunescape ( string )
# Takes a URL escaped string and unencodes it. Again pinched from CGI.pm
############################################################################
sub URLunescape {
	($debug) && (print STDERR "URLunescape (@_) \@ " . time . "\n");
	my $todecode = shift;
	return undef unless defined($todecode);
	$todecode =~ tr/+/ /;	   # pluses become spaces
	$todecode =~ s/%([0-9a-fA-F]{2})/pack("c",hex($1))/ge;
	return $todecode;
}

############################################################################
# Subroutine: substOutput ( buffer_containing_output_tags,
#							flag_to_specify_format )
# Substitute all instances of the output tag in a string
# returning the substituted string
# $format is '0' for no changes
#			'1' for output newlines as HTML <br> elements
#			'2' for remove all newlines, and replace with space characters.
#			'4' prepare the output for lout
############################################################################
sub substOutput {
	($debug) && (print STDERR "substOutput (@_) \@ " . time . "\n");
	my ($buffer, $format, $includes) = @_;
	my ($tempstring, $endstring, $outstring, $doLines) = "";
	$outstring = "";
	doLoops($buffer);
	$$buffer =~ s#<only\s+if\s*=\s*(?:"([^"]+)"|'([^']+)')\s*>(.*?)</only>#
				  subOnly($3,$1,$2)#siexg;
	while ($$buffer =~ /(<output(\s+[^>\s]+?\s*=\s*('[^']*'|
							"[^\"]*"|[^\s>]+))+\s*>)/iox) {
		$$buffer = $';
		$endstring = $`;
		($tempstring, $doLines) = translateOutput($1);
		$tempstring =~ s/\n/<br \/>/g if ($format == 1 && !$doLines);
		$tempstring =~ s/\cM?\n/ /g if ($format == 2);
		$tempstring = clean4Lout($tempstring) if ($format == 4);
		$outstring .= "$endstring$tempstring";
	}
	$$buffer = "$outstring$$buffer";
	$outstring = "";
	if ($format == 1 || $includes) {
		### CRAZZEEEE!!! do SSI type includes if its a HTML format type
		### substitution.
		while ($$buffer =~ /<\!\-\-\#include\s+virtual\s*=\s*
							("([^"]+)"|'([^']+)'|(\S+))\s*
							(type\s*=\s*(?:html|"html"|'html')\s*)?-->/xi) {
			$$buffer = $';
			$endstring = $`;
			$tempstring = "";
			my $incFile = $2;
			$incFile = $3 if ($3);
			$incFile = $4 if ($4);
			my $needsEncoding = $5;
			($debug) && (print STDERR "including $incFile\n");
			$incFile = makePath($incFile);
			if (-f $incFile && -r $incFile &&
				-T $incFile) {
				grabFile($incFile, \$tempstring);
			}
			$tempstring = clean4Lout($tempstring) if ($format == 4);
			$tempstring = dehtml(undef, $tempstring) if ($needsEncoding);
			$outstring .= "$endstring$tempstring";
		}
	}
	$$buffer = $outstring . $$buffer;
}


############################################################################
# Subroutine: subOnly ( replace_data, condition [, condition ] )
# Return the replacement text if the condition is true
############################################################################
sub subOnly {
	my $repTxt = shift;
	my $cond = shift;
	$cond = shift unless ($cond);
	return (evalCond($cond) ? $repTxt : "");
}


############################################################################
# Subroutine: translateOutput ( output_tag_string )
# Take a tag in the form <output ...> and return the value based on
# %rqpairs. If no pair exists, return "".
############################################################################
sub translateOutput {
	($debug) && (print STDERR "translateOutput (@_) \@ " . time . "\n");
	my ($line) = shift;
	my ($name, $attrib, $tag, $nameoutput) = "";
	my (@nameoutput) = ();
	my (%ATTRIBS) = ();
	my (%SETATTRIBS) = ();
	my $isCounter = 0;
	my $newlineTrans = 0;
	my $matchVal = 1;
	my $matchData = 1;

	### Some attributes can be declared multiple times. define them here
	my $multiAttr = { charmap => 1 };
	foreach (keys %$multiAttr) {
		$ATTRIBS{$_} = [];
	}

	$ATTRIBS{'list'} = $ATTRIBS{'post'} = $ATTRIBS{'pre'} = $ATTRIBS{'case'} =
		$ATTRIBS{'name'} = $ATTRIBS{'sub'} = $ATTRIBS{'alt'} = 
		$ATTRIBS{'math'} = $ATTRIBS{'format'} = $ATTRIBS{'delim'} = 
		$ATTRIBS{'type'} = $ATTRIBS{'indent'} = $ATTRIBS{'newline'} = 
		$ATTRIBS{'altvar'} = $ATTRIBS{'subvar'} = 
		$ATTRIBS{'value'} = $ATTRIBS{'valuevar'} = $ATTRIBS{'data'} = 
		$ATTRIBS{'wrap'} = $ATTRIBS{'timeoffset'} = "";

	while ($line =~ /(\w+)\s*=\s*("[^"]*"|'[^']*'|[^\s>]+)/) {
		print STDERR "Translating $line\n" if ($debug);
		$line = $';
		$attrib  = lc($1);
		$tag = $2;
		$tag =~ s/^'([^']*)'/$1/ unless ($tag =~ s/^"([^"]*)"/$1/);
		if ($multiAttr->{$attrib}) {
			push(@{$ATTRIBS{$attrib}}, $tag);
		} else {
			$ATTRIBS{$attrib} = $tag;
		}
		$SETATTRIBS{$attrib} = 1;
	}
	$ATTRIBS{'name'} =~ s/^\s*([\S])/$1/;
	$ATTRIBS{'name'} =~ s/(.*[\S])\s*$/$1/;
	$_ = $ATTRIBS{'name'};
	securityName($_);

	@nameoutput = getOutVals($_, \%ATTRIBS, \$isCounter);

	### Firstly, it should be unescaped if needed.
	if ($ATTRIBS{'type'} =~ /^unescaped(html)?$/i) {
		@nameoutput = map { URLunescape($_); } @nameoutput;
	} elsif ($ATTRIBS{'type'} =~ /^sql$/i) {
		push(@{$ATTRIBS{'charmap'}}, "',''");
		$SETATTRIBS{'charmap'} = 1;
	}

	if (scalar(@nameoutput) && $ATTRIBS{'subvar'} &&
		(!$SETATTRIBS{'valuevar'} || $nameoutput[0] eq $ATTRIBS{'valuevar'})) {
		securityName($ATTRIBS{'subvar'});
		$debug && print STDERR "subvar replace $_ with $ATTRIBS{'subvar'}\n";
		$_ = $ATTRIBS{'subvar'};
		@nameoutput = getOutVals($_, \%ATTRIBS, \$isCounter); 
	} elsif ((!scalar(@nameoutput) || ($SETATTRIBS{'valuevar'} &&
			 $nameoutput[0] ne $ATTRIBS{'valuevar'})) && $ATTRIBS{'altvar'}) {
		securityName($ATTRIBS{'altvar'});
		$debug && print STDERR "altvar replace $_ with $ATTRIBS{'altvar'}\n";
		$_ = $ATTRIBS{'altvar'};
		@nameoutput = getOutVals($_, \%ATTRIBS, \$isCounter); 
	}
	if ($SETATTRIBS{'value'}) {
		$matchVal = ($nameoutput[0] eq $ATTRIBS{'value'}) ? 1 : 0;
	}
	if ($SETATTRIBS{'data'} && scalar(@nameoutput)) {
		$ATTRIBS{'data'} =~ s/^\s*(.*?)\s*$/\L$1\E/;
		$debug && print STDERR "data $nameoutput[0] as a $ATTRIBS{'data'}\n";
		$matchData = !checkType($ATTRIBS{'data'},$nameoutput[0]);
		$debug && print STDERR "check results in $matchData\n";
	}

	### We can now apply various transformations on the data.
	### Upper of lowercase
	if ($ATTRIBS{'case'} =~ /^upper$/i) {
		@nameoutput = map { uc($_); } @nameoutput;
	} elsif ($ATTRIBS{'case'} =~ /^lower$/i) { 
		@nameoutput = map { lc($_); } @nameoutput;
	}
	
	### Perform maths functions
	if ($ATTRIBS{'math'}) {
		doMaths(\@nameoutput, $_, \%ATTRIBS);
	}

	### Map special character
	if ($SETATTRIBS{'charmap'}) {
		foreach (@{$ATTRIBS{'charmap'}}) {
			if (m!(.)\,(.*)!) {
				my $fromChar = $1;
				my $toStr = $2;
				$debug && print STDERR "Char mapping -${fromChar}- to -${toStr}-\n";
				$debug && print STDERR "(" . join("),(", @nameoutput) . ")\n";
				@nameoutput = map { s/\Q$fromChar\E/$toStr/gs;$_; } @nameoutput;
				$debug && print STDERR "(" . join("),(", @nameoutput) . ")\n";
			}
		}
	}

	if ($ATTRIBS{'type'} =~ /^escaped$/i) {
		@nameoutput = map { URLescape($_); } @nameoutput;
	} elsif ($ATTRIBS{'type'} =~ /^(unescaped)?html$/i) {
		@nameoutput = map { dehtml($1,$_); } @nameoutput;
	}

	# Wrap the element
	if ($ATTRIBS{'wrap'} && $ATTRIBS{'wrap'} =~ /^0*[1-9][0-9]*$/) {
		my $wrapCnt = 0;
		while ($wrapCnt < scalar(@nameoutput)) { 
			wrapText($ATTRIBS{'wrap'}, \${nameoutput[$wrapCnt++]});
		}
	}

	if ($ATTRIBS{'newline'} =~ /^html$/i) {
		@nameoutput = map { s/(\r?\n)/<br>\n/gs;$_; } @nameoutput;
		$newlineTrans = 1;
	} elsif ($ATTRIBS{'newline'} =~ /^none$/i) {
		@nameoutput = map { s/(\r?\n)/ /gs;$_; } @nameoutput;
		$newlineTrans = 1;
	} elsif ($ATTRIBS{'newline'} =~ /^paragraphs$/i) {
		@nameoutput = map { s/(\r?\n){3,}/\n\n/gs;$_; } @nameoutput;
		@nameoutput = map { s/(\r?\n){1,1}/\n/gs;$_; } @nameoutput;
		$newlineTrans = 1;
	} elsif ($ATTRIBS{'newline'} =~ /^unchanged$/i) {
		$newlineTrans = 1;
	}
	
	if (@nameoutput || $nameoutput || $isCounter) {
		### Now we have to be smart and handle multiple lists. Default
		### behavior is to display multiples as HTML UL lists, but can
		### be overridden by the list tag of OL, DIR or MENU.
		if (!$SETATTRIBS{'sub'} && ($ATTRIBS{'list'} || scalar(@nameoutput) > 1 )) {
			if ($SETATTRIBS{'delim'}) {
				$nameoutput= join("$ATTRIBS{post}$ATTRIBS{delim}$ATTRIBS{pre}",
								  @nameoutput);
				return("$ATTRIBS{pre}$nameoutput$ATTRIBS{post}", $newlineTrans);
			} elsif ($ATTRIBS{'list'} =~ /TEXT/i) {
				### Plain text list.
				$nameoutput = join("$ATTRIBS{post}\n	* $ATTRIBS{pre}",
									@nameoutput);
				return("\n	* $ATTRIBS{pre}$nameoutput$ATTRIBS{post}\n", 
					   $newlineTrans);
			} else {
				$ATTRIBS{'list'} = 'UL' unless ($ATTRIBS{'list'} ne "");
				$nameoutput = join ("$ATTRIBS{post}<LI>$ATTRIBS{pre}",
									@nameoutput);
			   
				return("<$ATTRIBS{list}><LI>$ATTRIBS{pre}" .
						"$nameoutput$ATTRIBS{post}</$ATTRIBS{list}>", 
						$newlineTrans);
			}
		} else {
			$nameoutput = $nameoutput[0] unless ($nameoutput);
			if ($SETATTRIBS{'sub'} && $matchVal && $matchData) {
				return($ATTRIBS{'sub'},0);
			} elsif ($matchVal && $matchData) {
				if ($SETATTRIBS{'indent'}) {
					$nameoutput =~ s/(\cM?\n)/$1$ATTRIBS{'indent'}/g ;
					$nameoutput = $ATTRIBS{'indent'} . 
									($isCounter ? '0' : $nameoutput);
					$isCounter = 0;
				}
				return("$ATTRIBS{pre}" .
						($isCounter ? '0' : $nameoutput) . "$ATTRIBS{post}",
						$newlineTrans);
			} else {
				return($ATTRIBS{'alt'},0);
			}
		}
	} else {
		return($ATTRIBS{'alt'},0);
	}
}

sub doLoops {
	my $data = shift;
	my $loopCnt = 0;
	my $pos = 0;
	my $buffer = "";
	my $num = "-?(?:\\d+|\\d*\\.\\d+)";
	my @els = split(/(<loop\s+[^>]+>|<\/loop>)/m, $$data);
	my $max = 0;

	while (@els && $max++ < 10000) {
    	my $el = $els[$pos];
		my $isLoop = ($el =~ /^<loop\s+[^>]+>/i);
		my $isEndLoop = ($el =~ /^<\/loop>/i);
		if ($isLoop && $#els > 1) {
        	$loopCnt++;
        	$pos++;
		} elsif ($isLoop) {
			splice(@els, $pos, 1);
			$pos--;
		} elsif ($isEndLoop) {
			if ($loopCnt > 0) { $loopCnt--; }
			if ($pos >= 1) {
				my $e1 = $els[$pos - 1];
				my $p1 = $pos - 1;
				my $p2 = $pos - 2;
				my $e2 = $els[$p2];
				my $start = undef;
				my $end = undef;
				my $step = 1;
				my $name = "";
				my $field = "";
				my $sql = "";
				#get loop data from $els[$p2];
				if ($e2 =~ /\sstart\s*=\s*(?:"($num)"|'($num)'|($num))/i) {
					$start = $+;
				}
				if ($e2 =~ /\send\s*=\s*(?:"($num)"|'($num)'|($num))/i) {
					$end = $+;
				}
				if ($e2 =~ /\sstep\s*=\s*(?:"($num)"|'($num)'|($num))/i) {
					$step = $+;
				}
				if ($e2 =~ /\sname\s*=\s*(?:"(\w+)"|'(\w+)'|(\w+))/i) {
					$name = $+;
				}
				if ($e2 =~ /\sfield\s*=\s*(?:"([\-\.\w]+)"|'([\-\.\w]+)'|([\-\.\w]+))/i) {
					if ($query->param($+)) { $field = $+; }
				}
				if ($e2 =~ /\ssqlrun\s*=\s*(?:"(\d+)"|'(\d+)'|(\d+))/i) {
					$sql = $+;
				}
				my @flist = ();
				if ($field) {
					@flist = $query->param($field);
					if ($step > 0) {
						$start = 0 unless ($start && $start > 0);
						$end = $#flist unless ($end && $end < $#flist);
					} else {
						$start = $#flist unless ($start && $start < $#flist);
						$end = 0 unless ($end && $end > 0);
					}
				}
				if ($sql) {
					if ($step > 0) {
						$start = 1;
						$end = $sqlCount{$sql};
					} else {
						$start = $sqlCount{$sql};
						$end = 1;
					}
				}
				# are we able to loop?
				my $tmpBuff = "";
				if (defined($start) && defined($end) &&
					(($step > 0 && $start <= $end) ||
					($step < 0 && $start >= $end))) {
					my $a = $start;
					my $b = $end;
					while (($step > 0 && $a <= $b) || ($step < 0 && $a >= $b)) {
						my $data = $e1;
						if ($name) {
							if (@flist) {
								$data =~ s/\@$name\@/$flist[$a]/sg;
							} else {
								$data =~ s/\@$name\@/$a/sg;
							}
						}
						$tmpBuff .= $data;
						$a += $step;
					}
				}
				my $o = ($pos > 2) ? 3 : 2;
				if ($o == 3) {
					$els[$pos - $o] .= $tmpBuff;
				} else {
					$els[$pos - $o] = $tmpBuff;
				}
				if  ($pos + 1 <= $#els) {
					$els[$pos - $o] .= $els[$pos + 1];
					splice(@els, $pos + 1, 1);
				}
				splice(@els, $pos - $o + 1, $o);
			}
			$pos = 0;
			$loopCnt = 0;
		} elsif ($loopCnt == 0) {
			# not in a loop, so this can be added to the content
			$buffer .= shift(@els);
		} elsif ($pos >= $#els) {
			# end of the line... if we're here, then there are
			# unclosed loops - join the array, and shove it on buffer.
			$buffer .= join("", @els);
			@els = ();
			$pos = 0;
		} elsif (!$isLoop && !$isEndLoop) {
			$pos++;
		}
	}
	$$data = $buffer;
}


END_OF_TEMPLATE_FUNCTIONS


my $pdfFunctions =<<'END_OF_PDF_FUNCTIONS';
sub makePdf {
	my $template = shift;
	my $pdfName = shift;
	$pdfName =~ s!(.*/)([^/]+)(\.[^/]*)$!$2\.pdf!;
	my $pdfDir = $1;
	($debug) && print STDERR "pdfDir is $pdfDir\n";
	my $fname = "$scratchPad/$pdfName";
	if ($ps2pdf && $lout && -d $scratchPad) {
		opendir (PDFDIR, $pdfDir);
		my @epsFiles = grep { /^[^\.]/ && /\.eps$/i } readdir(PDFDIR);
		closedir (PDFDIR);
		for (@epsFiles) {
			($debug) && print STDERR "copying $pdfDir$_\n";
			copy("${pdfDir}$_", "${scratchPad}/$_");
		}
		open (LIN, ">${scratchPad}/lout.in");
		print LIN $$template;
		close (LIN);
		my $cmd1 = "$lout $loutOpts lout.in >lout.ps";
		my $cmd2 = "$ps2pdf lout.ps ${fname}";
		($debug) && print STDERR "fname is $fname\n";
		($debug) && print STDERR "Running $cmd1\nand\n$cmd2\n";
		chdir ($scratchPad);
		system("$cmd1");
		system("$cmd2");
		if ($fname) {
			return $fname;
		}
	}
	return "";
}


sub clean4Lout {
	my $val = shift;
	$val =~ s/[\t ]+/ /gs;
	$val =~ s/([\"\\])/\"\\$1\"/gs;
	$val =~ s/([\#\&\/\@\^\{\|\}\~])/\"$1\"/gs;
	$val =~ s/(\r?\n){2,2}/\n\@LP\n/gs;
			 
	# Win latin stuff... can we check for this in form
	# enctype?
	$val =~ s/\x82/ \@Char quotesinglbase /gs;
	$val =~ s/\x83/ \@Florin /gs;
	$val =~ s/\x84/ \@Char quotedblbase /gs;
	$val =~ s/\x85/ \@Char ellipsis /gs;
	$val =~ s/\x86/ \@Dagger /gs;
	$val =~ s/\x87/ \@DaggerDbl /gs;
	$val =~ s/\x88/ \@Char circumflex /gs;
	$val =~ s/\x8a/ \@Char S /gs;
	$val =~ s/\x8c/ \@Char OE /gs;
	$val =~ s/\x91/ \@Char quoteleft /gs;
	$val =~ s/\x92/ \@Char quoteright /gs;
	$val =~ s/\x93/ \@Char quotedbl /gs;
	$val =~ s/\x94/ \@Char quotedbl /gs;
	$val =~ s/\x95/ \@Sym bullet /gs;
	$val =~ s/\x96/ \@Char endash /gs;
	$val =~ s/\x97/ \@Char emdash /gs;
	$val =~ s/\x99/ \@Sym trademarkserif /gs;
	$val =~ s/\x9c/ \@Char oe /gs;
	$val =~ s/\x9e/ \@Char z /gs;
	$val =~ s/\x9f/ \@Char Y /gs;
	return $val;
}
END_OF_PDF_FUNCTIONS


my $mailFunctions =<<'END_OF_MAIL_FUNCTIONS';

############################################################################
# Subroutine: attachFilesToMail (fileset_name, message_ref, has_body_content)
# This attaches files to a message body.
############################################################################
sub attachFilesToMail {
	my $type = shift;
	my $msg = shift;
	my $hasBody = shift;
	my ($key, $file);
	while (($key, $file) = each %{$CONFIG{$type}}) {
		($debug) && print STDERR "examining attachment $key, $file\n";
		next unless ($key =~ /(\d+)file/ && -f $file);
		my $attachNum = $1;
		$file =~ m!/([^/]+)$!;
		my $filename = $1;
		my $mime_type = 
			$CONFIG{$type}->{"${attachNum}mime"};
		($debug) && print STDERR "Attaching a mime type of $mime_type for $filename ($key)\n";
		unless ($mime_type) {
			$mime_type = (!$fhBug && -T $file) ? 'text/plain' :
									'application/octet-stream';
		}
		my @stats  = stat($file);
		($debug) && print STDERR "Attaching $file ($stats[7] bytes) " .
								 "to email\n";
		my $data = { Path => $file,
					 ReadNow => 1,
					 Filename => $filename
					 };
		unless ($mime_type =~ /^text\//) {
			$data->{'Encoding'} = "base64";
		}

		if (!$hasBody) {
			$$msg->data("This is a MIME message with attachments");
		}
		my $m = $$msg->attach(%$data);
		$m->attr("content-type" => $mime_type);
	}
}

############################################################################
# Subroutine: fakeEmail (address)
# MIME::Lite doesn't like sending odd email From addresses, so make them
# look a bit saner.
############################################################################
sub fakeEmail {
	($debug) && (print STDERR "fakeEmail (@_) \@ " . time() . "\n");
	$_ = shift(@_);
	if (!/\@.+/) { $_ .= "\@localhost"; }
	s/\@+/@/g;
	($debug) && (print STDERR "fakeEmail returns $_\n");
	return $_;
}

############################################################################
# Subroutine: mailResults ()
# Mail the results to the people in $mailto and also send back a mail to the
# form's sender using the sendertemplate config field.
############################################################################
sub mailResults {
	($debug) && (print STDERR "mailResults (@_) \@ " . time() . "\n");
	my ($outstring, $messageBuffer, $value, $tmpfile, $mailbuffer) = "";
	my ($mailto, $email, $tmp, $theirMail);
	my $t = time();

	if ($CONFIG{'encodesubjects'} && $CONFIG{'charset'} !~ /^us-ascii$/i) {
		foreach ('subject', 'sendersubject') {
			my $s = substr(MIME::Lite::encode_base64($CONFIG{$_}), 0, -2);
			$CONFIG{$_} = "=?" . $CONFIG{'charset'} . "?B?" .  $s . "?=";
		}
	}

	checkEmail($email) if ($email = $query->param('Email'));

	$mailto = $CONFIG{'mailto'};
	$mailto = $email if (!$mailto && $CONFIG{'returntosender'} && $email);

	### Handle a sendertemplate setting.
	if ($email && ($CONFIG{'sendertemplate'} || $CONFIG{'htmlsendertemplate'} ||
				   $CONFIG{'pdfsendertemplate'})
		&& ($mailto || $CONFIG{'replyto'} || $CONFIG{'senderreplyto'} ||
			$CONFIG{'senderfrom'} || $email)) {
		print STDERR "Should be sending a mail to the sender\n" if ($debug);
		
		my $theirTemplate = "";
		my $theirHtmlTemplate = "";
		my $theirPdfTemplate = "";
		my $hasBody = 0;
		my $senderFrom = $CONFIG{'senderfrom'} ? $CONFIG{'senderfrom'} :
						($CONFIG{'senderreplyto'} ? $CONFIG{'senderreplyto'} :
						($mailto ? $mailto : 
							($CONFIG{'replyto'} ? $CONFIG{'replyto'} : 
								$email)));
		my $senderMsg = MIME::Lite->build(
							  'From' => $senderFrom,
							  'To' => $email,
							  'Subject' => ($CONFIG{'sendersubject'} ? 
											  $CONFIG{'sendersubject'} :
											  $CONFIG{'subject'}),
							  'Reply-To' => ($CONFIG{'senderreplyto'} ? 
											  $CONFIG{'senderreplyto'} :
												  ($CONFIG{'replyto'} ? 
													  $CONFIG{'replyto'} : 
													  $mailto)),
							  'Bcc' => $CONFIG{'senderbcc'},
							  'Encoding' => $CONFIG{'encoding'},
						);

		if ($CONFIG{'sendertemplate'}) {
			grabFile($CONFIG{'sendertemplate'}, \$theirTemplate);
			substOutput(\$theirTemplate, '0', 1);
		}
		if ($CONFIG{'htmlsendertemplate'}) {
			grabFile($CONFIG{'htmlsendertemplate'}, \$theirHtmlTemplate);
			substOutput(\$theirHtmlTemplate, '0', 1);
		}
		if ($CONFIG{'pdfsendertemplate'}) {
			($debug) && print STDERR "Translating pdf sender template\n";
			grabFile($CONFIG{'pdfsendertemplate'}, \$theirPdfTemplate);
			substOutput(\$theirPdfTemplate, '4', 1);
			my $pdfFile = makePdf(\$theirPdfTemplate, 
								  $CONFIG{'pdfsendertemplate'});
			if ($pdfFile) {
				($debug) && print STDERR "Marking sender pdf as attachment\n";
				$CONFIG{"attachments"}->{"${attachCount}file"} = $pdfFile;
				$CONFIG{"attachments"}->{ $attachCount++ . "mime" } =
					"application/pdf";
			}
		}
		if ($CONFIG{'wrap'} && $theirTemplate) {
			wrapText($CONFIG{'wrap'}, \$theirTemplate);
		}
		if ($theirTemplate && $theirHtmlTemplate) {
			$hasBody = 1;
			($debug) && print STDERR "Making alt sender email\n";
			$senderMsg->attr("content-type" => 'multipart/alternative');
			$senderMsg->attr("content-type.boundary" => 'eskjdlj239w09epaods' . $$);
			my $m1 = $senderMsg->attach(
							Data => "$theirTemplate",
						);
			$m1->attr("content-type" => "text/plain; charset=$CONFIG{charset}");
			my $m2 = $senderMsg->attach(
							Data => "$theirHtmlTemplate",
						);
			$m2->attr("content-type" => "text/html; charset=$CONFIG{charset}");
			$m2->attr("content-location" => ($CONFIG{'senderbase'} ?
												$CONFIG{'senderbase'} : $base));
		} elsif ($theirHtmlTemplate) {
			$hasBody = 1;
			($debug) && print STDERR "Making HTML sender email\n";
			$senderMsg->attr('content-type' => "text/html; charset=$CONFIG{charset}");
			$senderMsg->attr('content-location' => ($CONFIG{'senderbase'} ?
													$CONFIG{'senderbase'} : $base));
			$senderMsg->data($theirHtmlTemplate);
		} elsif ($theirTemplate) {
			$hasBody = 1;
			($debug) && print STDERR "Making text sender email\n";
			$senderMsg->attr("content-type" => "text/plain; charset=$CONFIG{charset}");
			$senderMsg->data($theirTemplate);
		}
		if ($CONFIG{'attachments'}) {
			($debug) && print STDERR "Looking for sender attachments\n";
			attachFilesToMail("attachments", \$senderMsg, $hasBody);
		}
		$senderMsg->replace('X-Mailer' => "Soupermail $relVersion");
		$senderMsg->send();
	}

	my $hasMailingList = ($CONFIG{'maillist'} || ($CONFIG{"listformfield"} && 
							$query->param($CONFIG{"listformfield"})) ||
							scalar(@listSql)) && 
						($CONFIG{'listtemplate'} || $CONFIG{'htmllisttemplate'});

	return 1 unless ($mailto || $hasMailingList);

	if ($mailto) {
		my $origEnc = $CONFIG{'encoding'};
		### Since we're going through PGP ascii armoring, there's no need
		### to use 7bit safe quoted-printable messages since the data will
		### be mail transport safe.
		if ($CONFIG{'pgpuserid'}) {
			$CONFIG{'encoding'} = "8BIT";
		}

		my $footerText .= "-------------------------------\n" .
							"Remote Host: $ENV{'REMOTE_HOST'}\n" .
						  "Remote IP: $ENV{'REMOTE_ADDR'}\n" .
						  "User Agent: $ENV{'HTTP_USER_AGENT'}\n" .
						  "Referer: $ENV{'HTTP_REFERER'}\n";
		my $mailMessage = "";
		my $htmlMailMessage = "";
		my $destAddr = { 'From' => ($email) ? fakeEmail($email) : $mailto,
						 'To' => ($CONFIG{'returntosender'} && 
								  $email && $email ne $mailto) ?  
									  "$mailto, $email" : $mailto,
						 'Reply-To' => $CONFIG{'replyto'} ? 
										   $CONFIG{'replyto'} :
										   ($email ? $email : $mailto),
						 'Subject' => $CONFIG{'subject'},
						 'Bcc' => $CONFIG{'bcc'},
						 'Encoding' => $CONFIG{'encoding'}};
		my $mailtoMsg = MIME::Lite->build(%$destAddr);
		my $copyMsg = MIME::Lite->build(%$destAddr);
		if ($CONFIG{'mailtemplate'} || $CONFIG{'htmlmailtemplate'}) {
			if ($CONFIG{'mailtemplate'}) {
				grabFile($CONFIG{'mailtemplate'}, \$mailMessage);
				substOutput(\$mailMessage, '0', 1);

				$mailMessage .= "\n$footerText" unless 
					($CONFIG{'nomailfooter'});
				### If there's to be word wrapping...
				($CONFIG{'wrap'}) && (wrapText($CONFIG{'wrap'}, \$mailMessage));
			}
			if ($CONFIG{'htmlmailtemplate'}) {
				grabFile($CONFIG{'htmlmailtemplate'}, \$htmlMailMessage);
				substOutput(\$htmlMailMessage, '0', 1);
			}
			if ($mailMessage && $htmlMailMessage) {
				$mailtoMsg->attr("content-type" => 'multipart/alternative');
				$mailtoMsg->attr("content-type.boundary" => 'skfdhj384jhqoihe' . $$);
				my $m1 = $mailtoMsg->attach(
							Data => $mailMessage,
						);
				$m1->attr("content-type" => "text/plain; charset=$CONFIG{charset}");
				my $m2 = $mailtoMsg->attach(
							Data => $htmlMailMessage,
						);
				$m2->attr("content-type" => "text/html; charset=$CONFIG{charset}");
				$m2->attr("content-location" => ($CONFIG{'mailbase'} ? 
													$CONFIG{'mailbase'} : $base));
			} elsif ($htmlMailMessage) {
				($debug) && print STDERR "Making HTML mailto email\n";
				$mailtoMsg->attr('content-type' => "text/html; charset=$CONFIG{charset}");
				$mailtoMsg->attr('content-location' => ($CONFIG{'mailbase'} ?
														$CONFIG{'mailbase'} : $base));
				$mailtoMsg->data($htmlMailMessage);
			} else {
				($debug) && print STDERR "Making text  mailto email\n";
				$mailtoMsg->attr("content-type" => "text/plain; charset=$CONFIG{charset}");
				$mailtoMsg->data($mailMessage);
			} 
		} else {
			my (@keylist) = ($CONFIG{'alphasort'} ? sort($query->param()) :
													$query->param());
			my ($key);
			foreach $key (@keylist) {
				### Because we may be dealing with multiple values, need to
				### join with commas.
				$value = join(',', $query->param($key));
				$messageBuffer .= "$key = $value\n";
			}

			$messageBuffer .= "\n$footerText" unless ($CONFIG{'nomailfooter'});
			### If there's to be word wrapping...
			($CONFIG{'wrap'}) && (wrapText($CONFIG{'wrap'}, \$messageBuffer));
			### Don't encode the message if its going to a non PGP/MIME
			### destination.
		   	$mailtoMsg->attr("content-type" => "text/plain; charset=$CONFIG{charset}");
			$mailtoMsg->data($messageBuffer);
		}

		### At this point, message buffer contains the right message

		### Store a marker to see if we're splitting attachments from PGP
		my $added = 0;
		my $headSet = 0;

		### Its here that file upload should go - should restrict size
		### Pseudo code is:
		### foreach input item, look at its values
		### see if the value has a filehandle
		### if there's a filehandle, read it in to the specified size
		### MIME it up
		### print it with an appropriate mime type
		### simple :)

		if ($CONFIG{'mimeon'}) {
			foreach ($query->param()) {
				my $val;
				foreach $val ($query->upload($_)) {
					next unless ($val && fileno($val) && ref($val));
					if ($debug) {
						print STDERR "Upload $val\n";
						while (my ($n, $v) = each %{$query->uploadInfo($val)}) {
							print STDERR "	$n => $v\n";
						}
					}
					my $isText = (!$fhBug && -T $val);
					my $mime_type = "";
					if ($query->uploadInfo($val)) {
						$mime_type = $query->uploadInfo($val)->{'Content-Type'};
					}
					unless ($mime_type) {
						$mime_type = ($isText) ? 'text/plain' :
											 'application/octet-stream';
					}
					($debug) && print STDERR "Upload mime $mime_type\n";
					my $fname = $val;
					if ($query->user_agent() =~ /(PPC|Mac)\b/) {
						$fname =~ s/.*:([^:]*)/$1/;
					} else {
						 $fname =~ s/\\/\//g;
						 $fname =~ s/.*\/([^\/]*)/$1/;
					}
					($debug) && print STDERR "Upload name $fname\n";
					
					my $m;
					my $data = {Filename => $fname,FH => $val};
					unless ($mime_type =~ /^text\//) { $data->{'Encoding'} = 'base64'; }
					if ($CONFIG{'pgpuploads'}) {
						$m = $mailtoMsg->attach(%$data);
					} else {
						$added++;
						if (!$headSet) {
							$copyMsg->attr('content-type' => 'multipart/mixed');
							$copyMsg->attr('content-type.boundary' => 'sdfjeirkjf93akjl2' . $$);
						}
						$m = $copyMsg->attach(%$data);
					}
					$m->attr("content-type" => $mime_type);
				}
			}
		}

		if ($CONFIG{'pdfmailtemplate'}) {
			my $pdfTemplate = "";
			grabFile($CONFIG{'pdfmailtemplate'}, \$pdfTemplate);
			substOutput(\$pdfTemplate, '4', 1);
			my $pdfName = $CONFIG{'pdfmailtemplate'};
			my $pdfFile = makePdf(\$pdfTemplate, $pdfName);
			$pdfName =~ s!.*/([^/]+)(\.[^/]*)$!$1\.pdf!;
			if ($pdfFile) {
				($debug) && print STDERR "Putting $pdfName as an attachment\n";
				my $m;
				if ($CONFIG{'pgppdfs'}) {
					$m = $mailtoMsg->attach(
									Path => $pdfFile,
									Filename => $pdfName
									);
				} else {
					$added++;
					if (!$headSet) {
						$copyMsg->attr('content-type' => 'multipart/mixed');
						$copyMsg->attr('content-type.boundary' => 'jlyiytjr3gktasdgqbsab' . $$);
					}
					$m = $copyMsg->attach(Path => $pdfFile,
											Filename => $pdfName);
				}
				$m->attr("content-type" => 'application/pdf');
			}
		}

		if ($CONFIG{'pgpuserid'}) {
			my $encMsg = $mailtoMsg->body_as_string();
			if ($encMsg =~ /^\-\-(_\-.*)$/m) {
				$encMsg = "Content-Type: multipart/mixed; boundary=\"$1\"\r\n\r\n$encMsg";
			}
			pgpMessage(\$encMsg, $CONFIG{'pgpuserid'});
			if ($CONFIG{'pgpmime'}) {
				if (! $added) {
					$copyMsg->attr('content-type' => 'multipart/encrypted');
					$copyMsg->attr('content-type.protocol' => 'application/pgp-encrypted');
					$copyMsg->attr('content-type.boundary' => 'of3ewjlkdsi3jd9asjd' . $$);
					my $m = $copyMsg->attach(
								  Data => 'Version: 1'
							  );
					$m->attr("content-type" => 'application/pgp-encrypted');
					my $p = $copyMsg->attach(
								  Data => $encMsg
							  );
					$p->attr("content-type" => 'application/octet-stream');
				} else {
					my $subMsg = MIME::Lite->build();
					$subMsg->attr('content-type' => 'multipart/encrypted');
					$subMsg->attr('content-type.protocol' => 'application/pgp-encrypted');
					$subMsg->attr('content-type.boundary' => 'of3ekjhdsgfytdsbuJTWERKGAk' . $$);
					my $m = $subMsg->attach(
								  Data => 'Version: 1'
							  );
					$m->attr("content-type" => 'application/pgp-encrypted');
					my $p = $subMsg->attach(
								  Data => $encMsg
							  );
					$p->attr("content-type" => 'application/octet-stream');
					$copyMsg->attach($subMsg);
				}
			} else {
				if (! $added) {
					$copyMsg->data($encMsg);
					$copyMsg->attr("content-type" => 'text/plain');
				} else {
					$copyMsg->attach(Type => 'TEXT',
										Data => $encMsg);
				}
			}
			$mailtoMsg = $copyMsg;
		}


		$debug && print STDERR "Sending mail to $mailto or $email\n";
		$mailtoMsg->replace('X-Mailer' => "Soupermail $relVersion");
		$mailtoMsg->send();
		undef $messageBuffer;
		$CONFIG{'encoding'} = $origEnc;
	}

	if ($hasMailingList) {
		my $textTemplate = "";
		my $htmlTemplate = "";
		if ($CONFIG{'listtemplate'}) {
			grabFile($CONFIG{'listtemplate'}, \$textTemplate);
		}
		if ($CONFIG{'htmllisttemplate'}) {
			grabFile($CONFIG{'htmllisttemplate'}, \$htmlTemplate);
		}
		($debug) && print STDERR "Got maillist templates\n";
		my @listLines = ();
		my $maxItemCnt = 0;
		my $listReply = $CONFIG{'listreplyto'} ? $CONFIG{'listreplyto'} : 
							($email ? $email : $mailto);
		my $listFrom = $CONFIG{'listfrom'} ? $CONFIG{'listfrom'} : 
							($email ? $email : $mailto);

		### Read in the mailing list data from the file datasource
		if ($CONFIG{'maillist'}) {
			($debug) && print STDERR "Opening data file $CONFIG{maillist}\n";
			open(MAILLIST, "<$CONFIG{maillist}");
			($fileLocking) && flock(MAILLIST, LOCK_SH);
			while (<MAILLIST>) {
				chomp;
				my @bits = split(/,/);
				push(@listLines, [ 1, @bits ]);
			}
			($fileLocking) && flock(MAILLIST, LOCK_UN);
			close(MAILLIST);
		}

		### Pull the mailing list data from the form field specified
		if ($CONFIG{'listformfield'} && 
			$query->param($CONFIG{'listformfield'})) {
			($debug) && print STDERR "Getting maillist data from form field $CONFIG{listformfield}\n";
			my @lines = split(/\n/, $query->param($CONFIG{'listformfield'}));
			foreach (@lines) {
				chomp;
				my @bits = split(/,/);
				push (@listLines, [ 1, @bits ]);
			}
		}

		### Pull some mailing list data from the SQL command
		if (scalar(@listSql)) {
			push(@listLines, @listSql);
		}

		eval('use Net::SMTP;');
		my @smtpCon = ();
		my $hasSmtp = ($@ || !$mailhost ? 0 : 1);
		if ($hasSmtp) {
			### Make sure we don't generate too many threads
			if ($smtpPoolSize > scalar(@listLines)) {
				$smtpPoolSize = scalar(@listLines);
			}
			### Open up a set of connections
			for (0 .. $smtpPoolSize) {
				$smtpCon[$_] = Net::SMTP->new($mailhost);
			}
		}
		my $poolNum = -1;

		### Now loop through the mailing list data
		foreach (@listLines) {
			$poolNum++;
			$poolNum = 0 if ($poolNum > $smtpPoolSize);
			my @rawList = @$_;
			my $itemCnt = 1;
			my $inQuote = 0;
			my $item = "";
			my $subedTxt = "";
			my $subedHtml = "";
			my $subedMsg = "";
			my $undefCnt = 0;
			my $doQuotes = shift(@rawList);
			while ($undefCnt++ < $maxItemCnt) {
				($debug) && print STDERR "Unsetting $undefCnt\n";
				$CONFIG{'maillistdata'}->{$undefCnt} = "";
			}
			foreach $item (@rawList) {
				if ($doQuotes && $inQuote) {
					($debug) && print STDERR "In quote with $item\n";
					$item =~ s/""/"/g;
					if ((($item =~ tr/"//) % 2) && $item =~ s/"$//) {
						$inQuote = 0;
					}
					$CONFIG{"maillistdata"}->{$itemCnt} =
						$CONFIG{"maillistdata"}->{$itemCnt} . ",$item";
					if (!$inQuote) { $itemCnt++; }
				} else {
					($debug) && print STDERR "In no quote with $item\n";
					if ($doQuotes && $item =~ s/^"//) {
						$inQuote = 1;
						$item =~ s/""/"/g;
						if ((($item =~ tr/"//) % 2) && $item =~ s/"$//) {
							$inQuote = 0;
						}
					}
					$CONFIG{"maillistdata"}->{$itemCnt} = $item;
					if (!$inQuote) { $itemCnt++; }
				}
				if ($itemCnt > $maxItemCnt) { $maxItemCnt = $itemCnt; }
			}
			#### Should send mail at this point
			if ($textTemplate) {
				$subedTxt = $textTemplate;
				substOutput(\$subedTxt, '0', 1);
			}
			if ($htmlTemplate) {
				$subedHtml = $htmlTemplate;
				substOutput(\$subedHtml, '0', 1);
			}

			my $thisListSubject = $CONFIG{'listsubject'};
			if ($thisListSubject =~ /^"[^"]*"\s*$/) {
				subReplace(\$thisListSubject);
				$thisListSubject = replacer($thisListSubject, 'listsubject');
			}
			
			if ($CONFIG{'encodesubjects'} && $CONFIG{'charset'} !~ /^us-ascii$/i) {
				my $s = substr(MIME::Lite::encode_base64($thisListSubject), 0, -2);
				$thisListSubject = "=?" . $CONFIG{'charset'} . "?B?" .  $s . "?=";
			}

			my $listMsg = MIME::Lite->build(
							 'From' => $listFrom,
							 'To' => $CONFIG{'maillistdata'}->{1},
							 'Reply-To' => $listReply,
							 'Subject' => $thisListSubject,
							 'Encoding' => $CONFIG{'encoding'},
						);
			$listMsg->add('Precedence' => $CONFIG{listprecedence});
			if ($subedTxt && $subedHtml) {
				$listMsg->attr("content-type" => 'multipart/alternative');
				$listMsg->attr("content-type.boundary" => 'skf349sadjq2uadlkj' . $$);
				$listMsg->attach(Data => $subedTxt);
				my $m = $listMsg->attach(Data => $subedHtml);
				$m->attr("content-type" => "text/html; charset=$CONFIG{charset}");
				$m->attr("content-location" => ($CONFIG{'listbase'} ? 
												$CONFIG{'listbase'} : $base));
			} elsif ($subedHtml) {
				$listMsg->attr("content-type" => "text/html; charset=$CONFIG{charset}");
				$listMsg->attr("content-location" => ($CONFIG{'listbase'} ? 
														$CONFIG{'listbase'} : $base));
				$listMsg->data($subedHtml);
			} else {
				$listMsg->data($subedTxt);
			}
			if ($CONFIG{'maillistdata'}->{1}) {
				if ($CONFIG{'listattachments'}) {
					($debug) && print STDERR "Looking for list attachments\n";
					attachFilesToMail("listattachments", \$listMsg, 1);
				}
				$listMsg->replace('X-Mailer' => "Soupermail $relVersion");
				if ($hasSmtp) {
					$smtpCon[$poolNum]->mail($listFrom);
					$smtpCon[$poolNum]->to($CONFIG{'maillistdata'}->{1});
					$smtpCon[$poolNum]->data();
					$smtpCon[$poolNum]->datasend($listMsg->as_string());
					$smtpCon[$poolNum]->dataend();
					$smtpCon[$poolNum]->reset();
				} else {
					$listMsg->send();
				}
			}
		}
		if ($hasSmtp) {
			for (0 .. $smtpPoolSize) {
				$smtpCon[$_]->quit;
			}
		}
	}
	return 1;
}

END_OF_MAIL_FUNCTIONS

############################################################################
# Subroutine: wrapText ( number_of_characters_to_wrap_to,
#						buffer_to_wrap )
# Takes a buffer, and wraps it to the number of characters specified.
# Returns the wrapped buffer.
############################################################################
sub wrapText {
	($debug) && (print STDERR "wrapText (@_) \@ " . time . "\n");
	my ($wrap, $buffer) = @_;
	my ($start, $rest, $tmp, $something);
	### Need to isolate words longer than the wrap size ...
	$$buffer =~ s/([^\s]{$wrap,})\s/\n$1\n/g;
	### ... and then do real wrapping.
	while ($$buffer =~ /([^\n]{$wrap})/) {
		$start = $`;
		$rest = $';
		$something = $1;
		$something =~ s/((.|\n)*)\s((.|\n)*)/$1\n$3/;
		$something =~ /((.|\n)*)(\n.*)/;
		$tmp .= $start . $1;
		$$buffer = $3 . $rest;
	}
	$$buffer = $tmp . $$buffer;
}

############################################################################
# Subroutine: dehtml ( [unescape], string )
# Change common HTML characters to special charaters optionally url
# unescaping if neccessary. 
############################################################################
sub dehtml { 
	my $arg1 = shift;
	my $arg2 = shift;
	$_ = ($arg1) ? URLunescape($arg2) : $arg2;
	s/\&/\&#38;/g; s/>/\&#62;/g; s/</\&#60;/g;
	s/\"/\&#34;/g; s/\'/\&#39;/g;
	return $_;
}



my $pgpFunctions =<<'END_OF_PGP_FUNCTIONS';

############################################################################
# Subroutine: pgpFail ( failure_message )
# Need a special pgp failure routine to clean up after pgp's done a mess.
############################################################################
sub pgpFail {
	($debug) && (print STDERR "pgpFail (@_) \@ " . time . "\n");
	my ($msg) = shift;
	fatal("PGP Failure:\n\n    $msg");
}

############################################################################
# Subroutine: pgpInit ()
# Using PGP, so check all's well
# This is designed with pgp 5.0i in mind, so i have to take care
# that pgp doesn't generate any unwanted output... ie. give it a
# random number file
# Stop soupermails from clashing by using pid numbers
# If it all goes pear shape, make sure the files are deleted
# by giving total write access. I suppose this is a hole, but a small one
#
# How to encrypt to sender... hmm, they'd have to supply their own
# pgp key... i guess it could be done, but not at the moment.
# Guess i could introduce a text area called PGP for users to put
# their key in, or have the pgp check the Email field
# Perhaps even use netscape's upload button - only if v.adventurous though
############################################################################
sub pgpInit {
	my %exts = ('gpg', 'gpg', 'pgp2', 'pgp', 'pgp5', 'pkr', 'pgp6', 'pkr');
	my $keyring = 'pubring.' . $exts{$CONFIG{'defaultencryption'}};
	my $secring = 'secring.' . $exts{$CONFIG{'defaultencryption'}};

	($debug) && (print STDERR "pgpInit (@_) \@ " . time . "\n");
	fatal("Cannot use PGP encryption with Return to Sender option") 
		if ($CONFIG{'returntosender'});

	if (-f "$configRoot/$keyring") {
		copy("$configRoot/$keyring", "$scratchPad/$keyring") || 
			pgpFail("Can't copy $keyring");
		showFile("${scratchPad}/$keyring");
	}
	if (-f "$configRoot/$secring") {
		copy("$configRoot/$secring", "$scratchPad/$secring") || 
			pgpFail("Can't copy $secring");
		showFile("${scratchPad}/$secring");
	}

	### Create a config and random file for PGP.
	if (!$CONFIG{'gnupg'}) {

		### I don't know how random this is going to be, but there's
		### no HTTP keypress emulator :)
		open(RAND, "> ${scratchPad}/randseed.bin") || 
			pgpFail("can't open randseed.bin for creating");
		my ($i);
		for ($i = 0; $i < 512; $i++) {
			print RAND pack("c", rand(255));
		}
		close(RAND);
		showFile("${scratchPad}/randseed.bin");

		### Make a config file... PGP 5 complains if it doesn't get one.
		my $conf = ($CONFIG{'defaultencryption'} eq 'pgp2') ? 'config.txt' : 'pgp.cfg';

		open (PGPCONF, "> ${scratchPad}/$conf") ||
			pgpFail("can't open $conf for creating");
		if ($OS eq "windows") { 
			$scratchPad =~ s/\/+/\\/g;
			print PGPCONF "PubRing=${scratchPad}\\$keyring\n" 
				if (-f "${scratchPad}/$keyring");
		} else {
			print PGPCONF "PubRing=${scratchPad}/$keyring\n" 
				if (-f "${scratchPad}/$keyring");
		}
		if ($CONFIG{'defaultencryption'} ne 'pgp2') {
			print PGPCONF "NoBatchInvalidKeys=0\n";
			print PGPCONF "HTTPKeyServerHost=$CONFIG{pgpserver}\n"
				if ($CONFIG{'pgpserver'});
			print PGPCONF "HTTPKeyServerPort=$CONFIG{pgpserverport}\n"
				if ($CONFIG{'pgpserverport'});
		}
		print PGPCONF "VERBOSE=0\n";
		close(PGPCONF);
	}
}


############################################################################
# Subroutine: pgpMessage (messageRef, timeString)
# Wrap a message up as a PGP encrypted message
############################################################################
sub pgpMessage {
	my $messageBuffer = shift;
	my $uid = shift;
	my $pgpBuffer = "";
	### want to PGP encode the buffer.
	pgpInit();
	$| = 1;
	my $cmd = "";

	my $outfile = "$scratchPad/eout.txt";
	my $t = ($CONFIG{'pgptextmode'} ? " -t" : "");
	if ($CONFIG{'gnupg'}) {
		$cmd = "$pgpencrypt --homedir $scratchPad --batch " .
			   "--always-trust --quiet --no-secmem-warning $t " .
			   "-ear '${uid}'";
		if ($OS eq "windows") {
			$outfile =~ s/\/+/\\/g;
			$cmd .= " -o \"$outfile\"";
			$cmd =~ s/'/"/g;
		} else {
			$cmd .= " -o $outfile";
		}
		$debug || close(STDERR);
		open (WINGPGIN, "| $cmd");
		print WINGPGIN $$messageBuffer;
		close WINGPGIN;
	} else {
		if ($OS eq "windows") {
			$outfile =~ s/\/+/\\/g;
			$cmd = "\"$pgpencrypt\" $t -a -f -r $uid +batchmode -o $outfile";
		} else {
			if ($CONFIG{'defaultencryption'} eq 'pgp2') {
				$cmd = "PGPPATH=$scratchPad $pgpencrypt $t -fea '${uid}' " .
						" -o $outfile";
			} else {
				$cmd = "PGPPATH=$scratchPad $pgpencrypt $t -a -r '${uid}' " .
						"-f +batchmode=1 -o $outfile";
			}
		}
		$ENV{'PGPPATH'} = $scratchPad;
		chdir($scratchPad);
		open (WINPGPIN, "| $cmd");
		print WINPGPIN $$messageBuffer;
		close WINPGPIN;
	}
	open (WINOUT, "< $outfile");
	while (<WINOUT>) {
		$pgpBuffer .= $_;
	}
	close (WINOUT);
	$debug && print STDERR ($CONFIG{'gnupg'} ? "GPG" : "PGP") . ": $cmd\n" .
				"Generated " . length($pgpBuffer) . " bytes\n";
	$$messageBuffer = $pgpBuffer;
}

END_OF_PGP_FUNCTIONS

############################################################################
# There are a couple of deadlock points in soupermail, mainly due to PGP and
# fileuploads. So, we'll actually fork of a child to do that dangerous stuff
# and kill it if a certain timeout's reached.
############################################################################
if ($forkable && $OS eq "unix" && ($child = fork)) {
	$debug = 0;
	$SIG{CHLD} = sub { cleanScratch(); exit; };
	$SIG{TERM} = sub { kill 9, $child;
						cleanScratch(); exit; };
	$SIG{PIPE} = sub { kill 9, $child;
						cleanScratch(); exit; };
	$| = 1;
	sleep $uploadTimeout;
	kill 9, $child;
	fatal ("Soupermail has timed out");
	exit;
} else {
	### Stop STDERR being output to the screen
	### This is UNIX specific... should check the OS I guess...
	if ($debug) {
		open(STDERR, ">> $debug"); 
	} else {
		open(STDERR, "> /dev/null");
	}

	$| = 1;
	$CONFIG{'ref'} = translateFormat('REF:%rrrrrr%');

	### This is the dangerous child that could hang on the new CGI
	$query = new CGI;

	### Remove leading and trailing spaces.
	nukeValues();

	if ($debug) {
		print STDERR "\n\nrunning on perl $] for $^O\n\n";
		print STDERR "\nsoupermail version $relVersion\n\n";
		while (my($en, $ev) = each %ENV) { print STDERR "$en=$ev\n"; }
		print STDERR "Soupermail variables:\nserverRoot = $serverRoot\n" .
					"privateRoot = $privateRoot\n" .
					"tempDir = $tempDir\n" .
					"fhBug = $fhBug\n" .
					"hasDbi = $hasDbi\nmailhost = $mailhost\nmailprog = $mailprog\n" .
					"ps2pdf = $ps2pdf\nlout = $lout\n" .
					"\nData = " . $query->self_url() . "\n";
	}

	# Set up the MIME::Lite mailer to use the right email method
	if ($mailhost) {
		($debug) && (print STDERR "Setting mail to use $mailhost\n");
		MIME::Lite->send("smtp", $mailhost, Debug=>($debug ? 1 : 0));
	} elsif ($mailprog) {
		($debug) && (print STDERR "Setting mail to use $mailprog\n");
		MIME::Lite->send("sendmail", "$mailprog -t -oi -oem", Debug=>($debug ? 1 : 0));
	}

	# And stop it warning
	if (!$debug) { MIME::Lite->quiet(1); }

	$base = ($query->referer() =~ m!^https!i) ? "https" : "http";
	if ($query->referer() =~ m!^https?://([^/]+)!i) {
		$base .= "://$1";
	} else {
		$base .= "://" . $query->server_name();
	}

	### Try and find out where the configuration file is.
	my $transPath = "";
	$transPath = $query->path_translated() if ($query->path_translated());
	if ($transPath =~ m!${serverRoot}(.*)/([^/]*)! &&
		!$query->param('SoupermailConf')) {
		### $pageRoot is where the actual script is being called from
		$pageRoot = $1;
		$configRoot = $serverRoot . $pageRoot;
		securityFilename($pageRoot);
		### The configuration file
		$config = $transPath;
		$base .= $pageRoot;
	} else {
		### See if the config file's been specified in the form itself
		if ($query->param('SoupermailConf')) {
			unless ($query->param('SoupermailConf') =~ m!^[\~/]!) {
				if ($query->referer() =~ m!^https?://[\w\.\-]+(:\d+)?(/.*)!i) {
					my $urlPath = $2;
					### Remove any anchor or query stuff... won't work
					### for path info though :(
					$urlPath =~ s/(^.*?)[\#\?]/$1/;
					$urlPath =~ m!(.*)/[^/]*!;
					$pageRoot = $1;
					$config = "$serverRoot$pageRoot/" . 
								$query->param('SoupermailConf');
					### Have to possibly compress ../ type directories.
					while ($config =~ s![^/]+/\.\./!!) {}
					fatal ("Config file out of server root") unless
						($config =~ /^$serverRoot/);
					$base .= $pageRoot;
				} else {
					fatal("Cannot determine conf location from referer");
				}
			} elsif ($query->param('SoupermailConf') =~ m!^\~!) {
				### The config file is in the private root
				$query->param('SoupermailConf') =~ m!(.*)/[^/]*!;
				$pageRoot = $1;
				$config = "$privateRoot/" . substr($query->param('SoupermailConf'),1);
				$privateConfig = 1;
			} else {
				### The config file is an absolute path starting with /.
				$query->param('SoupermailConf') =~ m!(.*)/[^/]*!;
				$pageRoot = $1;
				$config = $serverRoot . $query->param('SoupermailConf');
				$base .= $pageRoot;
			}
			securityFilename($config);
			fatal("Unable to find or read the config file - " .
					"read http://soupermail.sourceforge.net/faq.html#configprob")
				 unless (-e $config && -f $config && -r $config);
			### Need to reset pageRoot here because ../s in the relative
			### path may have altered things.
			if ($config =~ m!^($serverRoot|$privateRoot)(.*)/[^/]+!) {
				$pageRoot = $2;
				$configRoot = $1 . $2;
			}
		} else {
			fatal("Unable to determine where the config file is.");
		}
	}
	$base .= "/";
	($debug) && print STDERR "Set configRoot to $configRoot\n";
	my $configFile = "";
	grabFile($config, \$configFile);

	$debug && print STDERR "Reading config $config\n";
	for (split(/\n/, $configFile)) {
		my ($setValue);
		my ($toValue);
		next if (/^\s*\#/);
		next unless (/\S/);
		if (/^\s*([^:\s]*\S+)\s*:\s*(.*[\S])\s*$/) {
			$setValue = $1;
			$toValue = $2;
			unless ($setValue =~ /^(if|unless)/i) {
				fatal ("Too many quote marks in a configuration line:\n\n    $_")
					if (($toValue =~ tr/"/"/) > 2);
			}
		
			### now do some work to do replacement of mailto, replyto,
			### subject, ref and cookie values
			if ($toValue =~ /^"[^"]*"\s*$/ && 
				$setValue =~ /$replaceable/ix) {
				$toValue = replacer($toValue, $setValue);
			}
			setConfig($setValue, $toValue);
		} else {
			fatal("Unrecognised config line:\n\n    '$_'\n");
		}
	}
	$debug && print STDERR "Finished reading config $config\n";

	$pgpencrypt = $pgpSet->{$CONFIG{'defaultencryption'}};
	if ($CONFIG{'defaultencryption'} eq 'gpg') { $CONFIG{'gnupg'} = 1; }

	makeScratch();
	if ($CONFIG{'templated'}) { 
		eval($templateFunctions);
		$debug && print STDERR "Evaluated template functions\n";
	}
	if ($CONFIG{'pgpuserid'} || $CONFIG{'filepgpuserid'}) {
		eval($pgpFunctions);
		$debug && print STDERR "Evaluated PGP functions\n";
	}
	if ($CONFIG{'fileto'}) {
		eval($fileFunctions);
		$debug && print STDERR "Evaluated file functions\n";
	}
	if ($CONFIG{'pdftemplate'} || $CONFIG{'pdfmailtemplate'} ||
		$CONFIG{'pdfsendertemplate'}) {
		eval($pdfFunctions);
		$debug && print STDERR "Evaluated pdf functions\n";
	}
	if ($CONFIG{'mailto'} || $CONFIG{'returntosender'} || 
		$CONFIG{'sendertemplate'} || $CONFIG{'htmlsendertemplate'} ||
		$CONFIG{'pdfsendertemplate'} || $CONFIG{'pdfmailtemplate'} ||
		$CONFIG{'maillist'} || $CONFIG{'listformfield'}) {
		eval($mailFunctions);
		$debug && print STDERR "Evaluated mail functions $@\n";
	}

	### Do a test to see if the GPG key is OK
	if ($CONFIG{'pgpuserid'}) {
		if ($CONFIG{'gnupg'}) {
			fatal("GPG doesn't appear to be available at:\n\n    $pgpencrypt") unless
				(-f $pgpencrypt && -x $pgpencrypt);
			fatal("Cannot find GPG keyring") unless 
				(-f "$configRoot/pubring.gpg");
			fatal("Cannot read GPG keyring") unless 
				(-r "$configRoot/pubring.gpg");
		} else {
			fatal("PGP doesn't appear to be available at:\n\n    $pgpencrypt") unless
				(-f $pgpencrypt && -x $pgpencrypt);
			fatal("Can't find pubring.pkr in:\n\n    ${pageRoot}") unless 
				(-f "$configRoot/pubring.pkr" || 
				 $CONFIG{'pgpserver'});
			fatal("Can't read pubring.pkr in:\n\n    ${pageRoot}") unless 
				(-r "$configRoot/pubring.pkr" || 
				 $CONFIG{'pgpserver'});
		}
	}
	### Check for expiry date
	if ($today > $CONFIG{'expirydate'}) {
		doCounters('expires');
		$CONFIG{"ref"} = translateFormat($CONFIG{"ref"});
		subReplace();
		returnExpired();
		cleanScratch();
		exit;
	}

	### Check for missing required fields
	if (formMissingRequired() || 
		badTypes(\@typeChecks) || 
		$CONFIG{'error'}) {
		$debug && print STDERR "Have failed a required, type or config_error check\n";
		doCounters('failure');
		$CONFIG{"ref"} = translateFormat($CONFIG{"ref"});
		subReplace();
		returnFailure();
		cleanScratch();
		exit;
	}

	### Check for a blank form
	if (formIsBlank()) {
		doCounters('blank');
		$CONFIG{"ref"} = translateFormat($CONFIG{"ref"});
		subReplace();
		returnBlank();
		cleanScratch();
		exit;
	}

	### Looks ok, so return the final page
	doCounters('success');
	$CONFIG{"ref"} = translateFormat($CONFIG{"ref"});
	subReplace();
	if ($CONFIG{'fileto'}) { genFileto(); }
	returnSuccess();
	cleanScratch();
	exit;
}


############################################################################
# Subroutine: URLescape ( string )
# Escape out characters in a string, and return the string. Pinched
# straight out of CGI.pm, but since its not exported explicitly I figure
# its best to copy it here.
############################################################################
sub URLescape {
	($debug) && (print STDERR "URLescape (@_) \@ " . time . "\n");
	my $toencode = shift;
	return undef unless defined($toencode);
	$toencode=~s/([^a-zA-Z0-9_.-])/uc sprintf("%%%02x",ord($1))/eg;
	return $toencode;
}

############################################################################
# Subroutine: subReplace ( [optional_ref_value] ) 
# Replace http_ref and counter values for config options. This needs
# to happen after counters have been processed
############################################################################
sub subReplace {
	($debug) && (print STDERR "subReplace () \@ " . time . "\n");
	my $optVal = shift;
	my $setValue;
	if ($optVal) {
			$$optVal =~ s/\$counter_(\d+)/$CONFIG{'counter'}->{"${1}value"}/gs;
			$$optVal =~ s/\$http_ref/$CONFIG{'ref'}/gs;
	} else {
		foreach $setValue (keys %needToReplace) {
			my $val = $CONFIG{$setValue};
			($debug) && (print STDERR "val is $val\n");
			$val =~ s/\$counter_(\d+)/$CONFIG{'counter'}->{"${1}value"}/gs;
			$val =~ s/\$http_ref/$CONFIG{'ref'}/gs;
			($debug) && (print STDERR "processing $setValue to $val\n");
			$CONFIG{$setValue} = $val;
		}
	}
}

############################################################################
# Subroutine: makeUrl ( url )
# For convenience sake, this will try and figure out if a given URL is 
# absolute or relative. If its relative, it'll try and fill in the
# blanks to make it an absolute URL for the current server. 
# Returns the absolute URL.
############################################################################
sub makeUrl {
	($debug) && (print STDERR "makeUrl (@_) \@ " . time . "\n");
	$_ = shift;
	my ($server, $url);
	$server = $query->server_name() unless ($server = $ENV{'HTTP_HOST'});
	if ($query->server_port() != 80 && ! $server =~ /:\d+$/) {
		$server .= ":" . $query->server_port();
	}
	my $proto = "http" . ($ENV{'HTTPS'} =~ /on/i ? "s" : "");
	SWITCH: {
		if (/^\//) { $url = "${proto}://${server}$_"; last SWITCH; }
		if (m!^https?://!i) { $url = $_; last SWITCH; }
		$url = "${pageRoot}/$_";
		while ($url =~ s![^/]+/\.\./!!) {}
		$url = "${proto}://${server}$url";
	}
	return($url);
}


############################################################################
# Subroutine: makePath ( path )
# Makes a path from the server root from the specified path. If the path is
# absolute (ie. starts with a /, its assumed to be from the server root,
# otherwise its assumed to be relative to the configuration file.)
############################################################################
sub makePath {
	($debug) && (print STDERR "makePath (@_) \@ " . time . "\n");
	my $path = shift;
	my $oPath = $path;
	if ($path =~ /^\~/) {
		$path = "${privateRoot}/" . substr($path,1); 
		fatal("Calling private information from a non-private config file")
			unless ($privateConfig);
	} elsif ($path =~ /^\//) {
		$path = $serverRoot . $path; 
	} else {
		$path = "$configRoot/" . $path; 
	}
	while ($path =~ s![^/]+/\.\./!!) {}
	$path =~ s!/+!/!g;
	securityFilename($path);
	($path =~ /^$serverRoot\//) && (return $path);
	($path =~ /^$privateRoot\//) && (return $path);
	fatal("The path $oPath requested is outside the server root");
}


############################################################################
# Subroutine: setConfig ( configuration_line )
# This routine takes a configuration variable name and a value and attempts
# to set the variable to the value. It does a fair bit of error and
# security checking depending on the type of variable to set.
############################################################################
sub setConfig {
	($debug) && (print STDERR "setConfig (@_) \@ " . time . "\n");
	$_ = shift; 
	my ($value) = shift;
	$_ = lc($_);
	CONFSWITCH : {

	### Required form fields that must be filled in before success.
	### Ignored fields can be used to hide hidden fields from the blank
	### form checking routine.
	if (/^(required|ignore)$/) {
		securityName($value, 1);
		my ($list) = ($1 eq "required" ? \@required : \@ignored);
		push(@$list, $value);
		last CONFSWITCH;
	}

	### Localised error string
	if (/^error$/) {
		$CONFIG{"error"} = $value;
		last CONFSWITCH;
	}

	### Type checking fields
	if (/^is(not)?(number|integer|email|creditcard)$/) {
		push(@typeChecks, [$_, $value]);
		last CONFSWITCH;
	}
	
	### This is a subject line for generated email... truncated at 199
	### characters to stop DoS attacks against crappy mail clients.
	if (/^(sender|list)?subject$/) {
		if (length($value) > 199) {
			$value = pack("a199", $value);
		}
		$CONFIG{$&} = $value;
		last CONFSWITCH;
	} 

	### A format for the autogenerated reference field.
	### See translateFormat() for more on how it works.
	if (/^ref/) {
		$CONFIG{'ref'} = $value;
		last CONFSWITCH;
	}

	### For the base URLs for HTML email
	if (/^((list|sender|mail)base)$/) {
		$CONFIG{$1} = $value;
		last CONFSWITCH;
	}
	
	### The log on details for DBI support 
	if (/^(sql(user|password))$/) {
		$CONFIG{$1} = $value;
		last CONFSWITCH;
	}

	### The database connection string
	if (/^sqlname$/) {
		unless ($value =~ /^dbi:[^:]+(:.*)?/i) { 
			fatal("Malformed database name:\n\n    $value"); }
		$CONFIG{'sqlname'} = $value;
		last CONFSWITCH;
	}

	### Variables to pass into database queries must be passed as
	### bind values for safety.
	if (/^sqlbind(\d+)$/) {
		if ($1 > 0) {
			my $pos = $1 - 1;
			my $val = replacer($value, $_);
			if ($val eq "") { $val = undef; }
			if (defined $val) { $bindVals[$pos] = $val; }
		}
		last CONFSWITCH;
	}

	### A database query is provided in DBI bind format for safety, as this
	### does all the database escaping. We need DBI and the connection name
	### of the database
	if (/^sqlrun(\d+)|listsql$/ && $hasDbi && $CONFIG{'sqlname'}) {
		if (formMissingRequired() || badTypes(\@typeChecks) ||
			$CONFIG{'error'}) {
			($debug) && print STDERR "Skipping SQL $value due to requires/types.\n";
			@bindVals = ();
			last CONFSWITCH;
		}
		my $sqlNum = $1 || 'listsql';
		($debug) && print STDERR "Trying database " . $CONFIG{'sqlname'} . "\n";
		my $dbh = DBI->connect($CONFIG{'sqlname'}, 
								$CONFIG{'sqluser'}, 
								$CONFIG{'sqlpassword'}) || last CONFSWITCH;
		($debug) && print STDERR "Connected to database\n";
		my $sth = $dbh->prepare($value);
		if ($sth) {
			my $rv;
			eval('$rv = $sth->execute(@bindVals);');
			if (!$@) {
				my @sqlVals = $sth->fetchrow_array;
				my $loop = 0;
				if ($sqlNum eq 'listsql') {
					push (@listSql, [ 0, @sqlVals ]);
				} else {
					while (scalar(@sqlVals)) {
						for (0 .. $#sqlVals) {
							$sqlVals{"sql_${sqlNum}_" . ($loop + 1) . "_" .
									($_ + 1)} = $sqlVals[$_];
						}
						$loop++;
						@sqlVals = $sth->fetchrow_array;
					}
					$sqlCount{$sqlNum} = $loop;
				}
			} else {
				($debug) && print STDERR "Unable to execute with " . 
					join(",", @bindVals) . $dbh->errstr . ", $@\n";
			}
		} else {
			($debug) && print STDERR "Unable to prepare statement '$value' " . 
				$dbh->errstr;
		}
		$dbh->disconnect();
		@bindVals = ();
		last CONFSWITCH;
	}

	### A filename to save the form results into. It should be specified
	### relative to where the configuration file was placed.
	if (/^fileto/) {
		$CONFIG{'fileto'} = $value;
		last CONFSWITCH;
	}

	### This is a filename for a counter. The numbers in the middle are
	### used to specify which counter we're talking about.
	if (/^counter(\d+)file/) {
		my $countNum = $1;
		my $counterFile = makePath($value);
		$counterFile =~ m!^(.*)/[^/]*$!;
		fatal ("Can not write to counter file of:\n\n    $value") 
			if ((-e $counterFile && ! -w $counterFile) ||
				(-e $counterFile && -l $counterFile) ||
				(! -e $counterFile && ! -w $1));
		my $counterValue = "0";
		grabFile($counterFile, \$counterValue) if (-f $counterFile);
		$counterValue =~ /^(\d+)/;
		$CONFIG{"counter"}->{"${countNum}value"} = $1;
		$CONFIG{"counter"}->{"${countNum}file"} = $counterFile;
		if (!$CONFIG{"counter"}->{"${countNum}step"}) {
			$CONFIG{"counter"}->{"${countNum}step"} = 1;
		}
		last CONFSWITCH;
	}

	### Set the counter to an absolute value.
	if (/^setcounter(\d+)/) {
		my $countNum = $1;
		fatal("Counter values must be numeric for:\n\n    $_") if 
			($value =~ /[^\d]/);
		$CONFIG{"counter"}->{"${countNum}set"} = $value;
		last CONFSWITCH;
	}

	### Set the counter step value.
	if (/^counter(\d+)step/) {
		my $countNum = $1;
		fatal("Counter step values must be numeric for:\n\n    $_") if 
			($value =~ /[^\d]/);
		$CONFIG{"counter"}->{"${countNum}step"} = $value;
		last CONFSWITCH;
	}

	### Get the form field name that contains mailing list data
	if (/^listformfield$/) {
		securityName($value, 1);
		$CONFIG{"listformfield"} = $value;
		last CONFSWITCH;
	}

	### Counters can change depending on the four different outcomes of
	### a form's submission.
	if (/^counter(\d+)on(failure|success|expires|blank)$/) {
		my $countNum = $1;
		my $mode = $2;
		last CONFSWITCH unless ($value =~ /^(yes|no|1|0)$/i);
		$CONFIG{'counter'}->{"${countNum}on$mode"} = 
			($value =~ /^(yes|1)$/i) ? 1 : 0;
		last CONFSWITCH;
	}

	### Attachments are sent with sendertemplate data and there can be
	### any number of them.
	if (/^(list)?attachment(\d+)$/) {
		my $atype = ($1 ? "listattachments" : "attachments");
		my $attachNum = $2;
		if ($value ne '""') {
			my $attachFile = makePath($value);
			unless (-f $attachFile && -r $attachFile) {
				fatal("Cannot read file attachment:\n\n    $attachNum");
			}
			($debug) && print STDERR "Config attaching $attachFile\n";
			$CONFIG{$atype}->{"${attachNum}file"} = $attachFile;
			$attachCount++;
		} else {
			delete $CONFIG{$atype}->{"${attachNum}file"};
			delete $CONFIG{$atype}->{"${attachNum}mime"};
			$attachCount--;
		}
	}

	### Attachments need to have a mime type associated with them
	if (/^(list)?attachment(\d+)(mime)/) {
		my $atype = ($1 ? "listattachments" : "attachments");
		my $attachNum = $2;
		my $attachType = $3;
		fatal("Unrecognised $atype MIME format:\n\n    $value") unless
			($attachType ne "mime" || 
				$value =~ m!^${eToken}+/${eToken}+(\s*;\s*${eToken}+\s*(=\s*${eToken}+)?)*$!);
		$CONFIG{$atype}->{"${attachNum}$attachType"} = $value;
		last CONFSWITCH;
	}

	### Templates returned to the browser can have their mime types	
	### set here.
	if (/^(success|blank|expires|failure)mime$/) {
		my $n = $&;
		fatal("Unrecognised return MIME format:\n\n    $value") unless
			($value =~ m!^${eToken}+/${eToken}+(\s*;\s*${eToken}+\s*(=\s*${eToken}+)?)*$!);
		$CONFIG{$n} = $value;
		last CONFSWITCH;
	}

	### This specifies the maximum number of bytes a soupermail generated
	### file can grow to. If a new addition will take the file over this
	### size, the file is initially deleted. The backup name (if any)
	### for the deleted file is specified with filebackupformat.
	if (/^filemaxbytes/) {
		fatal("filemaxbytes must be a number")	if ($value =~ /[^\d]/);
		$CONFIG{'filemaxbytes'} = $value;
		last CONFSWITCH;
	}

	### This is the format for any backup of a soupermail generated file
	### which is deleted due to the filemaxbytes setting. It takes the
	### same formatting values as a reference number format.
	if (/^filebackupformat/) {
		$value = translateFormat($value);
		my $tmpFile = makePath($value);
		if (-e $tmpFile && !-w $tmpFile) {
			fatal("No permissions for writing to filebackupformat");
		}
		if (-e $tmpFile && -l $tmpFile) {
			fatal("The filebackupformat file is a symlink");
		}
		### Check to see if we've got write access to the backup
		### directory.
		unless (-e $tmpFile) {
			$tmpFile =~ m!(.*/)[^/]*!;
			fatal ("Cannot write into the backup directory") unless (-w $1);
		}
		$CONFIG{'filebackupformat'} = $tmpFile;
		last CONFSWITCH;
	}

	### email address(es) to send the form's mail to.
	### checkEmail() does a little security check to make sure emails
	### look right.
	if (/^(sender|list)?replyto|mailto|(sender|list)from|(sender)?bcc/) {
		checkEmail($value);
		$CONFIG{$&} = $value;
		last CONFSWITCH;
	} 

	### Set up some template files. All these are assumed to be relative
	### to the location of the configuration file.
	if (/^(headings|footings|success|failure|blank|
		   (expires|file|pdf)template|
		   (html|pdf)?mailtemplate|(html|pdf)?sendertemplate)|
		   (html)?listtemplate$/x) {
		my $cf = $&;
		if (!$CONFIG{'templated'}) {
			$CONFIG{'templated'} = (/success|failure|blank|template/);
		}
		$CONFIG{$cf} = makePath($value);
		fatal("Cannot find the '$cf' template file") unless 
			(-f $CONFIG{$cf} && -r $CONFIG{$cf});
		last CONFSWITCH;
	}

	### Get the mailing list - or at least make sure it exists
	if (/^maillist$/) {
		my $list = $&;
		$CONFIG{$list} = makePath($value);
		fatal("Cannot find the maillist file:\n\n    $list") unless 
			(-f $CONFIG{$list} && -r $CONFIG{$list});
		last CONFSWITCH;
	}

	### If the sender of the email wants to get a confirmation copy of
	### soupermail generated email, setting this to 'yes' or 1 will do
	### so by putting the sender in the CC email header.
	if (/^returntosender/) {
		last CONFSWITCH unless ($value =~ /^(yes|no|1|0)$/i);
		$CONFIG{'returntosender'} = ($value =~ /^(yes|1)$/i) ? 1 : 0;
		last CONFSWITCH;
	}

	### Without a template, sort form fields in the return email
	### alphabetically.	
	if (/^alphasort/) {
		last CONFSWITCH unless ($value =~ /^(yes|no|1|0)$/i);
		$CONFIG{'alphasort'} = ($value =~ /^(yes|1)$/i) ? 1 : 0;
		last CONFSWITCH;
	}

	### Subject lines in emails are sent 7bit, this means non-ascii
	### characters get munged. Setting encodesubjects to yes means they
	### get base64 encoded as per RFC 2047.
	if (/^encodesubjects$/) {
		last CONFSWITCH unless ($value =~ /^(yes|no|1|0)$/i);
		$CONFIG{'encodesubjects'} = ($value =~ /^(yes|1)$/i) ? 1 : 0;
		last CONFSWITCH;
	}


	### To prevent mail loops, emails sent with the maillist functions
	### will be given a precedence of list.
	if (/^listprecedence/) {
		last CONFSWITCH unless ($value =~ /^(junk|list|bulk)$/i);
		$CONFIG{'listprecedence'} = $value;
		last CONFSWITCH;
	}

	### This field takes a date, and will cause the form to stop
	### accepting submissions ON or AFTER that date.
	if (/^expires/) {
		fatal ("Invalid expiry format:\n\n    $value") unless 
			($value =~ /^(\d\d?)-(\d\d?)-(\d\d(\d\d)?)$/);
		if ($1 > 31 ||  $2 > 12 || $1 < 1 || $2 < 1) {
			fatal ("Invalid Expiry date:\n\n    $1 - $2 - $3");
		} elsif ($3 > 2037) {
			### Hey, this even looks for the dreaded 32bit running out
			### of bits bug!
			fatal("Expiry date must be before the year 2038");
		}
		$CONFIG{'expirydate'} = timelocal(0,0,0,$1,($2 - 1), $3);
		last CONFSWITCH;
	}

	### This species how many characters to wrap emails to.
	if (/^wrap/) {
		$value =~ s/\D//g;
		$CONFIG{'wrap'} = $value;
		last CONFSWITCH;
	}

	### This is the username or KeyID of a user in the pubring.pkr
	### PGP public keyring placed in the directory where the config file
	### is. Using KeyIDs is better, as they are unique (I think).
	if (/^(file)?pgpuserid/) {
		fatal("Illegal characters in the PGP userid:\n\n    $value") if
			($value =~ /[^\w \<\>\@\.\-]/);
		$CONFIG{$_} = $value;
		last CONFSWITCH;
	}

	### PGP 5 can look for stuff off an internet PGP key server, this
	### way, you should be able to use pgp userids that are on a remote
	### server, rather than in your public keyring.
	if (/^pgpserver/) {
		unless ($value =~ /^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})|
							(([\w\-]+\.)*[\w\-]+)$/x) {
			fatal("The PGP keyserver name must be a hostname or an" .
				  " IP address");
		}
		$CONFIG{'pgpserver'} = $value;
		last CONFSWITCH;
	}

	### This defines the post the PGP key server's running on.
	if (/^pgpport/) {
		unless ($value =~ /^\d+$/) {
			fatal("The PGP keyserver port must be an integer");
		}
		$CONFIG{'pgpserverport'} = $value;
		last CONFSWITCH;
	}

	### These are the flags to say whether or not to use GNU Privacy
	### Guard rather than PGP 5 an whether to use PGP/MIME packaging of
	### the email.
	if (/gnupg|pgpmime|pgpuploads|pgppdfs|pgptextmode/) {
		my $confVal = $&;
		last CONFSWITCH unless ($value =~ /^(yes|no|1|0)$/i);
		$CONFIG{$confVal} = ($value =~ /^(yes|1)$/i) ? 1 : 0;
		last CONFSWITCH;
	}

	### Allow a user selectable version of pgp/gpg
	if (/pgpversion/) {
		my $confVal = $&;
		last CONFSWITCH unless ($pgpSet->{$value});
		$CONFIG{'defaultencryption'} = $value;
		($debug) && print STDERR "Default encryption method set to $value\n";
		last CONFSWITCH;
	}

	if (/7bit/) {
		my $confVal = $&;
		last CONFSWITCH unless ($value =~ /^(yes|no|1|0)$/i);
		$CONFIG{'encoding'} = ($value =~ /^(yes|1)$/i) ? "quoted-printable" : 
														 "8BIT";
		last CONFSWITCH;
	}

	### The defines the character set to set as the email character set
	if (/mailcharset/) {
		if ($value =~ /[^\w\-]/) {
			fatal("The mail character set must only contain letters, numbers " .
				  "and hyphens");
		}
		$CONFIG{'charset'} = $value;
		last CONFSWITCH;
	}

	### This sets up an if conditional value.
	if (/^if|(unless)/) {
		my $conditionType = $1 ? 1 : 0;
		fatal("Conditional $value with wrong format") unless 
			($value =~ /.*\s+then\s+[^:\s]+\s*:\s*.*[\S]\s*/i);
		parseCondition($value, $conditionType);
		last CONFSWITCH;
	}

	### Rather than using a templates, these goto... values goto a
	### specific URL.
	if (/^(goto(success|failure|expires|blank))$/) {
		$CONFIG{$1} = makeUrl($value);
		last CONFSWITCH;
	}

	### Set some boolean flags up.
	### By default, soupermail pops a 4 line summary about the form that
	### started it at the end of the email it sends out. nomailfooter
	### stops that behaviour.
	### By default, any files written by soupermail are made unreadable
	### to the webserver. If you want, setting filereadable stops this
	### behaviour.
	### Setting nofilecr will remove newline characters from anything
	### written into a soupermail generated file.
	### Setting fileattop will place new entries into a soupermail
	### generated file right at the top, or, if a headings has been	
	### specified, straight after the headings.
	### Setting mimeon allows MIME form uploads. The generated emails
	### will have MIME based attachments for anything uploaded.
	### Setting cgiwrappers alters the chmod behaviour when hiding files
	if (/^nomailfooter|filereadable|nofilecr|fileattop|mimeon|
		  cgiwrappers/x) {
		my $confVal = $&;
		last CONFSWITCH unless ($value =~ /^(yes|no|1|0)$/i);
		$CONFIG{$confVal} = ($value =~ /^(yes|1)$/i) ? 1 : 0;
		last CONFSWITCH;
	}

	### This will set or generate a cookie.
	### Defaults for a new cookie are:
	###	 name	- cookie1, cookie2 up to cookie9
	###	 value   - ""
	###	 path	- path to the soupermail CGI
	###	 domain  - the current server's name
	###	 expires - in 24 hours
	###	 secure  - sent over SSL and non-SSL connections
	if (/^${cookieStr}(name|value|path|domain|secure|expires)/) {
		my $item  = $1 - 1;
		my $cset  = $2;
		my $cname = "cookie$1";
		my $cval  = "";
		my $csec  = 0;
		my $cexpires = '+1d';
		my $cdomain = ($query->virtual_host() ? $query->virtual_host() :
												$query->server_name());
		my $cpath = $query->script_name();
		if ($cset eq "name") {
			$cname = $value;
			if ($cname =~ /[^\w\-]/) {
				fatal("Cookie names can only contain letters and numbers");
			}
			if (length($cname) > 50) { 
				fatal("Cookie names must be less than 50 characters long.");
			}
		} elsif ($cset eq "value") {
			if (length($value) > 516) {
				$value = substr($value, 516);
			}
			$cval = $value;
		} elsif ($cset eq "path") {
			fatal("Invalid cookie path:\n\n    $value") if ($value =~ /[^\w\.\/\%\-]/);
			$cpath = $value;
		} elsif ($cset eq "domain") {
			fatal("Invalid cookie domain:\n\n    $value") 
				unless ($value =~ /^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})|
									(([\w\-]+\.)*[\w\-]+)(:\d+)?$/x);
			$cdomain = $value;
		} elsif ($cset eq "secure") {
			$csec = $value = ($value =~ /yes|1/i) ? 1 : 0;
		} elsif ($cset eq "expires") {
			unless ($value =~ /^(\+\d+[smhdMy]|
								\-\d+[smhdMy]|
								[nN][oO][wW]|
								\d\d?-\d\d?-\d\d(\d\d)?|
								\d\d?-\d\d?-\d\d(\d\d)?\s+\d\d?:\d\d?(:\d\d?)?|
								\d\d?:\d\d?(:\d\d?)?)$/x) {
				fatal("Incorrect cookie expires format:\n\n    $value");
			}
			my (@hasDate) = ();
			my (@hasTime) = ();

			### Now check the date format.
			if ($value =~ /\b(\d\d?)-(\d\d?)-(\d\d(\d\d)?)\b/) {
				if ($1 > 31 ||  $2 > 12 || $1 < 1 || $2 < 1) {
					fatal ("Invalid Expiry date:\n\n    $1 - $2 - $3");
				} elsif ($3 > 2037) {
					fatal("Cookie expiry date must be before the year 2038");
				}
				$hasDate[0] = $1;
				$hasDate[1] = $2;
				$hasDate[2] = $3;
			}

			### And check the time format.
			if ($value =~ /\b(\d\d?):(\d\d?)(:(\d\d?))?\b/) {
				if ($1 > 23 || $2 > 59 || ($4 && $4 > 59)) {
					fatal("Invalid cookie expiry time:\n\n    ${1}:$2$3");
				}
				$hasTime[0] = $1;
				$hasTime[1] = $2;
				$hasTime[2] = $4;
			}

			### Now set up the time/date stuff.
			if (@hasDate || @hasTime) {
				if (@hasDate && @hasTime) {
					$value = localtime(timelocal($hasTime[2],
										$hasTime[1],
										$hasTime[0],
										$hasDate[0],
										$hasDate[1] - 1,
										$hasDate[2]));
				} elsif (@hasDate) {
					$value = localtime(timelocal(0, 0, 0,
										$hasDate[0],
										$hasDate[1] - 1,
										$hasDate[2]));
				} else {
					my @now = localtime(time);
					$value = localtime(timelocal($hasTime[2],
										$hasTime[1],
										$hasTime[0],
										$now[3],
										$now[4],
										$now[5]));
				}
			}
			$cexpires = $value;
		}
		if ($cookieList[$item]) {
			### That cookie already exists, so we'll have to change	
			### stuff.
			$cookieList[$item]->{$cset} = $value;
		} else {
			### Its a new cookie, hhhmmmmmm, coookies :)
			$cookieList[$item] = {'name'=>$cname, 'value'=>$cval,
								  'domain'=>$cdomain, 'path'=>$cpath,
								  'secure'=>$csec, 'expires'=>$cexpires};
		}
		last CONFSWITCH;
	}

	### This controls when cookies will be sent out.
	if (/^cookieon(failure|success|blank|expires)$/) {
		my $cfgval = $1 . "cookie";
		last CONFSWITCH unless ($value =~ /^(yes|no|1|0)$/i);
		$CONFIG{$cfgval} = ($value =~ /^(yes|1)$/i) ? 1 : 0;
		last CONFSWITCH;
	}

	} ### End of CONFSWITCH
}


############################################################################
# Subroutine: parseCondition ( condition, if_or_unless )
# This will go through a conditional configuration statement
# It'll see if the condition is true, and if so set the specified 
# config value.
############################################################################
sub parseCondition {
	($debug) && (print STDERR "parseCondition (@_) \@ " . time . "\n");
	$_ = shift;
	my $cType = shift;
	my ($opens, $closes, $set, $cond, $toValue);
	my ($tmp) = "";

	($debug) && print STDERR "Got cond $_\n";
	### Initially break up the conditions.
	/^((?:[^\:]*(?:'[^']*'|"[^"]*")[^\:]*)|[^\:]*[^\s:])\s+
		  then\s+([^:]*[^\s:])\s*:\s*(.*[\S])\s*/ix;
	$cond = $1;
	$set = $2;
	$toValue = $3;

	$debug && print STDERR "[$cond] [$set] [$toValue]\n";
	### Perform some validation checks on the statement.
	fatal ("Don't use nested conditionals in:\n\n    $_") 
		if ($set =~ /(if|unless)/i);
	$opens = tr/(/(/;
	$closes = tr/)/)/;
	fatal("Mismatched parentheses in:\n\n    $cond") 
		if ($opens != $closes);
	$tmp = $cond;
	$tmp =~ s/\&\&|\|\|//g;
	failSecurity("<B>$cond </B>contains unamtched &#124;s and &amp;s") 
		if ($tmp =~ /&|\|/);
	fatal ("Too many quote marks in a configuration line:\n\n    $_")
		if (($toValue =~ tr/"/"/) > 2);

	### Some values can contain other config and form values, but
	### NOT ALL. Why? Paranoid security and I really can't see a use
	### for changing the others.
	if ($toValue =~ /^"[^"]*"\s*$/ &&
		$set =~ /$replaceable/ix) {
		$toValue = replacer($toValue, $set);
	}

	$cond = evalCond($cond);
	if ($cType) {
		setConfig($set, $toValue) unless ($cond);
	} else {
		setConfig($set, $toValue) if ($cond);
	}
}


############################################################################
# Subroutine: evalCond ( condition )
# Return true or false based on whether the condition evaluates
############################################################################
sub evalCond {
	my $cond = shift;
	### The not operator needs a bit of pre-tweaking for easy matching.
	$cond =~ s/!([^=])/! $1/g;
	### Now break into smaller parts and security check.
	my @conBits = split (/\(\s*|\)\s*|\&\&\s*|\|\|\s*|\!\s+/, $cond);

	my $ops = "\\s+has(?:nt)?\\s+|\\s*[=!]=\\s*|\\s+eq\\s+|" .
			  "\\s+ne\\s+|\\s*[<>]=?\\s*|\\s+[gl]t\\s+|" .
			  "\\s+[gl]e\\s+|\\s+contains\\s+|\\s+(?:longer|shorter)than\\s+";

	### Each part should be of the form:
	### field op token	  OR	  field	
	### where field is a field name from the form, op is a boolean
	### operator and token is some alphanumeric.
	while (scalar(@conBits)) {
		### Have to put the scalar in to cope with null list values.
		my $part = shift(@conBits);
		next unless ($part =~ /\S/);
		my ($field, $op, $val, $result);
		$_ = $part;
		$debug && print STDERR "Looking at condition $_ \n";
			
		if (/^("[^"]+"|'[^']+'|[\S]+)($ops)
			("[^"]+"|'[^']+'|[\S]+)\s*$/x) {
	
			### Dealing with a boolean expression.
			$result = '0';
			$field = $1;
			$op = lc($2);
			$val = $3;
			$op =~ s/\s//g;
			$field =~ s/^"([^"]+)"/$1/ unless ($field =~ s/^'([^']+)'/$1/);
			$val =~ s/^"([^"]+)"/$1/ unless ($val =~ s/^'([^']+)'/$1/);
			securityName($field) unless 
				($field =~ /^\$((http|cookie)_[\w\-]+|
								(maillist|counter)_\d+|sql_\d+_\d+_\d+)/xi);;
			$debug && print STDERR "field = $field; op = $op; val = $val \n";

			### Now see if field is something out of the form.
			if ($op =~ /^has/) {
				$debug && print STDERR "parsing has condition $op \n";
				if ($field =~ /^\$cookie_([\w\-]+)/) {
					$result = '1' if ($query->cookie($1) eq $val);
				} elsif ($field =~ /^\$(http_[\w\-]+)/i) {
					$result = '1' if (getHttpValue($1) eq $val);
				} elsif ($field =~ /^\$counter_(\d+)/i) {
					$result = '1' if 
						($CONFIG{'counter'}->{"${1}value"} eq $val);
				} elsif ($field =~ /^\$maillist_(\d+)$/) {
					$result = 1 if 
						($CONFIG{"maillistdata"} && 
							$CONFIG{"maillistdata"}->{$1} eq $val);
				} elsif ($field =~ /^\$(sql_\d+_\d+_\d+)$/i) {
					$result = '1' if ($sqlVals{$1} eq $val);
				} else {
					foreach ($query->param($field)) {
						($debug) && print STDERR "Checking $_ against $val\n";
						$result = '1',last if ($_ eq $val);
					}
				}
				$result = !$result if ($op =~ /nt/);
			} elsif ($op =~ /^(longer|shorter)than/) {
				$debug && print STDERR "parsing longer/shorter condition $op \n";
				my $subOp = $1;
				my $str = undef;
				if ($field =~ /^\$cookie_([\w\-]+)/) {
					$str = $query->cookie($1) || "";
				} elsif ($field =~ /^\$(http_[\w\-]+)/i) {
					$str = getHttpValue($1) || "";
				} elsif ($field =~ /^\$counter_(\d+)/i) {
					$str = $CONFIG{'counter'}->{"${1}value"} || "";
				} elsif ($field =~ /^\$maillist_(\d+)$/) {
					$str = $CONFIG{"maillistdata"}->{$1} || "";
				} elsif ($field =~ /^\$(sql_\d+_\d+_\d+)$/i) {
					$str = $sqlVals{$1} || "";
				}
				if (defined($str)) {
					($debug) && print STDERR "Checking $str against $val\n";
					if ($subOp eq 'longer') {
						$result = '1' if (length($str) > $val);
					} else {
						$result = '1' if (length($str) < $val);
					}
				} else {
					foreach ($query->param($field)) {
						($debug) && print STDERR "Checking $_ against $val\n";
						if ($subOp eq 'longer') {
							$result = '1' if (length() > $val);
						} else {
							$result = '1' if (length() < $val);
						}
					}
				}
			} elsif ($op =~ /^contains/) {
				### Escape out potential regexp characters
				$val = "\Q$val\E";
				if ($field =~ /^\$cookie_([\w\-]+)/i) {
					$field = $query->cookie($1);
					$result = ($field =~ /$val/i);
				} elsif ($field =~ /^\$(http_[\w\-]+)/i) {
					$field = getHttpValue($1);
					$result = ($field =~ /$val/i);
				} elsif ($field =~ /^\$counter_(\d+)/i) {
					$result = 
						($CONFIG{'counter'}->{"${1}value"} =~ /$val/i);
				} elsif ($field =~ /^\$maillist_(\d+)$/) {
					$result = 1 if 
						($CONFIG{"maillistdata"}->{$1} =~ /$val/i);
				} elsif ($field =~ /^\$(sql_\d+_\d+_\d+)$/i) {
					$result = '1' if ($sqlVals{$1} =~ /$val/);
				} else {
					foreach ($query->param($field)) {
						$result = '1',last if (/$val/i);
					}
				}
			} else {
				if ($field =~ /^\$cookie_([\w\-]+)/i) {
					$field = $query->cookie($1);
				} elsif ($field =~ /^\$(http_[\w\-]+)/i) {
					$field = getHttpValue($1);
				} elsif ($field =~ /^\$counter_(\d+)/i) {
					$field = $CONFIG{'counter'}->{"${1}value"};
				} elsif ($field =~ /^\$(sql_\d+_\d+_\d+)$/i) {
					$result = '1' if ($sqlVals{$1} eq $val);
				} elsif ($field =~ /^\$maillist_(\d+)$/) {
					$result = '1' if 
						($CONFIG{"maillistdata"} && $CONFIG{"maillistdata"}->{$1} eq $val);
				} else {
					$field = $query->param($field);
				}
				### Single quote strings to stop them being 'eval'ed
				$field = "\"\Q${field}\E\"" unless ($field =~ /^\d+$/);
				$val = "\"\Q$val\E\"" unless ($val =~ /^\d+$/);
				($debug) && print STDERR "Evaling $field $op $val\n";
				$result = eval "$field $op $val";
			}
		} elsif (/^\s*("[^"]+"|'[^']+'|\S+)\s*$/) {
			### Does the field exist?
			$field = $1;
			$field =~ s/^"([^"]+)"/$1/ unless 
				($field =~ s/^'([^']+)'/$1/);
			if ($field =~ /^\$cookie_([\w\-]+)/i) {
				$result = defined $query->cookie($1) ? 1 : 0;
			} elsif ($field =~ /^\$(http_[\w\-]+)/) {
				$result = (getHttpValue($1) != "") ? 1 : 0;
			} elsif ($field =~ /^\$counter_(\d+)/i) {
				$result = ($CONFIG{'counter'}->{"${1}value"}) ? 1 : 0;
			} elsif ($field =~ /^\$maillist_(\d+)$/) {
				$result = 
					($CONFIG{"maillistdata"} && $CONFIG{"maillistdata"}->{$1}) ? 1 : 0;
			} elsif ($field =~ /^\$(sql_\d+_\d+_\d+)$/i) {
				$result = ($sqlVals{$1} || $sqlVals{$1} eq '0') ? 1 : 0;
			} else {
				securityName($field);
				$result = (defined $query->param($field)) ? 1 : 0;
			}
		} else {
			fatal("Bad conditional:\n\n    $_");
		}

		$result = '0' if ($result != 1);
		$cond =~ s/\Q$part\E/$result /;
	}

	($debug) && print STDERR "Should eval condition $cond\n";
	eval {$cond = eval "$cond"};
	return $cond;
}


############################################################################
# Subroutine: replacer ( string_containing_things_to_replace )
# The aim here is to do robust replacement of values from the user's form
# (anything that starts with '$form_') most of the http_ variables that
# can be used in output tags (things starting '$http_'), cookie values
# (anything starting with '$cookie_') and some
# special ones like $subject, $sendersubject, $replyto, $mailto...
# All the replacement values must appear in a double quoted string.
############################################################################
sub replacer {
	($debug) && (print STDERR "replacer (@_) \@ " . time . "\n");
	my $toValue  = shift;
	my $setValue  = shift;
	$toValue	 =~ s/^"(.*)"\s*$/$1/;
	my $escaped = ($setValue =~ /^goto/i ? 1 : 0);
	my $tmpString = "";
	my @chunks = split(/((?:(?:\$form|\$http|\$cookie)_[\w\-]+)|
						(?:(?:\$\{form|\$\{http|\$\{cookie)_[\w\-]+?\})|
						\$sql_\d+_\d+_\d+|\${sql_\d+_\d+_\d+}|
						\$mailto|\$\{mailto\}|
						\$goto(?:success|failure|blank|expires)|
						\$\{goto(?:success|failure|blank|expires)\}|
						\$(?:sender)?subject|\${(?:sender)?subject\}|
						\$(?:sender)?replyto|\$\{(?:sender)?replyto\}|
						\$counter_\d+|\$\{counter_\d+\}|
						\$maillist_\d+|\$\{maillist_\d+\})/ix, $toValue);

	### Now look through what we've got.
	for (@chunks) {
		s/^\$\{(.*)\}$/\$$1/;
		($debug) && print STDERR "replacer looking at chunk $_\n";
		if (/^\$(((form|http|cookie)_[\w\-]+)|sql_\d+_\d+_\d+|
					mailto|(sender)?subject|(sender)?replyto|
					counter_\d+|maillist_\d+)/ix) {
			my $replaceStr = "";
			my $isCounter = 0;
			if (/^\$form_([\w-]+)/i) {
				### This is a value from the submitted form.
				$replaceStr = $query->param($1);
			} elsif (/^\$counter_\d+/i) {
				### This is a counter
				$needToReplace{lc($setValue)} = 1;
				$replaceStr = $_;
				$isCounter = 1;
			} elsif (/^\$(http_referer)/i) {
				### This is one of the http variables.
				$replaceStr = getHttpValue($1);
			} elsif (/^\$(http_ref)/i) {
				### This is a reference number, which we may work out with counters
				$needToReplace{lc($setValue)} = 1;
				$replaceStr = $_;
			} elsif (/^\$(http_[\w\-]+)/i) {
				### This is one of the http variables.
				$replaceStr = getHttpValue($1);
			} elsif (/^\$cookie_([\w-]+)/i) {
				### This is a cookie value.
				$replaceStr = $query->cookie($1);
			} elsif (/^\$(sql_\d+_\d+_\d+)$/) {
				### This is a sql statement return
				$replaceStr = $sqlVals{$1};
			} elsif (/^\$maillist_(\d+)$/) {
				### This is maillist info
				$replaceStr = $CONFIG{'maillistdata'}->{$1};
			} else {
				/^\$(.*)/;
				$replaceStr = $CONFIG{lc($1)};
				if ($1 =~ /^goto/i) { $escaped = 0; }
			}
			$replaceStr =~ s/\s/ /g;
			if ($escaped && !$isCounter) { $replaceStr = URLescape($replaceStr); }
			$tmpString .= $replaceStr;
		} else {
			$tmpString .= $_;
		}
	}
	($debug) && print STDERR "Replacer returns [$tmpString]\n";
	return $tmpString;
}


############################################################################
# Subroutine: getHttpValue ( string_to_match )
# Given a string starting with 'http_', this will return an appropriate
# value from the CGI environment, or an emprty string if it doesn't 
# recognise what was passed in.
############################################################################
sub getHttpValue {
	($debug) && (print STDERR "getHttpValue (@_) \@ " . time . "\n");
	$_ = shift;
	if (/^http_(remote_user|remote_addr|remote_ident|remote_host|
				server_name|server_port)$/xi) {
		return($ENV{"\U$1\E"});
	}
	if (/^(http_(user_agent|referer|from|host))$/i) {
		return($ENV{"\U$1\E"});
	}
	if (/^http_time/) {
		return(translateFormat("%hhhh%:%mm%:%ss%"));
	}
	if (/^http_date/) {
		return(translateFormat("%ddd% %mmmm% %dd% %yyyy%"));
	}
	if (/^http_ref/) { return($CONFIG{'ref'}); }
	if (/^http_config_path/) { return("$pageRoot/"); }
	if (/^http_config_error/) { return($CONFIG{'error'}); }
	return "";
}


############################################################################
# Subroutine: checkEmail ( email_address )
# Found a flaw in the email handling, so check that email addresses are
# correct... or at least contain reasonable characters
# The flaw would fail because the email had mismatched < brackets
############################################################################
sub checkEmail {
	($debug) && (print STDERR "checkEmail (@_) \@ " . time . "\n");
	$_ = shift;
	my ($opens, $closes);
	$opens = tr/</</; 
	$closes = tr/>/>/;
	fatal("Malformed Email in:\n\n    $_") if 
		($opens != $closes || $opens > 1 || $opens == 1 && !/^<.*>$/);
	s/</&lt;/, fatal("Can't handle email type:\n\n    $_") if 
		(/[^,\'\w\-\.\@\/\!\%\:\<\>\s\xc0-\xd6\xd8-\xf6\xf8-\xff ]/);
}


############################################################################
# Subroutine: fatal (msg)
# Takes a string message and makes a HTML failure page.
############################################################################
sub fatal {
	($debug) && (print STDERR "fatal (@_) \@ " . time . "\n");
	my ($msg) = @_;
	$msg = dehtml(undef, $msg);
	print "Content-type: text/html$CRLF$CRLF";
	print <<"	EOT";
	<HTML><HEAD><TITLE>Fatal Error</TITLE></HEAD>
	<BODY>
	<H1>Error:</H1>
	The soupermail CGI died due to the following error:<P>
	<BLOCKQUOTE><pre>$msg</pre></BLOCKQUOTE>
	<HR>
	Check your soupermail configuration or contact: 
	<A HREF="mailto:$soupermailAdmin">$soupermailAdmin</A> 
	informing them of the error, and how and where it occured.<P>
	<HR>
	<P>
	Soupermail Release Version $relVersion
	</P>
	</BODY></HTML>
	EOT
	cleanScratch();
	exit;
}


############################################################################
# Subroutine: securityFilename ( path_to_check )
# Exit the script if a filename contains ..'s or other potentially nasty
# characters.
############################################################################
sub securityFilename { 
	($debug) && (print STDERR "securityFilename (@_) \@ " . time . "\n");
	my ($filename) = shift;
	if ($filename =~ /\.\.|\~|[^\w\.\-\/:]/) {
		failSecurity("Filename $filename contains a .. " .
						" or other illegal characters");
		cleanScratch();
		exit;
	}
}


############################################################################
# Subroutine: securityName ( form_name_to_check )
# Exit the script if a given string contains shell meta characters
############################################################################
sub securityName {
	($debug) && (print STDERR "securityName (@_) \@ " . time . "\n");
	$_ = shift;
	my ($isrequired) = shift;
	my ($opens, $closes);
	my ($name) = $_;
	if ($isrequired) {
		### Required names can have brackets, &&s and ||s in, so strip
		### them from the name before checking and ensure they all match
		### up.
		$opens = tr/(//d;
		$closes = tr/)//d;
		fatal("Mismatched parentheses in:\n\n    $name") if 
			($opens != $closes);
		### Make sure people are only putting proper numbers of
		### ampersands in!
		s/&&|\|\|//g;
		#### And remove operators
		s/!=|==|<=|>=|<|>|!//g;
	}
	if (s!([^"'\w\s\.\-])!<font color="#ff0000"><b>$1</b></font>!g) {
		failSecurity ("$_ contains an insecure string such as a " .
						"shell meta character. Please use another string " .
						"containing only alphanumerics\n");
		cleanScratch();
		exit;
	}
}


############################################################################
# Subroutine: failSecurity ( failure_message )
# Something has failed a security check, so bomb out with a failure message
############################################################################
sub failSecurity {
	($debug) && (print STDERR "failSecurity (@_) \@ " . time . "\n");
	my ($msg) = shift;
	print $query->header();
	print "<HTML> <HEAD> <TITLE>Form Response</TITLE> </HEAD>\n";
	print "<BODY> <H1>Sorry</H1>\n";
	print "The form failed a security check.\n";
	if ($msg) {
		print "<P><H2>Failure Message:</H2><br \/>\n$msg\n";
	}
	print "</BODY> </HTML>\n";
	cleanScratch();
	exit;
}


############################################################################
# Subroutine: nukeValues ()
# This goes through all the form values, removing blank values and stripping
# leading and trailing space characters. Care is taken not to munge up 
# files that have been submitted using file upload.
############################################################################
sub nukeValues {
	($debug) && (print STDERR "nukeValues (@_) \@ " . time . "\n");
	no strict 'refs';
	my (@vals, @newvals, $val);
	foreach $val ($query->param()) {
		undef @newvals;
		@vals = $query->param($val);
		foreach (@vals) { 
			### Skip stripping for file upload fields.
			if (fileno($_)) { push(@newvals, $_); next; }
			s/(^\s+|\s+$)//g;
			### Read phrack 55 to see why the line below exists. ta rfp.
			s/\0//g;
			push (@newvals, $_) if /\S/;
		}
		$query->delete($val) unless (@newvals);
		$query->param($val, @newvals);
	}
}


############################################################################
# Subroutine: formIsBlank ()
# Return TRUE if the form is blank (i.e. has no non-ignored fields filled 
# in)
############################################################################
sub formIsBlank {
	($debug) && (print STDERR "formIsBlank (@_) \@ " . time . "\n");
	my (%names, $name, @vals);
	foreach ($query->param()) {
		@vals = $query->param($_);
		$names{$_} = ($#vals < 0) ? 0 : 1;
	}
	foreach $name (@ignored) {
		delete $names{$name};
	}
	return(!keys(%names));
}


############################################################################
# Subroutine: formMissingRequired ()
# Check that all the required bits have been filled in in the form.
# This bit is liable to change to add more complex behaviour
# Returns TRUE if the form has any missing bits
############################################################################
sub formMissingRequired {
	($debug) && (print STDERR "formMissingRequired (@_) \@ " . time . "\n");
	my ($name, $requiredLine, @requirednames, $replacement, $missing,
		$oldname);
	my (@vals);
	foreach $requiredLine (@required) {
		$missing = ! evalCond($requiredLine);
		last if ($missing);
	}
	return($missing);
}


############################################################################
# Subroutine: badTypes ( type_list )
# Check that the given datatypes for various fields are correct. Expects
# an array of type, value pairs to be passed in. Returns true if there
# are incorrect types.
############################################################################
sub badTypes {
	my $toCheck = shift;
	foreach (@$toCheck) {
		my ($type, $name) = @$_;
		my $v;
		foreach $v ($query->param($name)) {
			if (checkType($type, $v)) { return 1; }
		}
	}
	return 0;
}


sub checkType {
	my $type = shift;
	my $v = shift;
	my $r = 1;
	$type =~ s/^is//;
	if ($type =~ s/^not//) { $r = 0; }
	return 0 unless (defined $v);
	if ($type eq 'number') {
		if ($v !~ /^-?\d*(\.\d*)?$/) { return $r; }
	} elsif ($type eq 'integer') {
		if ($v !~ /^-?\d*(\.0*)?$/) { return $r; }
	} elsif ($type eq 'email') {
		if ($v !~ /^[\w\-\.\+\/\\\xc0-\xd6\xd8-\xf6\xf8-\xff ]+
				  \@[A-Za-z\d][\-\w]*[A-Za-z\d]
			(\.[\dA-Za-z][\-\w]*[A-Za-z\d])+$/x) { return $r; }
	} elsif ($type eq 'creditcard') {
		$v =~ s/\D//g;
		if (length($v) < 13) { return $r; }
		my ($sum, $i) = 0;
		foreach (reverse split(//, $v)) {
			my $s = $_ * (1 + $i++ % 2);
			$sum += $s - ($s > 9 ? 9 : 0);
		}
		if ($sum % 10) { return $r; }
	} 
	return !$r;
}

############################################################################
# Subroutine: returnHtml ( redirection_URL,
#						   template_pathname,
#						   return_message,
#						   boolean_replace_output_tags_flag,
#						   boolean_send_out_cookies_flag,
#						   boolean_is_pdf,
#						   mime_type)
# General routine to output HTML back to the browser.
############################################################################
sub returnHtml {
	($debug) && (print STDERR "returnHtml (@_) \@ " . time . "\n");
	my ($redirect, $template, $msg, $do_substitute, $do_cookie, $isPdf, $mime) = @_;
	my ($outstring);
	my @cookiesToGo = ();
	my $newCookie;

	### This goes throught the cookie settings generating CGI.pm cookie
	### objects.
	if ($do_cookie && @cookieList) {
		my $i = 0;
		while ($i < 3) {
			if ($cookieList[$i]) { 
				my %cookieVals = %{$cookieList[$i]};
				$i++,next unless ($cookieVals{"value"});
				$newCookie = $query->cookie(-name=>$cookieVals{"name"},
											-expires=>$cookieVals{"expires"},
											-value=>$cookieVals{"value"},
											-domain=>$cookieVals{"domain"},
											-path=>$cookieVals{"path"},
											-secure=>$cookieVals{"secure"});
				push(@cookiesToGo, $newCookie);
			}
			$i++;
		}
	}

	### Handle redirects or send the output from a template or default
	### message.
	if ($redirect) {
		if (@cookiesToGo) {
			print $query->redirect(-URL=>$redirect, -cookie=>\@cookiesToGo);
		} else {
			print $query->redirect($redirect);
		}
	} else {
		if ($template) {
			my $attName = $template;
			($debug) && print STDERR "Returning template $attName\n";
			$attName =~ s!.*/([^/]+)$!$1!;
			my $header = {};
			grabFile($template, \$outstring);
			if ($isPdf) {
				($do_substitute) && (substOutput(\$outstring, '4', 1));
				$attName =~ s/\..*$/\.pdf/;
				$attName .= ".pdf" unless ($attName =~ /\.pdf$/);
				($debug) && print STDERR "Attachment name $attName\n";
				$header->{'-Content_Disposition'} = "file;filename=${attName}";
			} else {
				($do_substitute) && (substOutput(\$outstring, '1'));
				if ($mime ne "text/html") {
					$header->{'-Content_Disposition'} = "inline;filename=${attName}";
				}
			}
			if (@cookiesToGo) {
				$header->{'-cookie'} = \@cookiesToGo;
			}
			$header->{'-type'} = "${mime};name=${attName}";
			print $query->header(%$header);
			if ($isPdf) {
				my $pdfFile = makePdf(\$outstring, $CONFIG{'pdftemplate'});
				($debug) && (print STDERR "sending out pdf $pdfFile\n");
				my $pdfOutput = "";
				grabFile($pdfFile, \$pdfOutput);
				($debug) && (print STDERR "pdf output size = " . 
										  length($pdfOutput) . " bytes\n");
				print $pdfOutput;
			} else {
				print $outstring;
			}
		} else {
			if (@cookiesToGo) {
				print $query->header(-type=>'text/html',
									-cookie=>\@cookiesToGo); 
			} else {
				print $query->header();
			}
			print "<HTML> <HEAD> <TITLE>Form Response</TITLE> </HEAD>\n";
			print "<BODY> $msg\n";
			print "</BODY> </HTML>\n";
		}
	}
}

############################################################################
# Subroutine: grabFile (filename, stringRef)
# Reads a file (usually a template) and places its contents in the thing
# specified by stringRef
############################################################################
sub grabFile {
	($debug) && (print STDERR "grabFile (@_) \@ " . time . "\n");
	my ($file, $buffer) = @_;
	my $fPath = $file;
	### Be paranoid, let admins block read access to directories or
	### block access on a global scale.
	$fPath =~ s/\\+/\//g;
	$fPath =~ s/(.*\/).*/$1/;
	if (-f "${fPath}$denyFile") {
		($debug) && print STDERR "SECURITY : ${fPath}$denyFile exists\n";
		failSecurity("Blocked from reading files in the given directory");
	}
	if ($paranoid && ! -f "${fPath}$allowFile") {
		($debug) && print STDERR "SECURITY : ${fPath}$allowFile doesn't exist\n";
		failSecurity("Not explicitly allowed to read files in the given directory");
	}
	my @stats = stat($file);
	open (FILE, "<$file") || fatal("Failed to open:\n\n    '${file}'");
	($fileLocking) && flock(FILE, LOCK_SH);
	binmode(FILE);
	read(FILE, $$buffer, $stats[7]);
	($fileLocking) && flock(FILE, LOCK_UN);
	close(FILE);
	($debug) && (print STDERR "file grabbed is $stats[7] bytes\n");
}

############################################################################
# Subroutine: returnBlank ()
# If the form was blank, produce a www page saying so
############################################################################
sub returnBlank {
	($debug) && (print STDERR "returnBlank (@_) \@ " . time . "\n");
	my ($msg) = "<H1>Sorry</H1>\n";
	$msg .= "You did not enter any form fields so the form was not submitted";
	returnHtml($CONFIG{'gotoblank'}, $CONFIG{'blank'}, $msg, 1, 
				$CONFIG{'blankcookie'},0,$CONFIG{'blankmime'});
}


############################################################################
# Subroutine: returnExpired
# The form is out of date, so return a page saying so.
############################################################################
sub returnExpired {
	($debug) && (print STDERR "returnExpired (@_) \@ " . time . "\n");
	my $msg = "<h1>Sorry</h1>The Form is now out of date. Your " .
				"information was not submitted.\n";
	my $goto = $CONFIG{'gotoexpires'} ? $CONFIG{'gotoexpires'} : '0';
	my $template = $CONFIG{'expirestemplate'} ? 
		$CONFIG{'expirestemplate'} : '0';
	returnHtml($goto, $template, $msg, 1, $CONFIG{'expirescookie'}, 0,
			   $CONFIG{'expiresmime'});
}


############################################################################
# Subroutine: returnFailure ()
# Return a failure page indicating that some required fields are missing
############################################################################
sub returnFailure {
	($debug) && (print STDERR "returnFailure (@_) \@ " . time . "\n");
	my $msg = "<H1>Sorry</H1>\n" .
			  "You did not complete all the required sections of the\n" .
			  "form.<br />Use your browser's BACK button to return to the\n".
			  "form and complete the missing fields.\n";
	my $goto = $CONFIG{'gotofailure'} ? $CONFIG{'gotofailure'} : '0';
	my $template = $CONFIG{'failure'} ? $CONFIG{'failure'} : '0';
	returnHtml($goto, $template, $msg, 1, $CONFIG{'failurecookie'}, 0,
			   $CONFIG{'failuremime'});
}


############################################################################
# Subroutine: returnSuccess ()
# The form has been successfully completed, so return a www page saying so
############################################################################
sub returnSuccess {
	($debug) && (print STDERR "returnSuccess (@_) \@ " . time . "\n");
	my $msg = "<H1>Thank You</H1>Your information has been submitted\n";
	my $goto = $CONFIG{'gotosuccess'} ? $CONFIG{'gotosuccess'} : '0';
	my $template = $CONFIG{'success'} ? $CONFIG{'success'} : '0';

	if (!$template && $CONFIG{'pdftemplate'}) {
		returnHtml($goto, $CONFIG{'pdftemplate'}, $msg, 1, 
				   $CONFIG{'successcookie'}, 1, 'application/pdf');
	} else {
		returnHtml($goto, $template, $msg, 1, $CONFIG{'successcookie'}, 0,
				   $CONFIG{'successmime'});
	}

	### Hmm, for user percieved speed, does closing STDOUT now help?
	close(STDOUT);
	if ($CONFIG{'fileto'}) {
		saveResults();
	}
	if ($CONFIG{'mailto'} || $CONFIG{'returntosender'} || 
		$CONFIG{'sendertemplate'} || $CONFIG{'htmlsendertemplate'} ||
		$CONFIG{'pdfsendertemplate'} || $CONFIG{'pdfmailtemplate'} ||
		$CONFIG{'maillist'} || $CONFIG{'listformfield'}) {
		$debug && print STDERR "About to mailResults\n";
		mailResults();
	}
}



############################################################################
# Subroutine: translateFormat ()
# Take a format string and return the expanded output.
############################################################################
sub translateFormat {
	($debug) && (print STDERR "translateFormat (@_) \@ " . time . "\n");
	my ($format) = shift;
	my ($offset) = shift;
	my ($mm, $mmm, $mmmm, $yy, $yyyy, $hh, $hhhh, $ss, $dd, $ddd, $ampm);
	my ($maxfactor) = 12; ### :-)
	my ($randomno);
	my $eTime = time;
	my ($currtime) = scalar (localtime($eTime));

	### Here, see if we need to rebuild based on an offset
	if ($offset && $offset =~ /^\s*([\+\-]?)\s*(\d+)\s*([smhd])\s*$/) {
		my $plusMinus = $1 ? $1 : "+";
		my $offBy = $2;
		my $unit = $3;
		($debug) && (print STDERR "got timeoffset of $1, $2, $3\n");
		if ($unit eq "m") { $offBy *= 60; }
		if ($unit eq "h") { $offBy *= 3600; }
		if ($unit eq "d") { $offBy *= 86400; }
		$currtime = scalar(localtime(eval("time $plusMinus $offBy")));
	}
	$currtime =~ /^(\w+)\s+(\w+)\s+(\d+)\s+(\d+):(\d+):(\d+)\s+(\d+)/;
	$ddd = $1;
	$mmmm = $2;
	$dd = $3;
	$hhhh = $4;
	$mm = $5;
	$ss = $6;
	$yyyy = $7;

	if ($offset && $offset =~ /^\s*([\+\-]?)\s*(\d+)\s*([My])\s*$/) {
		$mmm = $MONTHS{$mmmm};
		my $plusMinus = $1 ? $1 : "+";
		my $offBy = $2;
		my $unit = $3;
		($debug) && (print STDERR "got timeoffset of $1, $2, $3\n");
		if ($unit eq "M") {
			my $diff = eval("\$mmm $plusMinus \$offBy");
			if ($diff > 12 || $diff < 1) {
				($debug) && (print STDERR "evaling $yyyy $plusMinus floor(($diff - 1) / 12)\n");
				$yyyy = eval("\$yyyy + floor((\$diff - 1) /12)");
			}
			($debug) && (print STDERR "year is now $yyyy\n");
			$mmm = eval("\$mmm $plusMinus \$offBy");
			if ($mmm != 12) { $mmm = $mmm % 12; }
			$mmm = 12 unless ($mmm);
		} else {
			($debug) && (print STDERR "evaling $yyyy $plusMinus $offBy\n");
			$yyyy = eval("\$yyyy $plusMinus \$offBy");
		}
		my $eTime = timelocal(1, 1, 1, $dd, $mmm - 1, $yyyy);
		$currtime = scalar (localtime($eTime));
		$currtime =~ /^(\w+)\s+(\w+)\s+(\d+)\s+\d+:\d+:\d+\s+(\d+)/;
		$ddd = $1;
		$mmmm = $2;
		$dd = $3;
		$yyyy = $4;
	}
	$mmm = $MONTHS{$mmmm};
	$hh = ($hhhh > 12) ? ($hhhh - 12) : $hhhh;
	$ampm = ($hhhh > 12) ? "pm" : "am";
	$yyyy =~ /(\d\d)$/;
	$yy = $1;
	$hh = sprintf("%02u", $hh);
	$mm = sprintf("%02u", $mm);
	$ss = sprintf("%02u", $ss);
	$dd = sprintf("%02u", $dd);
	$yy = sprintf("%02u", $yy);
	$format =~ s/%yyyy%/$yyyy/gi;
	$format =~ s/%hhhh%/$hhhh/gi;
	$format =~ s/%ddd%/$ddd/gi;
	$format =~ s/%mmmm%/$mmmm/gi;
	$format =~ s/%mmm%/$mmm/gi;
	$format =~ s/%mm%/$mm/gi;
	$format =~ s/%dd%/$dd/gi;
	$format =~ s/%yy%/$yy/gi;
	$format =~ s/%ss%/$ss/gi;
	$format =~ s/%hh%/$hh/gi;
	$format =~ s/%ampm%/$ampm/gi;
	$format =~ s/%epoch%/$eTime/gi;
	$format =~ s/%counter_(\d+)%/$CONFIG{"counter"}->{"${1}value"}/gi;
	while ($format =~ /%(r{1,$maxfactor})%/) {
		my ($tmp) = $1;
		$randomno = rand (10 ** length($tmp));
		$randomno = int (10 ** $maxfactor + $randomno);
		$randomno = substr ($randomno, length($randomno) - length($tmp) );
		$format =~ s/%${tmp}%/${randomno}/;
	}

	return $format;
}


############################################################################
# Subroutine: showFile ( filename )
# Make a OS specific call to show a given file for the webserver...
# unhides under NT, chmods it under UNIX
############################################################################
sub showFile {
	($debug) && (print STDERR "showFile (@_) \@ " . time . "\n");
	my $filename = shift;
	no strict 'subs';
	if ($OS eq "windows") {
		Win32::File::SetAttributes($filename, Win32::File::NORMAL)
	} else {
		if ($CONFIG{"cgiwrappers"}) {
			chmod 0644, $filename;
		} else {
			chmod 0666, $filename;
		}
	}
}



sub makeScratch() {
	($debug) && (print STDERR "makeScratch (@_) \@ " . time . "\n");
	if ($CONFIG{'pgpuserid'} || $CONFIG{'filepgpuserid'} ||
		$CONFIG{'pdfsendertemplate'} || $CONFIG{'pdfmailtemplate'} ||
		$CONFIG{'pdftemplate'}) {
		if ($OS eq "windows") {
			my $rand = "$$" . int(rand(99999999));
			$rand =~ s/(.{8}).*/$1/;
			$scratchPad = "${tempDir}$rand";
		} else {
			$scratchPad = "${tempDir}soupermail$$" . int(rand(99999999));
		}
		fatal("Unable to create unique tmp directory:\n\n    $scratchPad") 
			 if (-e $scratchPad || -d $scratchPad || -l $scratchPad);

		umask(011);
		mkdir($scratchPad, 0766) || fatal("can't create tmp area:\n\n    $scratchPad");
		open (ALLOW, ">${scratchPad}/$allowFile");
		print ALLOW "x";
		close ALLOW;
	}
}

sub cleanScratch {
	($debug) && (print STDERR "cleanScratch (@_) \@ " . time . "\n");
	### Clean up the temp scratch pad directory.
	if ($CONFIG{'pgpuserid'} || $CONFIG{'filepgpuserid'} ||
		$CONFIG{'pdfsendertemplate'} || $CONFIG{'pdfmailtemplate'} ||
		$CONFIG{'pdftemplate'} && -d $scratchPad) {
		($debug) && (print STDERR "Cleaning $scratchPad\n");
		opendir (DIR, $scratchPad);
		my $item;
		my @items = readdir(DIR);
		closedir(DIR);
		while ($item = shift (@items)) {
			if ($item =~ /^[^\.]/ && -f "${scratchPad}/$item") {
				unlink("$scratchPad/$item");
			}
		}
		if (-d $scratchPad) {
			chdir ($tempDir);
			rmdir ($scratchPad) ||
				(($debug) && print STDERR "Unable to remove $scratchPad $!\n");
		}
	}
}



############################################################################
# Subroutine: doCounters ( mode_type )
#
# Look through the available counters, setting those that need to be set
# based on the given mode.
############################################################################

sub doCounters {
	my $counters = $CONFIG{"counter"};
	my $mode = shift;
	my ($n, $v);
	while (($n, $v) = each %$counters) {
		if ($n =~ /(\d+)on$mode/ && $v) {
			setCounter($1);
		}
	}
}

############################################################################
# Subroutine: setCounter ( counter_number )
#
# Take a counter from the counter hash and increase its value by whatever
# step is defined (or one if undefined)
############################################################################

sub setCounter {
	my $counterNum = shift;
	my $counterValue = $CONFIG{"counter"}->{"${counterNum}value"} +
					   $CONFIG{"counter"}->{"${counterNum}step"};

	if ($CONFIG{"counter"}->{"${counterNum}set"} ||
		$CONFIG{"counter"}->{"${counterNum}set"} eq "0") {
		$counterValue = $CONFIG{"counter"}->{"${counterNum}set"}
	}
	$CONFIG{"counter"}->{"${counterNum}value"} = $counterValue;

	if ($CONFIG{"counter"}->{"${counterNum}file"}) {
		open(COUNTER, ">" . $CONFIG{"counter"}->{"${counterNum}file"});
		print COUNTER $counterValue;
		close (COUNTER);
	}
}



__END__

=head1 NAME

Soupermail - a generic CGI WWW form handler written in Perl

=head1 SYNOPSIS

E<lt>form method="post" action="/cgi-bin/soupermail.pl"E<gt>

=head1 DESCRIPTION

Soupermail is a generic HTML form handling script designed to provide a
high degree of control over a form's behaviour and output. It provides the 
following features:

=over 4

=item * Email the contents of a form to one or more email addresses

=item * Expire a form based on the date

=item * Handle blank forms intelligently

=item * Limited conditional control based on the form's contents

=item * HTML and text templates

=item * Copy the form email to the form's sender

=item * PGP encrypt resulting emails (requires PGP 2, 5 or GNUPG installed)

=item * Write the contents of a form to a file

=item * Write the encrypted contents of a form to a file

=item * Generate a unique reference number for each submission

=item * Set certain form fields as required

=item * Word wrap resulting emails

=item * Handle file uploads, and send them on as MIME attachments

=item * Access CGI variables through templates

=item * Set cookies and display cookies by using templates

=item * Send the form's submitter a formatted reply

=item * Set any number of counter files up on the server

=item * Send mail as HTML and/or plain text 

=item * Act as a frontend for PDF generation with Lout and GhostScript

=item * Attach files to outgoing emails

=item * Validate form fields

=item * Send customised emails to lists of email addresses

=item * Return any mime type back to the browser (eg. XML)

=item * Read and write from SQL databases

=back

Soupermail can be used to handle single standalone forms, or generate and
control complex multipart forms.

=head1 RESTRICTED FORM FIELDS

Soupermail assumes some form fields have special meanings. These field names
ARE CASE SENSITIVE. The following is a list of such fields:

=over 4

=item B<Email>

Assumed to be the email address of the form's sender. Needed if the email is to
be copied to the sender, or you are using a B<sendertemplate>. When Soupermail
sends and email back, it will use the value of this field as the email's From:
address.

=item B<SoupermailConf>

This is a path to the configuration file that controls soupermail. The path
can either be relative to the location of the form, or an absolute path
from the webserver's root. If you are using soupermail to generate multipart
forms, it is recommended that you use absolute paths.


=back


=head1 CONFIGURATION FILES

Soupermail is controlled on a per form basis by using B<configuration files>.
Each form handled by soupermail must have an associated configuration file. 

The location of the file is passed to soupermail through the PATH_INFO CGI
variable, or by using 'SoupermailConf' as a form parameter. 
The PATH_INFO is set by providing a path after the call to soupermail
in the E<lt>formE<gt> element of the HTML page.

=over 4

=item eg. 

If a form has a configuration file in F</forms/config.txt>, the form
should call soupermail with

E<lt>C<form method="post" action="/cgi-bin/soupermail.pl/forms/config.txt">E<gt>

or as a form variable with:

E<lt>C<input type="hidden" name="SoupermailConf" value="/forms/config.txt">E<gt>

=back

The B<second> method of supplying the config file is recommended. People 
running under a cgiwrapped environment will have problems with the first 
method, and even worse, the IIS webserver defaults to not supporting 
the PATH_INFO method.

The path to the configuration file must be relative to the web server's 
root directory. Do not use URLs or absolute paths to the configuration file.

The format for a configuration file is a series of configuration
statements of the form:

=over 4

C<I<name> : I<value>>

or

C<if : I<condition> then name : I<value>>

or

C<unless : I<condition> then I<name> : I<value>>

=back

If a badly phrased or incorrect configuration file is passed to soupermail,
it will complain, so always check your soupermail configurations carefully.

Valid I<names> for the configuration file are:

=over 4

=item B<    7bit>

This can be set to B<yes> or B<no>. If its B<yes>, then email is sent 
out encoded as quoted printable characters (i.e. 7bit safe). By default though,
email is sent out as 8bit, and its assumed the mailservers in the
transmission route will handle the 8bit conversions. You should only
need to alter this if you are experiencing character corruption in your
emails.

=item B<alphasort>

Set to B<yes> or B<no>. When email is sent without a C<mailtemplate>, 
the form fields are displayed in the email in alphabetical order.
Setting this value to B<no> does not sort the fields, and returns them 
in the same order that the browser sent them.

=item B<attachmentI<X>>

Files can be attached to email sent with C<sendertemplate> and 
C<htmlsendertemplate>. B<I<X>> is a number identifying the attachment.

See also C<listattachmentI<X>>

=over 4

=item eg.

=for text
C<attachment1 : /forms/download/myfile.pdf
attachment3 : file2.doc>

=for man
C<attachment1 : /forms/download/myfile.pdf
attachment3 : file2.doc>

=for html
<pre>attachment1 : /forms/download/myfile.pdf
attachment3 : file2.doc</pre>

=back

=item B<attachmentI<X>mime>

Since Soupermail doesn't know about MIME types, you may want to set a
specific MIME type for an attachment so receiving mail clients know how
to deal with them. By default, Soupermail sends text attachments as
B<text/plain> and binary attachments as B<application/octet-stream>.

See also C<listattachmentI<X>mime>

=over 4

=item eg. 

=for text
C<attachment2 : /wordfile.doc
attachment2mime : application/x-msword
attachment5 : /forms/download/myfile.pdf
attachment5mime : application/pdf>

=for man
C<attachment2 : /wordfile.doc
attachment2mime : application/x-msword
attachment5 : /forms/download/myfile.pdf
attachment5mime : application/pdf>

=for html
<pre>attachment2 : /wordfile.doc
attachment2mime : application/x-msword
attachment5 : /forms/download/myfile.pdf
attachment5mime : application/pdf</pre>

=back

=item B<bcc>

This is a comma separated list of email addresses to blind carbon copy on
the email sent to the C<mailto> addresses. See also C<senderbcc>.

=item B<blank>

A template file to return to the user if they submitted a blank form.

=over 4

=item eg. 

C<blank : /forms/config/blank.tpl>

=back

=item B<blankmime>

The MIME type that's returned to the browser for the C<blank> template. Also
see C<successmime>, C<expiresmime> and C<failuremime>.

=item B<cgiwrappers>

Set to B<yes> or B<no>.
If you are running Soupermail in a CGI wrappers type environment, where 
Soupermail's running with its owner's permissions rather than the webserver's
permissions, setting cgiwrappers to B<yes> will make the
C<filereadable> config command actually work.

=item B<cookie[123456789]domain>

This specifies the domain name that the cookie will be sent to. By default,
no domain is specified for a cookie. See the section on L<COOKIES> for
more information.

=over 4

=item eg.

C<cookie1domain : myhost.domainname.com>

Will only send cookie1 to pages on the myhost.domainname.com webserver. See
the section on L<COOKIES> for more information.

=back

=item B<cookie[123456789]expires>

A date or time format indicating when one of the nine available cookies
expires. Allowable formats can be relative. eg. B<+1h> means one hour from
now, B<-2d> means 2 days ago. The time periods allowable are s = second, 
m = minute, h = hour, d = day, M = month, y = year.

Absolute dates and times can also be specified.

See the section on L<COOKIES> for more information. 

=over 4

=item eg.

C<cookie1expires : 1-4-1999 12:00:00>

will expire the first cookie at midday on 1 April 1999.

C<cookie2expires : +1M>

will expire the second cookie one month from when the form was submitted

=back

By default, cookies expire 24 hours from when they were set.

=item B<cookie[123456789]name>

This sets the name of one of the nine available cookies to a value. See the
section on L<COOKIES> for more information.

=over 4

=item eg.

C<cookie1name: zippy>

sets the first cookie's name to 'zippy'

=back

=item B<cookie[123456789]path>

This specifies which pathnames a cookie will be sent to. By default, this
will be to the location where soupermail is stored. See the section on
L<COOKIES> for more information.

=over 4

=item eg.

C<cookie3path : /products>

Would only send cookie 3 to pages below the /products directory of a website.

=back

=item B<cookie[123456789]secure>

This is a yes or no value that specifies whether a cookie will be sent over
all connections, or just secure SSL connections. See the section on 
L<COOKIES> for more information.

=item B<cookie[123456789]value>

This sets the value of one of the nine available cookies. See the section
on L<COOKIES> for more information.

=item B<cookieonblank>

If set to yes, this will send cookies when a blank form is detected.

=item B<cookieonexpires>

When set to yes, this will send cookies when a submission past an
expires date is sent.

=item B<cookieonfailure>

When this is set to yes, cookies will be sent out even if the form
has been considered a failure.

=item B<cookieonsuccess>

When set to yes, cookies are sent out when the form is considered a
success. This is the default behaviour.

=item B<counterI<X>file>

Each counter is stored on the webserver in a single file. The file simply
contains a number and should be specified in a directory that's writable by
the webserver. When a counterfile line is read into the config file, the
counter's value is made available for later use in the config file. See
L<COUNTERS> for more information.

=item B<counterI<X>onblank>

If set to C<yes>, this specifies that counter I<X> will be incremented
if a blank form is submitted.

=item B<counterI<X>onexpires>

If set to C<yes> this specifies that counter I<X> will be incremented
if the form is submitted after its expiry date.

=item B<counterI<X>onfailure>

If set to C<yes> this specifies that counter I<X> will be incremented
if the form is missing required fields.

=item B<counterI<X>onsuccess>

If set to C<yes> this specifies that counter I<X> will be incremented
if the form is submitted successfully. The default is to increase the counter
by is 1.

=item B<counterI<X>step>

This is a positive integer value that specifies how much counter I<X>
should be increased by.

=item B<encodesubjects>

By default, the Subject line of emails is assumed to be 7bit ASCII. However,
if you are sending non-ASCII characters, and have set the C<mailcharset>
option, then Subject lines are encoded as described in RFC 2047.

=item B<error>

This is an error message that you can generate and that becomes available
to use in the config file and templates as C<http_config_error>. If an
error is set, SQL commands will not run, and Soupermail will run in a
failure mode.

=item B<expires>

A date of the format dd-mm-yyyy after which the form cannot be submitted

=over 4

=item eg.

C<expires : 24-12-1998>

=back

This means the form would not be submittable after the 24st of December 1998

=item B<expiresmime>

The MIME type to return to the browser when C<expirestemplate> is sent
out. See also C<successmime>, C<blankmime> and C<failuremime>.

=item B<expirestemplate>

A template file to use if the form has been submitted after its B<expires>
date. See the section on L<TEMPLATES> for more information.

=item B<failure>

A template to return to the user if they have not completed all the required
fields of a form. See the section on L<TEMPLATES> for more information.

=over 4

=item eg.

C<failure : /forms/config/bad.tpl>

=back

=item B<failuremime>

The MIME type to return to the browser when the C<failure> template is sent
out. See also C<successmime>, C<blankmime> and C<expiresmime>.


=item B<fileattop>

When writing the contents of a form to a file, new data is usually placed
at the end of the file. By setting C<fileattop>, new data can be written
at the start of the file (although after any specified header).

=over 4

=item eg.

C<fileattop : yes>

=back

=item B<filebackupformat>

This specifies a filename for backup files to be written into if a soupermail
generated file will grow over a C<filemaxbytes> limit.

The value for this can include formatting codes as listed in the
L<FORMATS> section of this document. This lets you generate a number of backups
with a very fine level of detail.

The value specified in C<filereadable> will affect any backup files generated.

=over 4

=item eg.

C<filebackupformat: /files/backup.txt>

would always backup the file to /files/backup.txt

C<filebackupformat: /files/%yyyy%%mmm%%dd%backup.txt>

would backup to /files/19980801backup.txt on 1 August 1998.

=back

=item B<filemaxbytes>

This specifies the maximum size a soupermail generated file can grow to in
bytes. If a new addition would cause the generated file to grow over
C<filemaxbytes>, then the file will be cleared of all other entries.

If you would like to save backup copies of the file, rather than simply
deleting it, specify a C<filebackupformat> as described above.

To force a deletion after each entry, set the filemaxbytes to 1. Note that
setting it to 0 (zero), effectively resets filemaxbytes, and so has no
effect.

=over 4

=item eg. 

C<filemaxbytes: 10000>

=back

=item B<filepgpuserid>

If you want to store the data from a form encrypted, you can use
C<filepgpuserid> to securely store data.

=over 4

=item eg. 

C<filepgpuserid: vittal.aithal@bigfoot.com>

Will store data encrypted for vittal.aithal@bigfoot.com

=back

=item B<filereadable>

When writing form data to a file, the file is usually kept unreadable by the 
webserver. By setting C<filereadable>, the file can be made readable by the
webserver.

Note that this only affects people reading the file from a web browser, it
does not secure the file from other types of access (eg. from FTP or through
the filesystem). So, don't go storing credit card numbers in a file unless
you're damn sure that your machine's secure.

=over 4

=item eg.

C<filereadable : yes>

=back

=item B<filetemplate>

A template file which determines how a set of form data should be written to 
the file specified by C<fileto>. See the section on L<TEMPLATES> for more 
information.

=item B<fileto>

The filename that the contents of a form should be written to. The path is
either relative to the location of the configuration file or an absolute
path from the web server's root.

=over 4

=item eg.

C<fileto : output/out.txt>

=back

If no C<filetemplate> is given, the output form a form is written as a series
of lines matching:

C<name = value[,value ...]>

Where a form field has multiple values, these are listed separated by commas.

=item B<footings>

This is a plain text file that can be placed at the end of files specified by
C<fileto>.

=item B<gotoblank>

A URL for a page to redirect the user to if their form entry was blank. Unlike
the C<blank> field, the file is not a template, and so should not contain
E<lt>outputE<gt> elements. CGI variable replacement can be used in the value of C<gotoblank> to achieve L<PIPELINING>.


=over 4

=item eg.

C<gotoblank : http://myserver/errors/blank.htm>

=back

=item B<gotoexpires>

A URL for a page to redirect to if the form has past its C<expires> date.
CGI variable replacement can be used in the value of C<gotoexpires> to achieve L<PIPELINING>.

=item B<gotofailure>

A URL for a page to redirect the user to if their form entry did not contain
all the required fields. Unlike the C<failure> entry, this is not a template
and should not contain E<lt>outputE<gt> elements. CGI variable replacement 
can be used in the value of C<gotofailure> to achieve L<PIPELINING>.

=over 4

=item eg.

C<gotofailure : http://myserver/errors/failed.htm>

=back

=item B<gotosuccess>

A URL for a page to redirect the user to if their form entry was successfully
completed. Unlike the C<success> field, this is not a template and should
not contain E<lt>outputE<gt> elements. CGI variable replacement can be 
used in the value of C<gotosuccess> to achieve L<PIPELINING>.

=over 4

=item eg.

C<gotosuccess : http://myserver/forms/success.htm>

=back

=item B<gnupg>

It is possible to use the GNU Privacy Guard program rather than PGP. If you
do use it, then set C<gnupg> to yes in your configuration. If you do not,
then Soupermail will assume encryption is using PGP. This command is now
deprecated in favour of C<pgpversion>.


=item B<headings>

This is a plain text file that can be placed at the start of files specified
by C<fileto>.

=item B<htmllisttemplate>

The HTML email template to use for the L<MAILING LISTS> function. This
and/or a C<listtemplate> must be used for mailing lists to work.

=item B<htmlmailtemplate>

This option allows you to send mail formatted in HTML. Only the HTML
is sent, images are not encoded or sent. All relative links from the HTML
will be from the location of the config file on the server.
Probably the best thing to do with HTML templates is use absolute URLs
for images and suchlike.

If you specify both C<htmlmailtemplate> and C<mailtemplate> a mixed
text and HTML message is generated. This will allow people who don't have
HTML capable mail clients to read your mail.

=item B<htmlsendertemplate>

In the same way as C<htmlmailtemplate> is sent to the C<mailto> address, this
template is used when sending mail to the submitter of the form. It behaves
in the same way as C<htmlmailtemplate> when it comes to link handling.

=item B<ignore>

If your HTML forms contain hidden fields, you can C<ignore> them so that
you can check for situations where the user doesn't complete any fields. Only
one form field can be specified on an ignore line. Use multiple ignore lines
if you wish to ignore more than one field. The soupermail special form
variable C<SoupermailConf> is ignored automatically.

=over 4

=item eg.

=for text
C<ignore : hidden1
ignore : hidden2>

=for man
C<ignore : hidden1
ignore : hidden2>

=for html
<pre>ignore : hidden1
ignore : hidden2</pre>

This would ignore the values of fields 'hidden1' and 'hidden2' 
when determining if a form was left blank.

=back

=item B<if>

A conditional statement used to set configuration values based on the user's
form input. See the section on L<CONDITIONAL STATEMENTS> for more information.

=over 4

=item eg.

C<if : (division eq 'Accounts') then mailto : accounts@mycompany.com>

This would set C<mailto> to accounts@mycompany.com if the form contained
a field called 'division' and its value was 'Accounts'.

=back

=item B<iscreditcard>

This is used to validate a form field to see if its a credit card number.
The check performed is a basic Luhn checksum, and doesn't check card
ranges.

=over 4

=item eg.

If you have a field called 'creditc' in your form, and want to validate it,
use:

C<iscreditcard: creditc>

=back

If the validation fails, the C<failure> template is activated. Validation will
not fail if the field is left blank.

=item B<isemail>

This is used to validate a form field is an email address. If the validation 
fails, the failure template is activated.

=item B<isinteger>

This is used to validate a form field is an integer. If the validation fails, 
the failure template is activated.

=item B<isnumber>

Behaves in the same way as the isinteger option, and validates a form field 
as a number.

=item B<isnotcreditcard>

Used to check is a form field is NOT a credit card number.

=item B<isnotemail>

Used to check is a form field is NOT an email address.

=item B<isnotinteger>

Used to check is a form field is NOT an integer.

=item B<isnotnumber>

Used to check is a form field is NOT a number.

=item B<listattachmentI<X>>

This defines an attachment that is sent from the server to each mail
sent to the mailing list. It's syntax is the same as that of
C<attachmentI<X>>.

=item B<listattachmentI<X>mime>

This is the MIME type for an attachment sent to the mailing list.
See C<attachmentI<X>mime> for the syntax.

=item B<listbase>

When HTML email is sent to a mailing list, Soupermail inserts a
Content-Location email header based on the submitting form's URL. Use this
option to modify it for your own needs. Similar to C<senderbase> and
C<mailbase>.


=item B<listfrom>

The email address to use in the From: field for emails sent out using 
Soupermail's L<MAILING LISTS> function.

=item B<listformfield>

Sometimes, you may want to send emails to a mailing list
sent to the form through a form field. This config command says
which form field contains this data.

=item B<listprecedence>

When email is sent out with Soupermail's L<MAILING LISTS> function, the
Precedence mail header is set to prevent mail loops. It can take one
of three possible values; B<list>, B<junk> and B<bulk>. By default, the
Precedence value is B<list>.

=item B<listreplyto>

The email address to use in the Reply-To: field for emails sent out using 
Soupermail's L<MAILING LISTS> function.

=item B<listsql>

The data for a mailing list can be pulled from a SQL database as long as
the C<sqlname>, C<sqluser>, C<sqlpassword> and appropriate C<sqlbind>
values have been set. C<listsql> is an SQL command in the same format
as C<sqlrunI<X>> commands.

The data returned from the SQL statement must have the user's email
address as the first column.


=item B<listsubject>

The Subject: line to be used for emails sent out using the 
L<MAILING LISTS> function.

=item B<listtemplate>

The plain text message template to use for the L<MAILING LISTS>
function. This and/or a C<htmllisttemplate> must be specified for a
mailing list to work.

=item B<mailbase>

When HTML email is sent to the C<mailto> address, Soupermail inserts a
Content-Location email header based on the submitting form's URL. Use this
option to modify it for your own needs. Similar to C<senderbase> and
C<listbase>.

=over 4

=item eg.

C<mailbase : http://www.example.com/graphics/>

=back

=item B<mailcharset>

This defines the character set to send email as. It defaults to iso-8859-1.

=item B<maillist>

This option is the location for a L<MAILING LISTS> file.

=over 4

=item eg.

C<maillist : /forms/config/mynames.csv>

=back

=item B<mailtemplate>

A template file to use when formatting the outgoing email. See the section 
on L<TEMPLATES> for more information.

=over 4

=item eg.

C<mailtemplate : /forms/config/mail.tpl>

=back

=item B<mailto>

A comma separated list of email addresses to send the results of the email to.

=over 4

=item eg.

C<mailto : rod@mycompany.com, jane@othercompany.com, freddy@mycompany.com>

=back

=item B<mimeon>

When set, Soupermail will allow file uploads from web browsers using RFC1867
and will attach the uploaded files as MIME attachments on resulting emails.

=over 4

=item eg.

C<mimeon : yes>

This would allow MIME attachments to be sent.

=back

=item B<nofilecr>

When saving results to a file, it is sometimes useful to remove newline
characters from the results. Setting C<nofilecr> will do this.

=over 4

=item eg. 

C<nofilecr : yes>

This would remove newline characters from fields written to a file.

=back

=item B<nomailfooter>

Do not display the hostname and IP address details at the foot of each 
outgoing email.

=over 4

=item eg.

C<nomailfooter : yes>

=back

=item B<pdftemplate>

This is a lout template file that will be processed into a PDF and returned 
to the browser. If you want to use this option, don't specify a C<success> 
template in your config file. See the L<MAKING PDFs> section for more
details.

=item B<pdfmailtemplate>

This is a lout template file that will be processed into a PDF and returned 
to the C<mailto> email recipient as an email attachment. It can be used 
in conjunction with C<mailtemplate> and C<htmlmailtemplate>.

=item B<pdfsendertemplate>

This is a lout template file that will be processed into a PDF and returned 
to the email address given in the B<Email> form field. It can be used 
in conjunction with C<sendertemplate> and C<htmlsendertemplate>.

=item B<pgpmime>

By default, Soupermail will send PGP messages as a multipart/encrypted MIME
message (as per RFC 2015). However, not all PGP mail plugins recognise 
this format (eg, the Pegasus mail PGP plugin). Setting pgpmime to B<no> 
will not encapsulate the PGP message in MIME headers.


=item B<pgppdfs>

If set to 'no', then PDF's generated with Soupermail are NOT encrypted when
sent. Instead, they are attached to the encrypted content of the email.
The default behaviour is to encrypt PDFs.

=item B<pgpport>

This is the port number of a HTTP PGP 5 keyserver. The default port is
11371. The hostname for the server is specified with B<pgpserver> below.
See the section on L<USING PGP> for more information.

=item B<pgpserver>

This is the hostname of a HTTP PGP 5 keyserver to get PGP keys from.
See the section on L<USING PGP> for more information.

=over 4

=item eg.

C<pgpserver : pgpkeys.mit.edu>

=back

=item B<pgpuploads>

If set to 'no', then uploaded files are NOT encrypted when
sent. Instead, they are attached to the encrypted content of the email.
The default behaviour is to encrypt uploaded files.


=item B<pgpuserid>

A user in the public keyring which outgoing email should be encrypted for.
See the section on L<USING PGP> for more information.

=over 4

=item eg.

C<pgpuserid : bungle@mycompany.com>

=back

=item B<pgpversion>

From version 1.0.8, this is the prefered mechanism for selecting the
type of encryption to use. Values for this can currently be
'gpg', 'pgp2' and 'pgp5'. By using this field, future versions of PGP and
GNUPG can be supported.

=item B<ref>

A format for a reference number to be generated and used as the
I<http_ref> CGI variable. See the sections on L<CGI VARIABLES> and 
L<FORMATS> for more information.

=over 4

=item eg.

C<ref : REF%yy%%mmm%%dd%%rrrr%>

This may generate a reference like: REF9704016364 on April 1 1997

=back

=item B<replyto>

An email address that will be used in the Reply-To: mail header.

=over 4

=item eg.

C<replyto : zippy@mycompany.com>

=back

=item B<required>

A boolean expression which determines which form fields must be completed. 
The entry is composed of field names separated by && (AND) and || (OR) 
operators. See the section on L<Boolean Expressions> for more details.

=over 4

=item eg.

C<required : ((name && address) || telephone)>

The above expression requires either the fields name and address to be 
completed, or the field telephone to be completed.

=back

=item B<returntosender>

This will CC the sender of the form a copy of the email message sent as a 
result of the form. This requires the form to have a field called Email (case
sensitive), which is assumed to be the sender's email address.

=over 4

=item eg.

C<returntosender : yes>

=back

=item B<senderbase>

When HTML email is sent to the submitter of a form, Soupermail inserts a
Content-Location email header based on the submitting form's URL. Use this
option to modify it for your own needs. Similar to C<listbase> and
C<mailbase>.

=item B<senderbcc>

This is a comma separated list of email addresses to blind carbon copy on
the email sent to the form's sender when a C<sendertemplate> is specified.
See also C<bcc>.

=item B<senderfrom>

When using a C<sendertemplate>, the email address used in the email back to
the form's sender is set to this. The preferred order email addresses are 
chosen for the sender's From field is:

=over 4

=item * senderfrom

=item * senderreplyto

=item * mailto

=item * replyto

=item * sender's email address

=back

This field is useful if you need an auto-reply function from your form, but
don't want to obviously expose the mailto address directly to the sender of
a form.

=item B<senderreplyto>

An email address that will be used in the Reply-To: mail header for mails
sent with the C<sendertemplate> config option.

=item B<sendersubject>

Used in conjunction with C<sendertemplate>, this is a subject line only to
be used in email messages send directly back to the form's submitter. If its
not set, the subject line set with the C<subject> config line is used.

=item B<sendertemplate>

This is a template file for an email to be sent back to whoever submitted
the form. It takes the email address to send this to from the B<Email>
form variable. The From field of the email is set to either the C<mailto>
or C<replyto> configuration values. See the section on L<TEMPLATES> for
more information.

=item B<setcounterI<X>>

This sets the value of a counter prior to any templates being filled based
on the counter's onsuccess, onfailure, onblank and onexpires config
values.

=item B<sqlbindI<X>>

Using the C<sqlbind> command allows you to specify a variable that will 
be used in the next SQL statement specified by a C<sqlrunI<X>> command.

=over 4

=item eg.

=for text
C<sqlbind2: "$form_second_field"
sqlrun1: SELECT * FROM TABLE WHERE field1 = ? AND field2 = ?>

=for html
<pre>sqlbind2: "$form_second_field"
sqlrun1: SELECT * FROM TABLE WHERE field1 = ? AND field2 = ?</pre>

In this example, the value of the form field "second_field" is
used to replace the second question-mark value in the SQL statement.

=back

Binding does all the character escaping needed by the SQL, so there
is no need to enclose strings in single quotes.


=item B<sqlname>

This is the DBI name for the next database connection you will use.
You can use multiple connections during the course of a config file.
The format for the name is the normal DBI format.

=over 4

=item eg.

C<sqlname: dbi:mysql:database=test;host=mysql.example.net>

=back

=item B<sqlpassword>

This is the connection password that will be used for the next SQL
command run in the config file. Usually used with C<sqluser>.

=over 4

=item eg.

C<sqlpassword: my_random_password>

=back

=item B<sqlrunI<X>>

Multiple SQL statements can be executed in a config file, and
each statement is defined by a C<sqlrunI<X>> command. Statements are
executed in the order they are seen in the config file, working from
top to bottom. 

The number at the end of the C<sqlrunI<X>> name is used to
identify the results of the command for later use in the config
file and in templates.

Variables that you want to use in your SQL command that come from 
form, cookie or counter data must be passed in by I<binding> the
values. Binding involves using a question-mark character to represent
a variable, and setting a C<sqlbind> command to indicate something to
use.

=over 4

=item eg.

=for text
C<sqlbind1: "$form_name"
sqlrun1: SELECT id FROM users WHERE name LIKE ?>

=for html
<pre>sqlbind1: "$form_name"
sqlrun1: SELECT id FROM users WHERE name LIKE ?</pre>

The bind command attaches the value of the form field to the first
question-mark in the next SQL statement. In this case, if the
value of the form field 'name' was 'fred', then the SQL command
would become:

C<SELECT id FROM users WHERE name LIKE 'fred'>

=back

For security reasons SQL commands will not run if there are 
required, or invalid field types.

=item B<sqluser>

This is the username to use when connecting for the next SQL statement.
Usually used with C<sqlpassword>.

=over 4

=item eg.

C<sqluser: root>

=back

=item B<subject>

A subject line to use on resulting emails.

=over 4

=item eg.

C<subject : This is a feedback email>

=back

=item B<success>

A template file to return through the web browser if the form was correctly
submitted. See the section on L<TEMPLATES> for more information.

=over 4

=item eg.

C<success : /forms/config/success.tpl>

=back

=item B<successmime>

This allows you to specify a specific MIME type for the data returned
back to the browser by the C<success> template. Values given here should
be of the form C<word/word>. Its related to the C<failuremime>,
C<blankmime> and C<expiresmime> config commands.

=over 4

=item eg.

C<successmime : text/xml; charset=utf8>

=back

=item B<unless>

This has an identical format to the C<if> command, but performs the opposite
of what the C<if> tests do. Using this, you can check for when values are not
set. See the section on L<CONDITIONAL STATEMENTS> for more information.

=item B<wrap>

The number of characters to wrap the soupermail emails to.

=over 4

=item eg.

C<wrap : 60>

=back

=back

Sometimes it is useful to concatenate some of the configuration values, for
instance where you need to specify more that one C<mailto> recipient based
on the user's input. In order to do this, you can use the following variables
in you configuration files:

=over 4

=item B<$mailto>

This is the current value of C<mailto> in the configuration. This will be
expanded to the value when the configuration is parsed.

=over 4

=item eg.

=for text
C<mailto : rod@mycompany.com
mailto : "$mailto, jane@mycompany.com">

=for man
C<mailto : rod@mycompany.com
mailto : "$mailto, jane@mycompany.com">

=for html
<pre>mailto : rod@mycompany.com
mailto : "$mailto, jane@mycompany.com"</pre>

This example initially sets C<mailto> to rod@mycompany.com. Then it sets
C<mailto> to rod@mycompany.com, jane@mycompany.com. Notice that the expansion
occurs only if the value is enclosed in double quotes (").

=back

=item B<$subject>

This is used to get the current value of C<subject>

=over 4

=item eg.

=for html
<pre>subject : Feedback of type - 
if (feedtype eq 'comment') then subject : "$subject Comment"
if (feedtype eq 'problem') then subject : "$subject Problem"</pre>

=for text
C<subject : Feedback of type ->
C<if (feedtype eq 'comment') then subject : "$subject Comment">
C<if (feedtype eq 'problem') then subject : "$subject Problem">

=for man
C<subject : Feedback of type ->
C<if (feedtype eq 'comment') then subject : "$subject Comment">
C<if (feedtype eq 'problem') then subject : "$subject Problem">

This example changes the C<subject> based on a field in the original form 
called 'feedtype'.

=back

=item B<$replyto>

This is used to get the current value of the C<replyto> field.

=over 4

=item eg.

=for man
C<replyto : management@mycompany.com
if : (interested has 'rod') then replyto : "$replyto, rod@mycompany.com"
if : (interested has 'jane') then replyto : "$replyto, jane@mycompany.com"
if : (interested has 'freddy') then replyto : "$replyto, freddy@mycompany.com">

=for text
C<replyto : management@mycompany.com
if : (interested has 'rod') then replyto : "$replyto, rod@mycompany.com"
if : (interested has 'jane') then replyto : "$replyto, jane@mycompany.com"
if : (interested has 'freddy') then replyto : "$replyto, freddy@mycompany.com">

=for html
<pre>replyto : management@mycompany.com
if : (interested has 'rod') then replyto : "$replyto, rod@mycompany.com"
if : (interested has 'jane') then replyto : "$replyto, jane@mycompany.com"
if : (interested has 'freddy') then replyto : "$replyto, freddy@mycompany.com"
</pre>

If the form contained a set of checkboxes all called 'interested' with the
values of 'rod', 'jane' and 'freddy', this configuration will add the email
addresses of rod, jane and freddy depending upon which checkboxes were set
by the user.

=back

=item B<CGI variables>

It is possible to use all of the L<CGI VARIABLES> listed below 
by placing a '$' character before their name.

=over 4

=item eg.

C<$http_user_agent>

will return the web browser name.

=back

=item B<Form Variables>

It is possible to use any value from a form by placing '$form_' before the
form variable's name.

=over 4

=item eg.

If a form has a field called 'TheirName', then the following could be used in
the configuration file:

C<Subject: "Form response from $form_TheirName">

=back

=item B<Cookie Variables>

In the same way as its possible to use form variables, cookie variables can
be inserted by putting '$cookie_' before the cookie's name.
See the section on L<COOKIES> for more information.

=over 4

=item eg.

C<Subject: "The cookie named Bungle has value $cookie_Bungle">

=back

=back

Replacements can only be used when setting the subject, mailto, replyto,
reference number and cookie value fields. 

Replacement value will only be used when they are enclosed in double-quotes.
So, the following will NOT work:

=over 4

=item eg.

Subject: This is a non-working mail to $mailto

=back

However, this will work:

=over 4 

=item eg.

Subject: "This is a working mail to $mailto"

=back

=head1 CONDITIONAL STATEMENTS

Conditional statements in configuration files allow you to control the
configuration of a form based on the user's form input, values from a
users cookies or any of the http_ variables. A conditional
statement is made up of a boolean expression followed by a configuration
statement.

=over 4

=item ie.

C<if : I<boolean_expression> then I<configuration_statement>>

or

C<unless : I<boolean_expression> then I<configuration_statement>>

=back

The only configuration statement disallowed in a conditional statement is
another if or unless.

Conditional statements are executed in the same order that they appear in
the configuration file. 

=head2 Boolean Expressions

A boolean expression is something that can either be true or false. If it's
true, then the configuration statement is set, otherwise it isn't.

The simplest boolean expression is just the name of a form field. If the form
field was completed by the user, then the boolean is true.

=over 4

=item eg.

If you have a form that contains and input field called 'name' and you want to
set the C<subject> line based on this name being set, you could use the
following configuration statements:

=for text
C<subject : They haven't set their name
if : name then subject : They have set their name!>

=for man
C<subject : They haven't set their name
if : name then subject : They have set their name!>

=for html
<pre>subject : They haven't set their name
if : name then subject : They have set their name!</pre>

Initially, subject is set to 'They haven't set their name'. However, if the
'name' field is completed on the form, the conditional statement is
activated and the subject is reset to 'They have set their name!'.

=back

If you want to check on cookies, prefix the cookie's name with $cookie_. So,
if you wanted to test if the user had sent a cookie called "MyName", use
a condition like this:

=over 4

=item eg.

C<if: $cookie_MyName then Subject: "Cookie MyName was set to $cookie_MyName">

=back

Boolean expressions in soupermail use three basic operators, AND (&&), 
OR (||) and NOT (!). An expression with an AND in will be true if 
BOTH of the things around the AND are true. An expression with an OR 
in will be true if one or more of the things around the OR is true.
An expression preceded by a NOT will be true if the thing following 
it is false.

=over 4

=item eg.

I<x> && I<y> will be true if I<x> is true and I<y> is true

I<x> || I<y> will be true if I<x> is true or I<y> is true

I<x> && I<y> || I<z> will be true if I<x> and I<y> are both true, or 
I<x> is true.

!I<x> will be true if I<x> is false.

=back

Boolean expressions can contain any number of smaller boolean expressions.
To make life easy, you can group these with brackets "(" and ")".

=over 4

=item eg.

You have a form containing the fields 'name', 'address', 'telephone', 'fax' and
'Email'. You want to know that name has been filled in and that they have
supplied an address or telephone or email. The following boolean expression
could be used:

C< name && (address || telephone || Email)>

Notice the use of brackets, to enclose the ORs. If the brackets were missed 
out, the expression would have meant the user must complete their 
name and address, or their telephone, or their email; or as a boolean 
expression:

C<(name && address) || telephone || Email>

This is because AND is considered to be more important than OR.

=back

If you have form fields that contain spaces, you can still use them in boolean
expressions, but you must enclose them in double quotes (").

=over 4

=item eg.

You have a form containing:

E<lt>input type="text" name="First Name"E<gt>

Any boolean expression using this field name must use it quoted:

C<"First Name">

=back

Other operators available in boolean expressions are:

=over 4

=item B<==>

Numerical equality

=over 4

=item eg.  

C<if : age == 45 then subject : You are 45>

=back

=item B<!=>

Numerical inequality

=over 4

=item eg.  

C<if : age != 50 then subject : You are NOT 50>

=back

=item B<E<lt>=>

Numerically less than or equal to

=over 4

=item eg.  

C<if : age >E<lt>C<= 50 then subject : You are younger than 51>

=back

=item B<E<gt>=>

Numerically greater than or equal to

=over 4

=item eg.  

C<if : age >E<gt>C<= 50 then subject : You are older than 49>

=back

=item B<E<lt>>

Numerically less than

=over 4

=item eg.  

C<if : age E<lt> 50 then subject : You are younger than 50>

=back

=item B<E<gt>>

Numerically greater than

=over 4

=item eg.  

C<if : age E<gt> 50 then subject : You are older than 50>

=back

=item B<eq>

String equality

=over 4

=item eg.  

C<if : name eq 'Humphry' then subject : You are called Humphry>

=back

=item B<ne>

String inequality

=over 4

=item eg.

C<if : name ne 'Humphry' then subject : You are NOT called Humphry>

=back

=item B<le>

String less than or equal to

=item B<ge>

String greater than or equal to

=item B<lt>

String less than

=item B<gt>

String greater than

=item B<has>

A string value is equal to something in a multivalue field

=item B<hasnt>

A string value is not equal to something in a multivalue field

=item B<contains>

A string value exists inside, or is equal to another value. It is 
case-insensitive.

=over 4

=item eg.

C<if : name contains 'on' then subject: Your name contains the letters on>

The above example would match names such as "Ron" or "Donna".

=back

=item B<longerthan>

Returns true if the value to the left is made of more characters
than the value to the right.

=over 4

=item eg.

C<if : name longerthan 5 then subject: Your name has more than 5 characters>

=back

=item B<shorterthan>

Returns true if the value to the left is made of less characters
than the value to the right.

=over 4

=item eg.

C<if : name shorterthan 5 then subject: Your name has less than 5 characters>

=back

=back

=head1 TEMPLATES

Soupermail uses a series of templates specified by the configuration file to
control the output, either to the screen, a file or to email. All the
template locations should be specified relative to the location of the
configuration file, as absolute paths (things starting with a '/' character)
from the web server's root, or as private paths (things starting with
a '~' character). The basis for a template are the 
HTML-like elements called E<lt>outputE<gt>, E<lt>onlyE<gt> and
E<lt>loopE<gt>.

Templates can be used for emails, files and pages returned to the browser.
Templates returned to the browser can be given different MIME types, meaning
you can return things like WML for WAP sites.

When sending HTML email templates, you can set the base for images embedded in
the email with the C<listbase>, C<mailbase> and C<senderbase> commands.

The E<lt>onlyE<gt> element defines a block in a template to use if its
B<if> attribute is matched. The B<if> attribute should contain a boolean
expression. See L<Boolean Expressions> for more information about
what the B<if> attribute can contain.

=over 4

=item eg.

E<lt>only if="month == 12"E<gt>

Its December, so here's December's calendar:

E<lt>!--#include virtual="dec.txt"--E<gt>

E<lt>/onlyE<gt>

=back

E<lt>onlyE<gt> elements cannot be nested, but they can contain any number of
E<lt>outputE<gt> elements and includes.

E<lt>loopE<gt> elements allow one part of a template to be repeated multiple
times. Using loops, you can repeat a section of template a fixed number of
times, or loop through the values of form field.

Loops can take five attributes:

=over 4

=item start

If you need to control when a loop starts, the start attribute sets
the initial value of the loop. This can be any number.

=item end

This is the final value of the loop. It can be any number. If the value of
end is greater than the value of start, the loop counts forward in steps
of one. If the value of end is less than the value of start, the loop counts
backward in steps of minus one.

=item name

Each time Soupermail goes through a loop, you can take the current value
of the loop, and use it in the template. To get the value, you need to
refer to it by the loop's name.

To get the value out, surround the loop's name by @ characters inside
the loop block.

=over 4

=item eg.

=for text
C<E<lt>loop name="loopvalue" start="1" end="5"E<gt>
@loopvalue@
E<lt>/loopE<gt>>

=for html
<pre>&lt;loop name="loopvalue" start="1" end="5"&gt;
@loopvalue@
&lt;/loop&gt;</pre>

This loop will return '1 2 3 4 5'.

=back

=item step

The default step in loops between the start and end values is one.
With the step attribute, you can change this value. Step can take
any number as a value.

=over 4

=item eg.

=for text
C<E<lt>loop name="loopvalue" start="1" end="5" step="2"E<gt>
@loopvalue@
E<lt>/loopE<gt>>

=for html
<pre>&lt;loop name="loopvalue" start="1" end="5" step="2"&gt;
@loopvalue@
&lt;/loop&gt;</pre>

This loop will return '1 3 5'.

=back

=item field

When you need to use a loop to run through the multiple values
of a form field the field attribute is used to specify which
field to loop with.

=over 4

=item eg.

If you have a SELECT element in your form like this:

=for text
C<E<lt>select multiple="multiple" name="multiselect"E<gt>
E<lt>optionE<gt>value one
E<lt>optionE<gt>another value
E<lt>optionE<gt>yet another value
E<lt>/selectE<gt>>

=for html
<pre>&lt;select multiple="multiple" name="multiselect"&gt;
&lt;option&gt;value one
&lt;option&gt;another value
&lt;option&gt;yet another value
&lt;/select&gt;</pre>

you can use the following loop to get the values:

=for text
C<E<lt>loop name="selectfield" field="multiselect"E<gt>
One of the values is @selectfield@
E<lt>/loopE<gt>>

=for html
<pre>&lt;loop name="selectfield" field="multiselect"&gt;
One of the values is @selectfield@
&lt;/loop&gt;</pre>

=back

=back

The E<lt>outputE<gt> element can be considered as analogous to the HTML 
E<lt>inputE<gt> element.

Where an E<lt>outputE<gt> element appears in a template, Soupermail 
replaces it with some appropriate text. The value of the replacement 
text depends upon the attributes specified in the E<lt>outputE<gt> element.

=head2 Attributes for output

The following is a list of attributes that can be placed in template
E<lt>outputE<gt> elements.

=over 4

=item B<alt>

This field is alternative text to replace the E<lt>outputE<gt> element 
with, if the field name wasn't filled in on the original form.

=item B<altvar>

Usually, the value of the C<name> attribute is replaced in the
E<lt>outputE<gt> element. However, using C<altvar>, another variable
can be used if C<name> hasn't a value.

=over 4

=item eg.

Supposing you have a field called 'month' that you want to default to the
current month if it's not filled in in the form. The following could be
used:

E<lt>output name="month" altvar="http_date" format="%mmm%"E<gt>

=back

=item B<case>

This can take the values of B<upper> or B<lower> and will upcase or 
downcase the thing returned by the output element.

=item B<charmap>

Sometimes, you need to change one character in a string to another; for 
instance, escaping quote marks when saving a CSV file. The C<charmap> 
attribute allows a character to be changed to a string (or removed). The
format for the C<charmap> attribute should be the character to change,
followed by a comma, followed by the string to change it to.

=over 4

=item eg.

To double up quote marks for a CSV file, use something like:

E<lt>output name="fieldname" charmap='",""'E<gt>

To remove all occurrences of the letter 'a':

E<lt>output name="fieldname" charmap="a,"E<gt>

To turn underscores into hyphens:

E<lt>output name="fieldname" charmap="_,-"E<gt>

=back

=item B<data>

This is used to check the type of data in the form field. The C<data> attribute
can have the following values: B<number>, B<notnumber>, B<integer>,
B<notinteger>, B<email>, B<notemail>, B<creditcard>, B<notcreditcard>

If the check fails, then the output element will return its C<alt> value.

=over 4

=item eg.

Here are some examples for a form field, 'foo', with a value of 6.5:

E<lt>output name="foo" data="number" alt="fail" sub="pass"E<gt> = pass

E<lt>output name="foo" data="integer" alt="fail" sub="pass"E<gt> = fail

E<lt>output name="foo" data="notnumber" alt="fail" sub="pass"E<gt> = fail

E<lt>output name="foo" data="notinteger" alt="fail" sub="pass"E<gt> = pass

E<lt>output name="foo" data="email" alt="fail" sub="pass"E<gt> = fail

=back

The credit card check is a simple LUHN checksum that makes sure the number
given looks like a credit card number. It does not mean the number is a real
card number, or that there's any money in the account.

=item B<delim>

A text string to display between items in a text C<list>. 

=item B<format>

A format to specify how certain variables are formatted when displayed. Only 
applies to http_time, http_date and http_ref.

=item B<indent>

This is a string to indent the substituted text with. Its mainly useful
for email templates, where you may want to indent the contents of an HTML
textarea element.

=item B<list>

When an E<lt>outputE<gt> element is replaced by a multivalued form field, 
Soupermail's default behavior is to output a HTML E<lt>ulE<gt> list, or 
text list. By setting the C<list> attribute to ul|ol|menu|dir|text, a 
specific type of HTML list can be achieved. The text value will return a 
non-HTML text list. The format of this text list can be controlled by the 
C<delim> attribute.

=item B<math>

You can use simple maths expressions using this attribute. You can use
form, cookie and http values in the C<math> expression, and they will be
replaced before the expression is evaluated. Values that are undefined or
non-numeric are replaced by zero. If the C<name> attribute is multi-valued,
the C<math> expression is evalued for each value.

The following are the maths operators available:

=over 4

=item +

addition

=item -

subtraction

=item C<   *>

multiplication

=item /

division

=item sum()

summation of a multiple valued field

=item count()

count of a multiple valued field

=back
 
To add two fields together:

E<lt>output name="field1" math="field1 + field2"E<gt>

To calculate an average of a number of fields:

E<lt>output name="field1" math="(field1 + field2 + field3) / 3"E<gt>
 
=item B<name>

This should correspond to a field name from the HTML form, a CGI  
Variable available from Soupermail a cookie name, a counter value,
a mailing list value or a SQL value.
L<CGI variables> start with 'http_', counter values
start wit 'counter_', cookie values start
with 'cookie_', mailing list values start with 'mailist_' and SQL values 
start 'sql_'. This field is case-sensitive.

=item B<newline>

This allows newlines to be represented as either HTML or removed from the
value. If C<newline> has the value B<html>, then newline characters
are converted to E<lt>brE<gt> tags. If it has the value of B<none>, then
newline characters are replaced by spaces. If it has a value of
B<unchanged> then newlines are left as is. The value of B<paragraphs>
replaces breaks of more than 2 newlines with only 2 newlines - useful
for formatting plain text entries.

=item B<post>

This is text to be post-pended to the value of the field name if the
field was set in the original form. It isn't used with the C<alt> or C<sub>
attributes. For multivalue entries, the C<post> section is placed after each
list item.

=item B<pre>

This is text to be pre-pended to the value of the field name if the field 
name was set in the original form. It isn't used with the C<alt> or 
C<sub> attributes. For multivalue entries, the C<pre> section is placed 
before each list item.

=item B<precision>

Used in conjunction with the C<math> attribute, this value is the number of
decimal places to display numbers to.

=item B<sub>

This is text to replace the output field with if the field is set in the 
original form.

=item B<subvar>

This is similar to the C<altvar> attribute, but comes into play when the
variable set be the C<name> attribute has a value. 

=item B<timeoffset>

This is used for providing a time offset when outputting 
B<http_time> and B<http_date> values. Values should be of the form:

C<[+|-]>I<num>C<[smhdMy]>

Where, the initial plus and minus indicate the direction of the offset,
I<num> represents how much to offset by, and C<s> indicates an offset in
seconds, C<m> an offset in minutes, C<h> an offset in hours, C<d> an
offset in days, C<M> an offset in months and C<y> an offset in years.

=item B<type>

If type is set, it can be one of B<escaped>, B<unescaped>, B<html> or
B<unescapedhtml>. Escaping output tags is useful if you want to pass 
form values between forms in hidden form fields. Escaped output tags 
are URL encoded, so characters such as E<lt> and " don't appear. 
When you want to get the user's original values, use the B<unescaped> 
or B<unescapedhtml> types in an output tag. The B<html> type is useful
for displaying values in HTML templates where a user may have typed in
HTML characters such as E<lt> or E<gt>.

=over 4

=item eg.

If you have a field like this:

E<lt>input type="text" name="val"E<gt>

and this in a template:

E<lt>input type=hidden name=val value="E<lt>output name="val"E<gt>"E<gt>

and the user's typed something like this into the field:

B<The "sum" is E<gt> than the "parts">

If you don't escape the output tag, you get broken HTML like this:

E<lt>input type=hidden name=val value="The "sum" is E<gt> than the "parts""E<gt>

However, if you used E<lt>output name="val" type="html"E<gt>, you'd get:

E<lt>input type=hidden name=val value="The &amp;#34;sum&amp;#34; is &#62; than the &amp;#34;parts&amp;#34;"E<gt>

which is HTML safe.

=back

=item B<value>

Usually, if the thing set by C<name> has a value, it is returned by the
E<lt>outputE<gt> element. However, if C<value> is set, it is only returned
if its value equals that of B<value>. The C<alt> attribute will become active
if the values do not match and the C<sub> attribute will become active if
they do match. This may sound pretty daft, but its
useful for regenerating drop down lists in multipart forms. See the
Multipart form example that comes with Soupermail.

=item B<valuevar>

Similar to the C<value> attribute, but affects the use of C<altvar> and
C<subvar> replacement.

=item B<wrap>

An integer specifying how many characters to wrap the output value to.
Wrapping occurs after any maths, charmap or HTML conversions have
been applied to the value, but before the PRE and POST attributes take
effect. This attribute is useful for formatting HTML textarea elements.

=back

=head2 SSI Like Includes

Server Side Includes (SSI) are a means of dropping one file into another
before sending a page onto the user's browser. Soupermail can provide a basic
inclusion mechanism using the same syntax as normal SSI directives. Soupermail
will only handle E<lt>!--#include virtual="..."--E<gt> type includes, #exec
is too much of a processing burden. The path can either be an absolute path
from the server's root, or a path relative to the location of the config
file.

If you are putting the include into a HTML page, and don't want characters
like E<lt> to be specially treated by the browser, then you should put the
type="html" attribute in the include call: 
E<lt>!--#include virtual="..." type="html"--E<gt>. ALWAYS do this if
you do not trust the source of the include.

=head1 CGI VARIABLES

CGI variables are set by the web server, and in some specific cases, Soupermail.
These names should not be used as field names in your HTML forms.

=over 4

=item B<counter_I<X>>

The value of the counter named I<X>

=item B<http_time>

The time at the web server.

=item B<http_date>

The date at the web server.

=item B<http_referer>

The URL of the calling form.

=item B<http_remote_host>

The hostname of the person sending the form.

=item B<http_remote_addr>

The IP address of the person sending the form.

=item B<http_server_name>

The name of the webserver.

=item B<http_server_port>

The port number the webserver is listening on.

=item B<http_user_agent>

The type of browser used to send the form.

=item B<http_ref>

A soupermail generated reference number.

=item B<http_remote_user>

The username if the form was password protected.

=item B<http_remote_ident>

Not sure, but some browsers set it.

=item B<http_host>

The server name the browser thinks its at.

=item B<http_from>

A browser specific variable

=item B<http_config_error>

The last error message set in the config file with the 
C<error> config command.

=item B<http_config_path>

The path from the web server's root to the configuration file
that was used to generate the page. This can be very useful
when generating multipart forms, where you want to keep your
directory structure portable by using relative links.

=item B<maillist_I<X>>

This is a value from the current C<mailist> line of data. I<X> is the
column number of the data to use. Columns start at one (the email
address). See L<MAILING LISTS> for more information.

=back

=head1 FORMATS

Formats allow the http_time, http_date and http_ref variables to be controlled.
A format is a one line string containing the following substrings. When the 
E<lt>outputE<gt> element is expanded, the substrings are expanded into the 
following:

=over 4

=item B<%yyyy%>

A 4 digit year (eg. 1997)

=item B<%yy%>

A two digit year (eg. 97)

=item B<%mmmm%>

A three letter month code (eg. Jan)

=item B<%mmm%>

A two digit month code

=item B<%ddd%>

A three letter day code (eg. Mon)

=item B<%dd%>

A two digit day code (eg. 28)

=item B<%hhhh%>

A 2 digit 24 hour (eg. 13)

=item B<%hh%>

A 2 digit hour (eg. 03)

=item B<%mm%>

A 2 digit minute (eg. 23)

=item B<%ss%>

A 2 digit second (eg. 06)

=item B<%ampm%>

Either 'am' or 'pm' depending on what the time is.

=item B<%epoch%>

Return the epoch time for your system. On UNIX, this is the number of seconds
since 00:00:00, 01/01/1970.

=item B<%r...%>

A random number. The length of the random number is determined by the 
number of r's in the format. The maximum number of r's is 12. eg. %rrr% returns
a value between 0 and 999.

=item B<%c...%>

This is a formatting command used to break a number into a series of
space delimited blocks. The number of B<c> characters given determines
how many characters to use before a space.

=over 4

=item eg., to format a credit card number

use C<format="%cccc%"> which would give you something like:

C<1234 5678 9876 5432>

C<format="%ccc%"> would give you:

C<123 456 789 876 543 2>

=back

Non-numeric characters are removed from the value.


=item B<%counter_I<X>%>

This is the value of a config file specified counter. The value used is
calculated B<after> any increments or sets are performed on the counter, so
it will be the same value that appears in templates. The value of I<X> is
the counter number needed. eg. %counter_3%

=back

=head1 COUNTERS

Counters are a way of storing and reading the number of times Soupermail has
done something. They are specified in the configuration file, and you can have
any number of them in use. In their simplest guise, you can use them to count
how many people have submitted a form. More complex uses include setting
the maximum number of times a form's submitted, online voting systems
and renaming the filenames form information is saved to.

The behaviour of counters can be slightly odd for the unwary. Firstly, they
are always defined in the config file, but simply declaring a counter file
does not mean it gets updated, its value just becomes available for the config
file and for templates. To update a counter, an onsuccess, onfailure, onblank
or onexpires setting for the counter must be set.

Secondly, the value returned by a counter in the config file is the value
stored in the counter file BEFORE any increments have been performed on the
counter, however, the value returned in templates and the http_ref value
are set AFTER increments have been applied to the counter.

=over 4

=item eg.

=for man
C<mailto: cookiemonster@example.org
counter1file: counters/count1.txt
counter1onsuccess: yes
if : ("$counter_1" == 10) then setcounter1 : 1
if : ("$counter_1" == 10) then mailto : thecount@example.net>

=for text
C<mailto: cookiemonster@example.org
counter1file: counters/count1.txt
counter1onsuccess: yes
if : ("$counter_1" == 10) then setcounter1 : 1
if : ("$counter_1" == 10) then mailto : thecount@example.net>

=for html
<pre>mailto: cookiemonster@example.org
counter1file: counters/count1.txt
counter1onsuccess: yes
if : ("$counter_1" == 10) then setcounter1 : 1
if : ("$counter_1" == 10) then mailto : thecount@example.net
</pre>

The above example would result in counter1 being set to 1 and the mailto
address set to thecount@example.net whenever the counter reached 10.
Note that even though the 
C<setcounter1> is set in the config file, it does not have an immediate
effect, and does not prevent the second C<if> statement being used.

=back

=head1 COOKIES

Cookies were introduced in Netscape Navigator 2.0. They are a means of 
storing information on the user's browser even after they've turned off their
computer. Soupermail allows up to nine cookies to be set, each cookie holding
at most 516 characters worth of data, and with a cookie name less than 50
characters long. The restriction on the cookie size and number of cookies
is mainly out of politeness, because its not considered nice to flood users
with cookies.

More information on cookies can be found at 
http://home.netscape.com/eng/mozilla/3.0/handbook/javascript/index.html

=head1 USING PGP

PGP is a means of encrypting text through a public key and decrypting through
a private key. Using PGP, Soupermail can send secure encrypted email over
an insecure Internet.

To use PGP, you will need to place a public keyring (pubring.pkr for
PGP 5, pubring.pgp for PGP 2.6.3 or pubring.gpg for GPG) in the 
directory where your form's configuration file is located. In your
configuration file, set B<pgpuserid> to be a user in the pubring keyring.
When soupermail generates an email, it will encrypt the message using the
public key of the given user. By default, this version of Soupermail 
assumes that GPG is being used.

As of Soupermail 1.0.3, GNU Privacy Guard (GPG) is supported as an alternative
to using PGP. Using GPG rather than PGP differs only in that the public
keyring file is called pubring.gpg.  The C<pgpversion> config option must be set
to choose between the different encryption methods. See the GPG documentation 
for more information.

If you have problems using PGP or GPG, make sure your webserver has the ability
to run the scripts - some server installations may not give the nobody user
rights for this. Generating a debug file is the best diagnostic option.

Versions of Soupermail greater than 1.0.8 have support for PGP 5.0i and 2.6.3i
(I've only tested the international versions so people using US versions may
have different results).

You can also specify a PGP keyserver in the configuration file. If specified,
the PGP encryption will look on the key server for encryption keys.
B<THE PGP KEYSERVER CODE IS EXPERIMENTAL AND HASN'T BEEN TESTED! USE AT YOUR
OWN RISK!>

For more information on PGP, please look at http://www.pgpi.org/

For more information on GPG, please look at http://www.gnupg.org/

=head1 MAKING PDFs

From version 1.0.7, Soupermail can generate Adobe PDF files by hooking up to
lout and ghostscript.

Lout is a nifty document formatting language, which is used to generate 
postscript files. Ghostscript is a postscript processor which can generate 
PDF files (amongst other things).

To use this feature, you're going to have to look into how lout templates work.
Its a powerful language, so spend some time delving though the documentation 
that comes with lout. Basically, Soupermail hooks into lout by allowing 
you to use E<lt>outputE<gt> elements in lout templates. Soupermail reads 
the lout templates you specify with the C<pdftemplate> config options, fills 
in the E<lt>outputE<gt> elements, then passes this on to lout and 
ghostscript to handle. The results can be emailed out, or returned to 
the browser depending on the config options you have used.

One of the nice things about using lout and ghostscript together is 
the ability to include EPS images in your generated PDFs. To do this, 
place your EPS files in the same directory as your lout templates and 
use lout's include image command in your templates. Soupermail assumes that
EPS files end in a C<.eps> file extension.

The Soupermail example files contain an example of using Soupermail's 
PDF commands.

To use the PDF commands, you'll need to install GhostScript from
http://www.cs.wisc.edu/~ghost/index.html and Lout from
ftp://ftp.cs.usyd.edu.au/jeff/lout/.


=head1 MAILING LISTS

Version 1.0.7 of Soupermail brings along mailing lists, which are ways of
sending Soupermail generated email to a set of people defined in a
file. To do this, you should specify a C<maillist> file in your form's
configuration. The C<maillist> file should be a set of lines, each one
starting with and email address, and with other optional columns following,
separated by commas.

=over 4

=item eg.

=for man
C<foo.bar@example.net,Mr Foo,nothing special
fred.bloggs@example.com,"Bloggs, Fred",geezer
xyz@example.com,XYZ Man,unable to think of a better name>

=for text
C<foo.bar@example.net,Mr Foo,nothing special
fred.bloggs@example.com,"Bloggs, Fred",geezer
xyz@example.com,XYZ Man,unable to think of a better name>

=for html 
<pre>foo.bar@example.net,Mr Foo,nothing special
fred.bloggs@example.com,"Bloggs, Fred",geezer
xyz@example.com,XYZ Man,unable to think of a better name,other stuff</pre>

=back

As you should see from the example, there can be any number of extra
columns of data in the file. When Soupermail is given a mailing list file,
it generates an email for each address in the file based on the
C<listtemplate> and C<htmllisttemplate> config options. However, these
templates can also take data from extra columns in the maillist file
and use them in E<lt>outputE<gt> elements.

=over 4

=item eg.

From our previous example, if the C<listtemplate> contains the following:

C<Hi >E<lt>C<output name="maillist_2">E<gt>C<, Email: >E<lt>C<output name="maillist_1">E<gt>

Then the email sent out to foo.bar@example.net would contain:

Hi Mr Foo, Email: foo.bar@example.net

the email sent out to fred.bloggs@example.com would contain:

Hi Bloggs, Fred, Email: fred.bloggs@example.com

and the email sent out to xyz@example.com would contain

Hi XYZ Man, Email: xyz@example.com

=back

Email addresses and other column data is not shared between the email addresses
in the list. However, if your list is private, you should ensure it isn't
browsable from the internet.

Sometimes, you don't have your mailing list data in a file - to handle this, there
are two other sources of list information. It is possible to pull list information
from a form field using the C<listformfield> config command to provide 
the list data. The format of the list data provided by the form field should
be the same format as for the data file - ie. email as the first field, with
other fields separated by commas.

Even more useful, it is possible to pull mailing list information from a
SQL database by using the C<listsql> command. This specifies a SQL statement 
which returns a table, the first field of which should be an email address.

It is possible to attach files to emails sent out with a mailing list using
the C<listattachmentI<X>> and C<listattachmentI<X>mime> commands.

Other list config commands are: C<listsubject>, C<listfrom> and
C<listreplyto>.

=head1 PIPELINING

Pipelining Soupermail allows you to use Soupermail to process a form and then
send on the original information to another URL for processing. This is
useful if you want to use Soupermail as a logger, or as a quick email
function to another web application.

To use pipelining, you need to use the C<gotosuccess>, C<gotoblank>,
C<gotofailure> and C<gotoexpires> config commands. These commands
usually specify a URL to go to once Soupermail has finished, but they
can also be used dynamically by using variable replacement of
L<CGI VARIABLES>.

=over 4

=item eg.

Once Soupermail's finished, I want to send the form onto a page
with the field B<foo> set to the word B<bar>. I can do this with the
following:

C<success: http://www.example.org/myscript?>B<foo>C<=>B<bar>

Now though, suppose I want to send whatever the user typed into one of
my form fields (eg. B<myfoofield>). I can use the following:

C<success: "http://wwww.example.org/myscript?>B<foo>C<=>B<${form_myfoofield}>C<">

=back

Some things to notice; The value of the config command has been wrapped in
double quotes - this allows CGI value replacement to happen. 
The CGI value replacement is wrapped in { } braces - this makes it easier
to distinguish the value.

What about sending multiple values? Well, you can have things like:

B<C<foo>>=B<C<${form_myfoofield}>>C<&>B<C<baz>>C<=>B<C<${cookie_myBazCookie}>>

Here, B<foo> is set to whatever value B<myfoofield> was in the original
form, and B<baz> is set to whatever value the cookie B<myBazCookie> has. The
ampersand (&) character is used to separate the values.

For those of you who may be doing advanced pipelining, you should know that
URI escaping is only done to replaced values. So, this is wrong:

C<B<foo>=B<my value>&B<baz>=B<${form_baz}>>

The space is illegal in URLs. It should be:

C<B<foo>=B<my%20value>&B<baz>=B<${form_baz}>>

=head1 DATABASE SUPPORT

As from version 1.0.8, Soupermail has included support for database
access. It can be used to query, insert, amend and delete records in
a database. The commands used for this are:

C<sqlbindI<X>>

C<sqlname>

C<sqlpassword>

C<sqlrunI<X>>

C<sqluser>

One important feature of Soupermail is the ability to use the values
returned by SQL SELECT statements in your config files and in templates.
All C<sqlrunI<X>> commands have an identifying number. All SQL commands
that return a table populate a two dimensional array of values. Used
in conjunction with the command number, it is possible to get 
any return value from a SQL command.

=over 4

=item eg.

Lets say we have a table called 'test' containing these values:

=for text
1    foo     boo
2    dish    dash
3    moo     maa

=for html
<table border="1">
<tr><td>1</td><td>foo</td><td>boo</td></tr>
<tr><td>2</td><td>dish</td><td>dash</td></tr>
<tr><td>3</td><td>moo</td><td>maa</td></tr>
</table>

Then, we have the following in our config:

C<sqlrun1: SELECT * FROM test>

We can get values back from this by using the variable
I<sql_[command_number]_[row_number]_[col_number]>. In config files,
this value should be prefixed with a $ sign.

In a config file:

C<if: "$sql_1_3_1" then subject: The test table has at least 3 rows>

In a template:

The third field on the second row of the table test is:

E<lt>output name="sql_1_2_3"E<gt> = dash

=back

To make use of database support with Soupermail, you'll need perl's DBI module
installed, and an appropriate DBD driver for your database. This driver must
support placeholders and bind values. Consult your DBD driver's manual
for more information on this.

=head1 PRIVATE ROOTS

From version 1.0.8, it is possible to store configuration files,
attachment files, templates and writable locations outside
your webserver's document tree. This is to allow you to store
information without it being viewable with a browser.

Not all ISP's will provide you with a directory outside your 
document tree, so you may need to ask their support staff
for an appropriate location.

To call a config file in a private root, prefix the filename
with a '~' character when setting SoupermailConf.

=over 4

=item eg.

C<E<lt>input type="hidden" name="SoupermailConf" value="~/subscribe/sub.con"E<gt>>

Looks for a config file $privateRoot/subscribe/sub.con

=back

One security restriction on private roots is that config files
outside the private root cannot read data from inside the config
root. ie. You can not have a config file outside the private
root calling a template inside the private root. The aim of this
is to save you if someone manages to write a config file on your
server. See the section on L<SECURITY> for more information about
making Soupermail paranoid.

=head1 SECURITY

With the introduction of database support, Soupermail has become
a bit of a security headache for the consciencious webmaster. Here
are some tips about using Soupermail in a secure manner.

Firstly, NEVER put a database password and username in an unsecured
config file. If the config file can be read by a user with a web
browser, and the file contains database connection information, then
you are in trouble. Use the $privateRoot Soupermail has to put
your config files outside the webserver tree.

NEVER use a database user with high privileges (eg. sa, system, sys, root)
to access your database via Soupermail, unless you are in a very
trusted environment and you know exactly what will be going into
your SQL statements.

ALWAYS ensure you are using a good random password for your database
access - people's names and stuff are trivial to brute-force.

If you have a database with a network daemon, ALWAYS consider ways you
can restrict access to only known hosts.

ALWAYS use requires, length checking and type checking in config files 
to make sure the data you pass to your SQL commands is valid.

NEVER make web writable directories in your CGI area.

ALWAYS consider how you will protect files written by Soupermail on
your webserver. Protecting the files usually involves ensuring that
they are safe from being read from a browser, the area being written
to cannot contain executables, that there is no means of anonymously
FTPing to the area and that other users on the system cannot exploit
the area.

ALWAYS remove backup files and temporary files from your live sites.

NEVER transmit credit card details by un-encrypted email.

NEVER store credit card numbers un-encrypted on your webspace.

Get to know the admin staff of your server space, or, at least find your
way around your service provider's support web pages.  If they don't have
support web pages, then worry.

If your job is to maintain your website, make sure you've read
http://www.w3.org/Security/FAQ/.  Website security is easily compromised
by misconfiguration of software - if you didn't read up about it, its 
your fault.

Where possible, use secure communications to your webspace, rather than
insecure access (eg. SCP rather than FTP, SSH rather than Telnet,
encrypted pcAnywhere, etc). IMHO, this is simple common sense, but it 
never hurts to say it again.

When you have Soupermail installed, you should be extra careful about
people being able to write config files to your system. If you are
using something like a message board, it may be possible for
someone to write a config file with it, and then use that config file
to read sensitive pages off your website. Beware!

To help counter this, from version 1.0.8, Soupermail will not read any
files from a directory containing a file called "soupermail.deny" (all
lower case). This file doesn't have to contain anything, just exist.
Place a soupermail.deny file in any directory that contains untrusted
content. Also place a soupermail.deny in any directory that contains
sensitive information (eg. ASP or PHP code containing database 
logon details).

For even more security, you can set the $paranoid variable in Soupermail.
In this mode, Soupermail won't read any files from a directory, unless
the directory contains a file called "soupermail.allow". This is
the recommended approach for security conscious webmasters.

=head1 REQUIREMENTS

Soupermail requires perl 5.004 or better. See http://www.perl.com/ for where
to get perl from, or http://www.activestate.com/ if you need the Windows NT
version of Perl.

To handle the CGI input, Soupermail needs Lincoln D. Stein's excellent
CGI module, available from 
http://www.genome.wi.mit.edu/ftp/pub/software/WWW/cgi_docs.html

To do anything, Soupermail needs the MIME::Lite module installed on your
server. This module can be downloaded from CPAN.
http://www.cpan.org/modules/by-module/MIME/

To send email, Soupermail either needs a working Net::SMTP perl module 
installed on the server, or, if you are on a UNIX server, a working 
sendmail. Net::SMTP is distributed as part of the 
Libnet set of packages available from CPAN. For users on Windows NT,
libnet is available with Activestate's Perl Package Manager.

On UNIX boxes, PGP requires PGP 2.6.3 or 5.0, available internationally from
http://www.pgpi.org/

Under NT, you can use the DOS version of PGP 5, again, available from
http://www.pgpi.org/. Unfortunately, I haven't got version 6.x to work
yet, so its the 16bit only.

GNU Privacy Guard is available from http://www.gnupg.org/


=head1 EXAMPLES

Some examples are distributed with Soupermail in
http://soupermail.sourceforge.net/downloads/examples.zip. 
If anyone has any good sites with examples, please let me know.

=head1 AUTHOR

Vittal Aithal E<lt>vittal.aithal@bigfoot.comE<gt>

=head1 CREDITS

I'd would be wrong to say I wrote this all on my own, other people made my life
difficult on the way, so I'd better credit them (only joking guys :) 
A round of applause for everyone at
http://soupermail.sourceforge.net/credits.txt

=head1 HISTORY

Soupermail started life in late 1995 as a fairly lightweight CGI to handle 
emails. However, as the years went by, it began to suffer heavily 
from creeping featuritis, and has now grown into a monster. It started life
at Unipalm PIPEX, and various copies/versions are used by a number of 
companies. UUNET UK ( http://www.uk.uu.net/ ) maintain a copy for their
WorldWeb service users, this copy escaped and worked at 
Ionica. However, things went a bit pear-shaped, so now it teleworks
from my house or from Revolution ( http://www.revolutionltd.com/ ).

=head1 BUGS

Success with PGP/GPG is highly variable upon platform its run on :( GPG
often depends on the Entropy Gathering Daemon to generate random numbers
and this may not work in a webserver user context.

CGIWrapped environments can prevent the config file location being passed in
with the PATH_INFO option, and will result in a config file error unless the
config location is passed in with the SoupermailConf form field.

Soupermail suffers from major bloat, but I just haven't worked up the will
to cull it down. The template code really needs to be modularised out.

Empty config files return a Thank you message, although nothing has happened.
Its debatable if this is correct.

=cut
 
# vim:ts=4

