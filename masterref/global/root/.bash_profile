# $Id: .bash_profile,v 1.2 2003/01/23 01:29:55 root Exp $

# Get the aliases and functions
if [ -f ~/.bashrc ]; then
	. ~/.bashrc
fi

## set hostname for options
HOSTNAME=`hostname`

## configure path
PATH=$PATH:$HOME/bin
PATH=$PATH:/usr/local/apache/bin
PATH=$PATH:/usr/local/lunarbin
PATH=$PATH:/usr/local/rrdtool/bin
if [ $HOSTNAME = 'name2.lunarhosting.net' ]; then
  PATH=$PATH:/usr/local/masterbin
fi

BASH_ENV=$HOME/.bashrc
USERNAME="root"

## set LANG for perl compatibility
LANG=en_US

export USERNAME BASH_ENV PATH LANG

## configure delete key for vi
stty erase ^?
