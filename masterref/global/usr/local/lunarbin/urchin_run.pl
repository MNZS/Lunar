#!/usr/bin/perl -w

# MasterRef
# $Id: urchin_run.pl,v 1.1 2003/04/02 19:08:41 root Exp $

use strict;
use Sys::Hostname;

if (hostname() !~ /^host/) {
  exit 1;
}

system("/usr/local/urchin/urchin -q");