## $Id: .bashrc,v 1.4 2003/07/24 18:38:02 root Exp $

# source global definitions
source /etc/profile
source /etc/bashrc

# set up term
export TERM="vt100"

# set up the prompt
H=`hostname -f | tr a-z A-Z`
export PS1="- \[\033[0;36m\]$H\[\033[0m\] -\n[\w] Yes, my master? >"

# set up my path
export PATH="$HOME/bin:/usr/local/bin:/bin:/usr/bin:/usr/sbin:/sbin:/usr/local/lunarbin:/masterbin:/usr/local/apache/bin";

# cvs related variables
export EDITOR=/usr/bin/vim
export CVSROOT=/usr/local/cvsroot

# This is for things that are completely host specific.
if [ -f ~/.bash_local ]; then
  source ~/.bash_local
fi

if [ -f /etc/bash-aliases ]; then
  source /etc/bash-aliases
fi
