# $Id: check_lockfile.pl,v 1.2 2003/06/10 14:19:33 root Exp $
# quit if lockfile
my $lockfile = '/var/run/allServices.lock';
if (-e $lockfile) {
  exit 1;
}
 
1;
