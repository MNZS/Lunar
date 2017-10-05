#package Lunar::PackageName;

## $Id: Users.pm,v 1.3 2003/08/20 06:16:22 root Exp $

use strict;
use warnings;

BEGIN {
  use Exporter ();
  our ($VERSION, @ISA, @EXPORT, @EXPORT_OK, %EXPORT_TAGS);

  # set the version for version checking
  $VERSION     = 1.00;

  @ISA         = qw(Exporter);
  @EXPORT      = qw(
			&getUsers
  );

  %EXPORT_TAGS = ( );

  @EXPORT_OK   = @EXPORT;

}

## add subroutine here

sub getUsers {
  ## return a hash of the system's users and their information

  my $opt = shift;

  my %unpriv;
  my %priv;
  my %staff;

  ## create a list of the system users
  open(PW,'/etc/passwd')
    or die "Can't open /etc/passwd : $!\n";
  my @userList = <PW>;
  close(PW);

  ## create hashes of users
  for my $line(@userList) {
    my ($user,$placeholder,$uid,$gid,$gecos,$homedir,$shell) = split(/:/,$line);
    if ($user eq 'cmenzes') {
      $staff{$user}{'uid'} = $uid;
      $staff{$user}{'dir'} = $homedir;
      $staff{$user}{'shell'} = $shell;
    } elsif ($uid < 500) {
      $priv{$user}{'uid'} = $uid;
      $priv{$user}{'dir'} = $homedir;
      $priv{$user}{'shell'} = $shell;
    } else {
      $unpriv{$user}{'uid'} = $uid;
      $unpriv{$user}{'dir'} = $homedir;
      $unpriv{$user}{'shell'} = $shell;
    }
  }

  ## return based on how we are called
  if ($opt =~ /user|customer|pop/) {
    return(%unpriv);
  } elsif ($opt =~ /system|priv/) {
    return(%priv);
  } elsif ($opt =~ /nostaff/) {
    return(%priv,%unpriv);
  } elsif ($opt =~ /staff/) {
    return(%staff);
  } elsif ($opt =~ /all/) {
    return(%staff,%priv,%unpriv);
  }
}

## needed for module completion
1; 
