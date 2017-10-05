# $Id: .bashrc,v 1.8 2003/09/23 19:27:11 root Exp $

# User specific aliases and functions
alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

if [ $HOSTNAME = "name1.lunarhosting.net" ]; then
  export MRTG_DIR="/usr/local/mrtg-2.9.25"
fi

export LANG="en_US"

# Source global aliases
if [ -f /etc/bash-aliases ]; then
	. /etc/bash-aliases
fi

