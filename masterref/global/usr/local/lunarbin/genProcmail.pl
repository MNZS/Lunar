#!/usr/bin/perl -w

use strict;
use File::Copy;
use Config::IniFiles;
use Lunar::Restrict;
use Lunar::Users;

# $Id: genProcmail.pl,v 1.10 2003/10/01 19:28:55 root Exp $

# Limit where script is ran
&limitHost('host');

my $revision = '1.0';
my $deny = '/usr/local/ref/email/procmail/procmail.deny';
my $cfgFile = '/etc/user-options/users.conf';
my $sa = 'spamassassin';
my $proc = '.procmail.' . $sa;

my %userList = &getUsers('customers');

my $cfg = Config::IniFiles->new(
                -file => $cfgFile,
                -nocase => 1,
                );

for my $user(keys %userList) {
  if (-d $userList{$user}{'dir'}) {
    &makeProcmail($user,$userList{$user}{'dir'});
  } else {
    next;
  }
}

sub makeProcmail {
  my $user = shift;
  my $home = shift;
  open(FH,">$home/.procmailrc")
    or die "Can't open $home/.procmailrc : $!\n";

print FH <<CFG;
# Procmailrc $revision 
LOGFILE=\$HOME/.procmail.log
TIMEOUT=60
INCLUDERC=.procmail.allow
INCLUDERC=.procmail.deny
INCLUDERC=.procmail.spamassassin
CFG
  
  close(FH);

  ## create icb allow file placeholder 
  if ( !-e "$home/.procmail.allow" ) {
    open(FH,">$home/.procmail.allow")
      or die "Can't open $home/.procmail.allow : $!\n";
    print FH "\#\# Placeholder for allow statements";
    close(FH);
  }

  ## create global denies
  copy($deny,"$home/.procmail.deny")
    or die "Can't copy deny to $home/.procmail.deny\n";

  ## create the spamassassin include placeholder
  &genSAFile($user);
}

sub genSAFile {
  my $user = shift;
  if (!$cfg->val($user,$sa)) {
    open(FH,">$userList{$user}{'dir'}/$proc")
      or die "Can't open $userList{$user}{'dir'}/$proc : $!\n";
    print FH "\#\# Placeholder for spamassassin";
    close(FH);

  } elsif ($cfg->val($user,$sa) eq 'on') {
    open(FH,">$userList{$user}{'dir'}/$proc")
      or die "Can't open $userList{$user}{'dir'}/$proc : $!\n";

print FH <<SA;
:0fw: spamassassin.lock
| /usr/bin/spamassassin

# Mails with a score of 15 or higher are almost certainly spam (with 0.05%
# false positives according to rules/STATISTICS.txt). Let's put them in a
# different mbox. (This one is optional.)
:0:
* ^X-Spam-Level: \\*\\*\\*\\*\\*\\*\\*\\*\\*\\*\\*\\*\\*\\*\\*
/dev/null
SA
 
    close(FH);
  } else {
    open(FH,">$userList{$user}{'dir'}/$proc")
      or die "Can't open $userList{$user}{'dir'}/$proc : $!\n";
    print FH "\#\# Placeholder for spamassassin";
    close(FH);
  }
}
