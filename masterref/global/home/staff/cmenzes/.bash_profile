## $Id: .bash_profile,v 1.1 2003/03/05 08:12:18 root Exp $

HISTSIZE=300
HISTFILESIZE=500

ulimit -c 1000000
umask 022
USER=`id -un`
LOGNAME=$USER
HOSTNAME=`/bin/hostname`

# Get the aliases and functions
if [ -f ~/.bashrc ]; then
        . ~/.bashrc
fi

export HOSTNAME USER LOGNAME
export HISTSIZE HISTFILESIZE

stty erase ^?
