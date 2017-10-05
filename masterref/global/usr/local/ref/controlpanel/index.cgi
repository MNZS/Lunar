#!/usr/bin/perl -w

# $Id: index.cgi,v 1.3 2003/04/09 23:20:03 root Exp $

use strict;
use Cwd;

my $rcs = (qw$Revision: 1.3 $)[-1];
my $domain = (split(/\//,cwd()))[-2];

print qq#Location: https://www.$domain/controlpanel/panel.cgi\n\n#;
exit(0);
